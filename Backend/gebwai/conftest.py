from typing import Any, AsyncGenerator
from unittest.mock import Mock

import pytest
from aiokafka import AIOKafkaProducer
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from httpx import AsyncClient
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool
from redis.asyncio import ConnectionPool

from gebwai.db.dependencies import get_db_pool
from gebwai.services.kafka.dependencies import get_kafka_producer
from gebwai.services.kafka.lifetime import init_kafka, shutdown_kafka
from gebwai.services.redis.dependency import get_redis_pool
from gebwai.settings import settings
from gebwai.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


async def drop_db() -> None:
    """Drops database after tests."""
    pool = AsyncConnectionPool(conninfo=str(settings.db_url.with_path("/postgres")))
    await pool.wait()
    async with pool.connection() as conn:
        await conn.set_autocommit(True)
        await conn.execute(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            "WHERE pg_stat_activity.datname = %(dbname)s "
            "AND pid <> pg_backend_pid();",
            params={
                "dbname": settings.db_base,
            },
        )
        await conn.execute(
            f"DROP DATABASE {settings.db_base}",
        )
    await pool.close()


async def create_db() -> None:  # noqa: WPS217
    """Creates database for tests."""
    pool = AsyncConnectionPool(conninfo=str(settings.db_url.with_path("/postgres")))
    await pool.wait()
    async with pool.connection() as conn_check:
        res = await conn_check.execute(
            "SELECT 1 FROM pg_database WHERE datname=%(dbname)s",
            params={
                "dbname": settings.db_base,
            },
        )
        db_exists = False
        row = await res.fetchone()
        if row is not None:
            db_exists = row[0]

    if db_exists:
        await drop_db()

    async with pool.connection() as conn_create:
        await conn_create.set_autocommit(True)
        await conn_create.execute(
            f"CREATE DATABASE {settings.db_base};",
        )
    await pool.close()


async def create_tables(connection: AsyncConnection[Any]) -> None:
    """
    Create tables for your database.

    Since psycopg doesn't have migration tool,
    you must create your tables for tests.

    :param connection: connection to database.
    """
    await connection.execute(
        "CREATE TABLE dummy (" "id SERIAL primary key," "name VARCHAR(200)" ");",
    )
    pass  # noqa: WPS420


@pytest.fixture
async def dbpool() -> AsyncGenerator[AsyncConnectionPool, None]:
    """
    Creates database connections pool to test database.

    This connection must be used in tests and for application.

    :yield: database connections pool.
    """
    await create_db()
    pool = AsyncConnectionPool(conninfo=str(settings.db_url))
    await pool.wait()

    async with pool.connection() as create_conn:
        await create_tables(create_conn)

    try:
        yield pool
    finally:
        await pool.close()
        await drop_db()


@pytest.fixture
async def test_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    """
    Creates kafka's producer.

    :yields: kafka's producer.
    """
    app_mock = Mock()
    await init_kafka(app_mock)
    yield app_mock.state.kafka_producer
    await shutdown_kafka(app_mock)


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool, None]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


@pytest.fixture
def fastapi_app(
    dbpool: AsyncConnectionPool,
    fake_redis_pool: ConnectionPool,
    test_kafka_producer: AIOKafkaProducer,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_pool] = lambda: dbpool
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    application.dependency_overrides[get_kafka_producer] = lambda: test_kafka_producer
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

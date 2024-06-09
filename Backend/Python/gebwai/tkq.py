import taskiq_fastapi
from taskiq import InMemoryBroker, ZeroMQBroker

from gebwai.settings import settings

broker = ZeroMQBroker()

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "gebwai.web.application:get_app",
)

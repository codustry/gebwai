# gebwai

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash {"id":"01HZZ08XSY4PS366JPX48QK98D"}
poetry install
poetry run python -m gebwai
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash {"id":"01HZZ08XSY4PS366JPX6AX7MG3"}
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash {"id":"01HZZ08XSY4PS366JPX9V15TTZ"}
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash {"id":"01HZZ08XSY4PS366JPXCY1N74A"}
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash {"id":"01HZZ08XSY4PS366JPXDKBXXGK"}
$ tree "gebwai"
gebwai
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "GEBWAI_" prefix.

For example if you see in your "gebwai/settings.py" a variable named like
`random_parameter`, you should provide the "GEBWAI_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `gebwai.settings.Settings.Config`.

An example of .env file:

```bash {"id":"01HZZ08XSY4PS366JPXHEDWPP1"}
BACKEND__RELOAD="True"
BACKEND__PORT="8000"
BACKEND__ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## OpenTelemetry

If you want to start your project with OpenTelemetry collector
you can add `-f ./deploy/docker-compose.otlp.yml` to your docker command.

Like this:

```bash {"id":"01HZZ08XSY4PS366JPXMK0STR0"}
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.otlp.yml --project-directory . up
```

This command will start OpenTelemetry collector and jaeger.
After sending a requests you can see traces in jaeger's UI
at http://localhost:16686/.

This docker configuration is not supposed to be used in production.
It's only for demo purpose.

You can read more about OpenTelemetry here: https://opentelemetry.io/

## Pre-commit

To install pre-commit simply run inside the shell:

```bash {"id":"01HZZ08XSY4PS366JPXQME6SBE"}
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);

You can read more about pre-commit here: https://pre-commit.com/

## Migrations

If you want to migrate your database, you should run following commands:

```bash {"id":"01HZZ08XSY4PS366JPXTJA5G79"}
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:

```bash {"id":"01HZZ08XSZJ3AC2CRXBKDN1RR0"}
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:

```bash {"id":"01HZZ08XSZJ3AC2CRXBMG9MR36"}
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```

## Running tests

If you want to run it in docker, simply run:

```bash {"id":"01HZZ08XSZJ3AC2CRXBNDB9FH3"}
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.

1. you need to start a database.

I prefer doing it with docker:

```sh {"id":"01HZZ08XSZJ3AC2CRXBQXS6RV5"}
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=gebwai" -e "POSTGRES_USER=gebwai" -e "POSTGRES_DB=gebwai" postgres:13.8-bullseye
```

2. Run the pytest.

```bash {"id":"01HZZ08XSZJ3AC2CRXBVV1X8X6"}
pytest -vv .
```

.PHONY: test integration_test lint format help

help:
	@echo "Available commands:"
	@echo "  make test              - Run unit tests"
	@echo "  make integration_test  - Run integration tests"
	@echo "  make lint              - Run linter"
	@echo "  make format            - Format code"

test:
	uv run --group test pytest tests/unit_tests/

integration_test:
	uv run --group test pytest tests/integration_tests/

lint:
	uv run --group lint ruff check .
	uv run --group lint ruff format --check .

format:
	uv run --group lint ruff check --fix .
	uv run --group lint ruff format .

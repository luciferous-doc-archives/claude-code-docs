.PHONY: fetch format format-check test-unit sync lint help

PYTHONPATH := src

fetch:
	PYTHONPATH=$(PYTHONPATH) uv run src/handlers/fetcher/fetcher.py

format:
	uv run black src/ tests/
	uv run isort src/ tests/

format-check:
	uv run black --check src/ tests/
	uv run isort --check src/ tests/

lint: format-check

test-unit:
	uv run pytest -vv tests/unit

sync:
	uv sync

help:
	@echo "Available targets:"
	@echo "  make fetch        - Run the document fetcher"
	@echo "  make format       - Format code with black and isort"
	@echo "  make format-check - Check code formatting without changes"
	@echo "  make lint         - Alias for format-check"
	@echo "  make test-unit    - Run unit tests"
	@echo "  make sync         - Install dependencies"
	@echo "  make help         - Show this help message"

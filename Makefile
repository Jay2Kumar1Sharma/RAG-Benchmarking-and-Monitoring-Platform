PYTHON := venv/Scripts/python
PIP := venv/Scripts/pip

.PHONY: install dev test lint format migrate revision precommit validate

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	pre-commit install

dev:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check app tests
	$(PYTHON) -m black --check app tests
	$(PYTHON) -m isort --check-only app tests

format:
	$(PYTHON) -m ruff check --fix app tests
	$(PYTHON) -m black app tests
	$(PYTHON) -m isort app tests

migrate:
	$(PYTHON) -m alembic upgrade head

revision:
	$(PYTHON) -m alembic revision --autogenerate -m "$(message)"

precommit:
	$(PYTHON) -m pre_commit run --all-files

validate:
	$(PYTHON) scripts/validate_project.py

# Testing And Validation

Run dependency-light project validation:

```powershell
venv\Scripts\python scripts\validate_project.py
```

Run the full test suite after dependencies are installed:

```powershell
venv\Scripts\python -m pytest
```

Run formatting and lint checks:

```powershell
make lint
```

The validation script checks Python syntax, line lengths, README wording constraints, and Graphify output presence without importing FastAPI, SQLAlchemy, or model libraries.


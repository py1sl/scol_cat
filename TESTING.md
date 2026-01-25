# Testing

This project uses pytest for unit testing.

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=. --cov-report=term-missing --cov-report=html
```

After running with coverage, you can view the HTML coverage report by opening `htmlcov/index.html` in your browser.

### Run Specific Test Files

```bash
# Run only model tests
pytest tests/test_model.py

# Run only controller tests  
pytest tests/test_controller.py
```

### Run Tests in Verbose Mode

```bash
pytest tests/ -v
```

## Test Structure

- `tests/test_model.py` - Tests for the model layer (Stamp and StampDatabase classes)
- `tests/test_controller.py` - Tests for controller business logic
- `tests/conftest.py` - Pytest configuration and shared fixtures

## Continuous Integration

Tests are automatically run on every pull request via GitHub Actions. The workflow:

1. Sets up Python 3.12
2. Installs dependencies
3. Runs all tests with coverage
4. Uploads coverage reports to Codecov
5. Comments coverage statistics on pull requests

See `.github/workflows/tests.yml` for the full workflow configuration.

# python-api-tests

## Preparation

Setup virtualenv
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
pre-commit install
```

## Running tests

Simple run:
```bash
source venv/bin/activate
pytest
```

## Description of modules

- **./api/client.py::Client**
  
    Place, where you can define things such as:
    - API requests
    - Business logic
- **./common/models.py**
    
    Define here models, for requests and responses
- **./common/random.py**

    Here you can define functions for generating some custom
    random data.
- **./conftest.py** && **./tox.ini**

    Here stored the PyTest configuration. You can add your custom
    parameters for tests in `pytest_addoption` and also remember
    to read the [PyTest docs](https://pytest.org/en/stable/example/simple.html#pass-different-values-to-a-test-function-depending-on-command-line-options)
    about it
- **./env.default.yml**

    Place where you could define some standard parameters values
    for PyTest. You can create different envs `./env.master.yml`,
    `./env.develop.yml`, `./env.testing.yml` and then just pass
    them to the pytest `pytest --env=env.testing.yml`
- **./.isort.cfg** && **./.pre-commit-config.yaml** && **./pyproject.toml**
    
    Configuration of pre-commit hooks

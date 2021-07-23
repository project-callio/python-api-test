import pytest
import yaml

from api.client import Client


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default=None, help="YAML file with configuration"
    )
    parser.addoption(
        "--host", action="store", help="Hostname to use in tests"
    )


def get_option(request, name):
    env = request.config.getoption("--env")
    result = request.config.getoption("--{}".format(name))
    if result is None and env:
        with open(env, "r") as yml_file:
            yml = yaml.safe_load(yml_file)
        result = yml.get(name)
    return result


@pytest.fixture(scope="session")
def api(request):
    client = Client(
        host=get_option(request, "host")
    )
    return client

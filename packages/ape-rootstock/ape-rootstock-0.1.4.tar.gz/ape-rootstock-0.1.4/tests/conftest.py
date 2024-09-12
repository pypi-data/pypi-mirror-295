import ape
import pytest


@pytest.fixture
def networks():
    return ape.networks


@pytest.fixture
def accounts():
    return ape.accounts


@pytest.fixture
def rootstock(networks):
    return networks.get_ecosystem("rootstock")


@pytest.fixture(autouse=True)
def eth_tester_provider():
    if not ape.networks.active_provider or ape.networks.provider.name != "test":
        with ape.networks.get_ecosystem("rootstock").local.use_provider("test") as provider:
            yield provider
    else:
        yield ape.networks.provider

from ape import plugins
from ape.api.networks import LOCAL_NETWORK_NAME, ForkedNetworkAPI, NetworkAPI, create_network_type
from ape_node import Node
from ape_test import LocalProvider

from .ecosystem import NETWORKS, Rootstock, RootstockConfig


@plugins.register(plugins.Config)
def config_class():
    return RootstockConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    yield Rootstock


@plugins.register(plugins.NetworkPlugin)
def networks():
    for network_name, network_params in NETWORKS.items():
        yield "rootstock", network_name, create_network_type(*network_params)
        yield "rootstock", f"{network_name}-fork", ForkedNetworkAPI

    # NOTE: This works for local providers, as they get chain_id from themselves
    yield "rootstock", LOCAL_NETWORK_NAME, NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    for network_name in NETWORKS:
        yield "rootstock", network_name, Node

    yield "rootstock", LOCAL_NETWORK_NAME, LocalProvider

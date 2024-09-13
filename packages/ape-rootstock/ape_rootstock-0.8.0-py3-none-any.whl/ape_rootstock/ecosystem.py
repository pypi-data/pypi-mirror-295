from typing import cast

from ape_ethereum.ecosystem import (
    BaseEthereumConfig,
    Ethereum,
    NetworkConfig,
    create_network_config,
)
from ape_ethereum.transactions import TransactionType

NETWORKS = {
    # chain_id, network_id
    "mainnet": (30, 775),
    "testnet": (31, 8100),
}


def _create_config() -> NetworkConfig:
    return create_network_config(
        block_time=30, required_confirmations=1, default_transaction_type=TransactionType.STATIC
    )


class RootstockConfig(BaseEthereumConfig):
    mainnet: NetworkConfig = _create_config()
    testnet: NetworkConfig = _create_config()


class Rootstock(Ethereum):
    fee_token_symbol: str = "RBTC"

    @property
    def config(self) -> RootstockConfig:  # type: ignore
        return cast(RootstockConfig, self.config_manager.get_config("rootstock"))

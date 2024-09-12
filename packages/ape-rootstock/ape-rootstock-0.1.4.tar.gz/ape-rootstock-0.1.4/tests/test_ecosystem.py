import pytest
from ape_ethereum.transactions import TransactionType
from ethpm_types import MethodABI


# NOTE: None because we want to show the default is STATIC
@pytest.mark.parametrize("tx_type", (0, 0, "0x0"))
def test_create_transaction(rootstock, tx_type, eth_tester_provider):
    tx = rootstock.create_transaction(type=tx_type)
    assert tx.type == TransactionType.STATIC.value
    assert tx.gas_limit == eth_tester_provider.max_gas


@pytest.mark.parametrize(
    "tx_type",
    (TransactionType.STATIC.value, TransactionType.STATIC.value),
)
def test_encode_transaction(tx_type, rootstock, eth_tester_provider):
    abi = MethodABI.model_validate(
        {
            "type": "function",
            "name": "fooAndBar",
            "stateMutability": "nonpayable",
            "inputs": [],
            "outputs": [],
        }
    )
    address = "0x2bEE6167f91d10Db23252e03dE039dA6B9047D49"
    actual = rootstock.encode_transaction(address, abi, sender=address, type=tx_type)
    assert actual.gas_limit == eth_tester_provider.max_gas

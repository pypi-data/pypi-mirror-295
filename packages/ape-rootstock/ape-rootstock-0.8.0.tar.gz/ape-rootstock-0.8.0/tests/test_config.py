from ape_ethereum.transactions import TransactionType

from ape_rootstock.ecosystem import RootstockConfig


def test_gas_limit(rootstock):
    assert rootstock.config.local.gas_limit == "max"


def test_default_transaction_type(rootstock):
    assert rootstock.config.mainnet.default_transaction_type == TransactionType.STATIC


def test_mainnet_fork_not_configured():
    obj = RootstockConfig.model_validate({})
    assert obj.mainnet_fork.required_confirmations == 0


def test_mainnet_fork_configured():
    data = {"mainnet_fork": {"required_confirmations": 555}}
    obj = RootstockConfig.model_validate(data)
    assert obj.mainnet_fork.required_confirmations == 555


def test_custom_network():
    data = {"apenet": {"required_confirmations": 333}}
    obj = RootstockConfig.model_validate(data)
    assert obj.apenet.required_confirmations == 333

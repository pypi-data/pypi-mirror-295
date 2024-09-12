from mm_starknet import balance
from mm_starknet.balance import (
    DAI_ADDRESS_MAINNET,
    ETH_ADDRESS_MAINNET,
    USDC_ADDRESS_MAINNET,
    USDT_ADDRESS_MAINNET,
)


def test_get_balance(mainnet_rpc_url, zklend_market_address):
    assert balance.get_balance(mainnet_rpc_url, zklend_market_address, ETH_ADDRESS_MAINNET).unwrap() > 1
    assert balance.get_balance(mainnet_rpc_url, zklend_market_address, DAI_ADDRESS_MAINNET).unwrap() > 1
    assert balance.get_balance(mainnet_rpc_url, zklend_market_address, USDT_ADDRESS_MAINNET).unwrap() > 1
    assert balance.get_balance(mainnet_rpc_url, zklend_market_address, USDC_ADDRESS_MAINNET).unwrap() > 1

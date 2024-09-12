from collections.abc import Sequence
from decimal import Decimal
from typing import cast

from mm_std import Err, Ok, Result, random_choice
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

ETH_ADDRESS_MAINNET = "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"
ETH_DECIMALS = 18
DAI_ADDRESS_MAINNET = "0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3"
DAI_DECIMALS = 18
USDC_ADDRESS_MAINNET = "0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8"
USDC_DECIMALS = 6
USDT_ADDRESS_MAINNET = "0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8"
USDT_DECIMALS = 6


def get_balance(node_urls: str | Sequence[str], address: str, token: str, attempts: int = 3) -> Result[int]:
    res: Result[int] = Err("not_started")
    for _ in range(attempts):
        try:
            url = cast(str, random_choice(node_urls))
            client = FullNodeClient(node_url=url)
            account = Account(
                address=address,
                client=client,
                chain=StarknetChainId.MAINNET,
                key_pair=KeyPair(private_key=654, public_key=321),
            )
            return Ok(account.get_balance_sync(token_address=token))
        except Exception as err:
            res = Err(err)
    return res


def get_balance_decimal(
    node_urls: str | Sequence[str],
    address: str,
    token: str,
    decimals: int,
    round_ndigits: int = 5,
    attempts: int = 3,
) -> Result[Decimal]:
    return get_balance(node_urls, address, token, attempts).and_then(
        lambda o: Ok(round(Decimal(o / 10**decimals), ndigits=round_ndigits)),
    )

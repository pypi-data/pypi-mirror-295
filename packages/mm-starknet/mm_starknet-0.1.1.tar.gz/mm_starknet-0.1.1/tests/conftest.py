import pytest
from mm_std import get_dotenv


@pytest.fixture
def zklend_market_address() -> str:
    return "0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05"


@pytest.fixture
def mainnet_rpc_url() -> str:
    return get_dotenv("MAINNET_URL")

from mm_std import Err, Ok, Result, hr, random_str_choice

from mm_starknet.types import Proxies


def address_to_domain(address: str, timeout: int = 10, proxies: Proxies = None, attempts: int = 3) -> Result[str]:
    url = "https://api.starknet.id/addr_to_domain"
    result = Err("not_started")
    for _ in range(attempts):
        res = hr(url, params={"addr": address}, proxy=random_str_choice(proxies), timeout=timeout)
        data = res.to_dict()
        if res.json and res.json.get("domain"):
            return Ok(res.json.get("domain"), data=data)
        if res.code == 400 and "no domain found" in res.body.lower():
            return Ok("", data)
        result = Err("unknown_response", data)

    return result

from decimal import Decimal

from mm_std import Err, Ok, Result, hr

from mm_aptos.types import Nodes, Proxies
from mm_aptos.utils import random_node, random_proxy


def get_balance(
    nodes: Nodes,
    account_address: str,
    coin_type: str,
    timeout: int = 10,
    proxies: Proxies = None,
    attempts: int = 3,
) -> Result[int]:
    result: Result[int] = Err("not_started")
    for _ in range(attempts):
        url = f"{random_node(nodes)}/accounts/{account_address}/resource/0x1::coin::CoinStore%3C{coin_type}%3E"
        res = hr(url, proxy=random_proxy(proxies), timeout=timeout)
        data = res.to_dict()
        try:
            if isinstance(res, Err):
                result = Err(res.unwrap_err(), data=data)
                continue
            if res.json.get("error_code") == "resource_not_found":
                return Ok(0, data=data)
            return Ok(int(res.json["data"]["coin"]["value"]), data=data)
        except Exception as err:
            result = Err(err, data=data)
    return result


def get_balance_decimal(
    nodes: Nodes,
    account_address: str,
    coin_type: str,
    decimals: int,
    round_ndigits: int = 5,
    timeout: int = 10,
    proxies: Proxies = None,
    attempts: int = 3,
) -> Result[Decimal]:
    return get_balance(nodes, account_address, coin_type, timeout=timeout, proxies=proxies, attempts=attempts).and_then(
        lambda o: Ok(round(Decimal(o / 10**decimals), ndigits=round_ndigits)),
    )

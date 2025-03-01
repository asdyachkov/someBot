# gas_manager.py
import aiohttp
from config import ETHERSCAN_API_KEY, ETHERSCAN_API_URL
from cache_manager import Cache

cache = Cache()

async def fetch_gas_data() -> dict:
    cached = await cache.get("gas_data")
    if cached:
        return cached

    url = f"{ETHERSCAN_API_URL}?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data.get("status") == "1":
                result = data.get("result", {})
                gas_data = {
                    "safe": float(result.get("SafeGasPrice")),
                    "propose": float(result.get("ProposeGasPrice")),
                    "fast": float(result.get("FastGasPrice"))
                }
                await cache.set("gas_data", gas_data, ttl=10)  # кэшируем на 10 секунд
                return gas_data
            else:
                raise Exception("Ошибка получения данных о газе с Etherscan")

async def get_dynamic_gas_price(priority: str = "propose") -> float:
    gas_data = await fetch_gas_data()
    if priority == "fast":
        return gas_data["fast"]
    elif priority == "safe":
        return gas_data["safe"]
    else:
        return gas_data["propose"]

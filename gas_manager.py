import aiohttp
import random
from config import ETHERSCAN_API_KEY, ETHERSCAN_API_URL, IS_TEST_MODE
from cache_manager import Cache
from loguru import logger

cache = Cache()

async def fetch_gas_data() -> dict:
    cached = await cache.get("gas_data")
    if cached:
        return cached

    url = f"{ETHERSCAN_API_URL}?module=gastracker&action=gasoracle&chainid=1&apikey={ETHERSCAN_API_KEY}"
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
                await cache.set("gas_data", gas_data, ttl=30)
                return gas_data
            else:
                raise Exception(f"Ошибка получения данных о газе с Etherscan: {data}")

async def get_dynamic_gas_price(priority: str = "propose") -> float:
    try:
        gas_data = await fetch_gas_data()
    except Exception as e:
        logger.error(f"Ошибка получения данных о газе с Etherscan: {e}")
        if IS_TEST_MODE:
            fallback = random.uniform(20, 40)
            logger.warning(f"Используем fallback динамической цены газа: {fallback:.2f} gwei")
            return fallback
        else:
            fallback = 30.0
            logger.warning(f"Используем fallback динамической цены газа: {fallback:.2f} gwei")
            return fallback

    if priority == "fast":
        return gas_data["fast"]
    elif priority == "safe":
        return gas_data["safe"]
    else:
        return gas_data["propose"]

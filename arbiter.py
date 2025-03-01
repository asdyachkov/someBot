import asyncio
import aiohttp
import random
from loguru import logger
from config import MONITOR_INTERVAL, MIN_SPREAD_HIGH, MIN_SPREAD_LOW, IS_TEST_MODE
from gas_manager import get_dynamic_gas_price
from flashloan import initiate_flashloan
from simulator import simulate_transaction
from metrics import TX_COUNTER, GAS_PRICE_GAUGE, EXCEPTIONS_COUNTER, SIMULATED_TRADES_TOTAL, SIMULATED_PROFIT_GAUGE, \
    SIMULATED_TRADE_DURATION


async def get_market_data() -> tuple:
    async with aiohttp.ClientSession() as session:
        uniswap_url = "https://api.uniswap.org/price/eth_usdt"
        pancakeswap_url = "https://api.pancakeswap.info/api/v2/tokens/eth"
        try:
            uniswap_resp, pancakeswap_resp = await asyncio.gather(
                session.get(uniswap_url),
                session.get(pancakeswap_url)
            )
            uniswap_data = await uniswap_resp.json()
            pancakeswap_data = await pancakeswap_resp.json()
        except Exception as e:
            logger.error(f"Ошибка получения рыночных данных: {e}")
            EXCEPTIONS_COUNTER.inc({"module": "arbiter", "function": "get_market_data"})
            uniswap_data = {"price": 0}
            pancakeswap_data = {"price": 0}
    return uniswap_data, pancakeswap_data


async def calculate_spread(uniswap_price: float, pancakeswap_price: float) -> float:
    if uniswap_price == 0:
        if IS_TEST_MODE:
            uniswap_price = random.uniform(1700, 1900)
            logger.warning(f"Цена Uniswap равна 0, подставляем тестовое значение: {uniswap_price:.2f}")
        else:
            raise ValueError("Цена Uniswap равна 0, деление на ноль")
    if pancakeswap_price == 0 and IS_TEST_MODE:
        pancakeswap_price = random.uniform(1700, 1900)
        logger.warning(f"Цена PancakeSwap равна 0, подставляем тестовое значение: {pancakeswap_price:.2f}")
    spread = (pancakeswap_price - uniswap_price) / uniswap_price
    return spread


async def arbitrage_cycle(private_key: str):
    while True:
        try:
            uniswap_data, pancakeswap_data = await get_market_data()
            uniswap_price = float(uniswap_data.get("price", 0))
            pancakeswap_price = float(pancakeswap_data.get("price", 0))
            try:
                spread = await calculate_spread(uniswap_price, pancakeswap_price)
            except Exception as calc_e:
                logger.error(f"Ошибка расчёта спреда: {calc_e}")
                EXCEPTIONS_COUNTER.inc({"module": "arbiter", "function": "calculate_spread"})
                await asyncio.sleep(MONITOR_INTERVAL)
                continue

            logger.info(f"Текущий спред: {spread * 100:.2f}%")

            # Обновляем динамическую цену газа
            dynamic_gas = await get_dynamic_gas_price("propose")
            GAS_PRICE_GAUGE.set({"module": "arbiter"}, dynamic_gas)

            # Определяем процент сделки
            if spread >= MIN_SPREAD_HIGH:
                trade_percentage = 1.0
            elif spread >= MIN_SPREAD_LOW:
                trade_percentage = 0.6
            else:
                logger.info("Спред ниже минимально допустимого уровня – сделка невыгодна.")
                await asyncio.sleep(MONITOR_INTERVAL)
                continue

            total_capital = 100_000  # Примерная сумма сделки
            trade_amount = total_capital * trade_percentage
            arbitrage_data = {
                "buy_from": "uniswap",
                "sell_on": "pancakeswap",
                "trade_amount": str(trade_amount),
                "expected_spread": str(spread),
            }

            if IS_TEST_MODE:
                logger.info("Запуск симуляции сделки...")
                sim_start = asyncio.get_event_loop().time()
                simulation_payload = {
                    "trade_amount": str(trade_amount),
                    "expected_spread": str(spread),
                    "arbitrage_data": arbitrage_data
                }
                result = await simulate_transaction(simulation_payload)
                sim_duration = asyncio.get_event_loop().time() - sim_start
                SIMULATED_TRADE_DURATION.observe({"module": "arbiter"}, sim_duration)
                if result.get("status") == "success":
                    profit = float(result.get("profit"))
                    logger.info(
                        f"Симуляция успешна: прибыль {profit:.2f}, время исполнения {result.get('execution_time'):.2f} сек.")
                    SIMULATED_TRADES_TOTAL.inc({"status": "success"})
                    SIMULATED_PROFIT_GAUGE.set({"module": "arbiter"}, profit)
                else:
                    logger.error(f"Симуляция неудачна: {result.get('error')}")
                    SIMULATED_TRADES_TOTAL.inc({"status": "failure"})
            else:
                logger.info("Инициирую реальный флэш‑займ для арбитража...")
                tx_hash = await initiate_flashloan("0xUSDTTokenAddress", trade_amount, arbitrage_data, private_key)
                logger.info(f"Флэш‑займ инициирован, tx hash: {tx_hash.hex() if hasattr(tx_hash, 'hex') else tx_hash}")
                TX_COUNTER.inc({})
        except Exception as e:
            logger.error(f"Ошибка в арбитражном цикле: {e}")
            EXCEPTIONS_COUNTER.inc({"module": "arbiter", "function": "arbitrage_cycle"})
        await asyncio.sleep(MONITOR_INTERVAL)

# simulator.py
import asyncio
import random
import time

async def simulate_transaction(simulation_payload: dict) -> dict:
    """
    Симулирует транзакцию, генерируя случайные, но реалистичные результаты.
    simulation_payload: словарь с параметрами сделки, например:
        "trade_amount": сумма сделки,
        "expected_spread": спред,
        "arbitrage_data": дополнительные параметры.
    """
    start_time = time.time()
    # Имитация задержки обработки от 0.5 до 2 секунд
    await asyncio.sleep(random.uniform(0.5, 2.0))
    # Вероятность успеха – 95%
    success_probability = 0.95
    if random.random() > success_probability:
        return {
            "status": "failure",
            "profit": 0,
            "execution_time": time.time() - start_time,
            "error": "Симуляция: сделка не удалась"
        }
    # Прибыль от сделки – случайное значение от 1% до 5% от суммы сделки
    trade_amount = float(simulation_payload.get("trade_amount", 0))
    profit_percentage = random.uniform(0.01, 0.05)
    profit = trade_amount * profit_percentage
    return {
        "status": "success",
        "profit": profit,
        "execution_time": time.time() - start_time,
        "simulated": True,
        "details": simulation_payload
    }

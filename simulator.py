# simulator.py
import asyncio
import random
import time

async def simulate_transaction(simulation_payload: dict) -> dict:
    start_time = time.time()
    # Имитируем задержку обработки от 0.5 до 2 секунд
    await asyncio.sleep(random.uniform(0.5, 2.0))
    success_probability = 0.95
    trade_amount = float(simulation_payload.get("trade_amount", "0"))
    if random.random() > success_probability or trade_amount <= 0:
        return {
            "status": "failure",
            "profit": 0.0,
            "execution_time": time.time() - start_time,
            "error": "Симуляция: сделка не удалась"
        }
    # Генерируем прибыль от сделки как от 1% до 5% от trade_amount
    profit_percentage = random.uniform(0.01, 0.05)
    profit = trade_amount * profit_percentage
    return {
        "status": "success",
        "profit": profit,
        "execution_time": time.time() - start_time,
        "simulated": True,
        "details": simulation_payload
    }

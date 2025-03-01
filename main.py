# main.py
import asyncio
from arbiter import arbitrage_cycle
from logger import setup_logger
from metrics import start_metrics_server
from mempool import monitor_mempool
from loguru import logger
from metrics import EXCEPTIONS_COUNTER

async def safe_task(task_func, *args, **kwargs):
    """Обёртка для безопасного выполнения корутины с перезапуском при ошибках."""
    while True:
        try:
            await task_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Задача {task_func.__name__} завершилась с ошибкой: {e}")
            EXCEPTIONS_COUNTER.inc({"module": "main", "function": task_func.__name__})
            await asyncio.sleep(5)  # задержка перед перезапуском

async def main():
    setup_logger()
    private_key = "YOUR_PRIVATE_KEY"  # Никогда не храните приватный ключ в коде
    target_addresses = [
        "0xUniswapRouterAddress",
        "0xPancakeSwapRouterAddress"
    ]
    asyncio.create_task(start_metrics_server(8001))
    await asyncio.gather(
        safe_task(monitor_mempool, target_addresses),
        safe_task(arbitrage_cycle, private_key)
    )

if __name__ == "__main__":
    asyncio.run(main())

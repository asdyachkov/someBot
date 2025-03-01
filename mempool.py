# mempool.py
import asyncio
from loguru import logger
from metrics import EXCEPTIONS_COUNTER
from web3.providers.websocket import WebsocketProvider
from blockchain import w3_eth

# Флаг, определяющий, поддерживается ли мониторинг мемпула
_mempool_supported = None

async def monitor_mempool(target_addresses: list, polling_interval: float = 1.0):
    global _mempool_supported
    # Если ещё не проверяли поддержку, определяем её
    if _mempool_supported is None:
        if isinstance(w3_eth.provider, WebsocketProvider):
            _mempool_supported = True
        else:
            _mempool_supported = False
            logger.warning("Текущий провайдер не поддерживает подписку на мемпул. Мониторинг мемпула отключён.")
    if not _mempool_supported:
        while True:
            await asyncio.sleep(polling_interval)
        return

    # Если поддерживается, пытаемся создать подписку один раз
    try:
        subscription = await w3_eth.eth.subscribe("newPendingTransactions")
        logger.info("Подписка на новые транзакции установлена через WebSocket")
    except Exception as e:
        logger.error(f"Ошибка при подписке на pending транзакции: {e}")
        EXCEPTIONS_COUNTER.inc({"module": "mempool", "function": "subscribe"})
        while True:
            await asyncio.sleep(polling_interval)
        return

    # Обработка новых транзакций
    while True:
        try:
            new_tx_hashes = await subscription.get_new_entries()
            conflicting_txs = []
            for tx_hash in new_tx_hashes:
                try:
                    tx = await w3_eth.eth.get_transaction(tx_hash)
                    if tx is None:
                        continue
                    if tx.get("to") in target_addresses:
                        conflicting_txs.append(tx_hash)
                except Exception as e:
                    logger.error(f"Ошибка при получении транзакции {tx_hash}: {e}")
                    EXCEPTIONS_COUNTER.inc({"module": "mempool", "function": "get_transaction"})
            if conflicting_txs:
                logger.info(f"Найдено {len(conflicting_txs)} конфликтующих транзакций в мемпуле")
            await asyncio.sleep(polling_interval)
        except Exception as inner_e:
            logger.error(f"Ошибка при обработке подписки мемпула: {inner_e}")
            EXCEPTIONS_COUNTER.inc({"module": "mempool", "function": "subscription_loop"})
            await asyncio.sleep(polling_interval)

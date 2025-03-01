# blockchain.py
import asyncio
from web3 import AsyncWeb3
from web3.providers.async_rpc import AsyncHTTPProvider
from config import ETH_RPC_URL, BSC_RPC_URL, POLYGON_RPC_URL

# Инициализация асинхронных клиентов для каждого блокчейна
w3_eth = AsyncWeb3(AsyncHTTPProvider(ETH_RPC_URL))
w3_bsc = AsyncWeb3(AsyncHTTPProvider(BSC_RPC_URL))
w3_polygon = AsyncWeb3(AsyncHTTPProvider(POLYGON_RPC_URL))

async def get_gas_price(w3: AsyncWeb3) -> int:
    return await w3.eth.gas_price

async def send_transaction(w3: AsyncWeb3, tx: dict, private_key: str):
    account = w3.eth.account.from_key(private_key)
    tx['nonce'] = await w3.eth.get_transaction_count(account.address)
    from gas_manager import get_dynamic_gas_price
    dynamic_gas = await get_dynamic_gas_price("propose")
    tx['gasPrice'] = int(dynamic_gas * (10**9))
    signed_tx = account.sign_transaction(tx)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash

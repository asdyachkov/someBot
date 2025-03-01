# flashloan.py
import asyncio
from blockchain import w3_eth, send_transaction
from config import AAVE_LENDING_POOL_ADDRESS

# Пример ABI для метода flashLoan – замените на реальный ABI
AAVE_FLASHLOAN_ABI = [
    # Здесь разместите реальный ABI метода flashLoan
]

async def initiate_flashloan(asset_address: str, amount: float, arbitrage_data: dict, private_key: str):
    contract = w3_eth.eth.contract(address=AAVE_LENDING_POOL_ADDRESS, abi=AAVE_FLASHLOAN_ABI)
    tx = contract.functions.flashLoan(
        asset_address,
        int(amount),
        arbitrage_data
    ).buildTransaction({
        'from': (await w3_eth.eth.account.create()).address,
        'gas': 8000000,
    })
    tx_hash = await send_transaction(w3_eth, tx, private_key)
    return tx_hash

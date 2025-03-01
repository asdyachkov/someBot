# risk_management.py
from config import MAX_SLIPPAGE, CRITICAL_POOL_LIQUIDITY

def calculate_amount_out_min(expected_amount: float, slippage: float = MAX_SLIPPAGE) -> float:
    """
    Рассчитывает минимальное количество токенов с учётом проскальзывания.
    """
    return expected_amount * (1 - slippage)

def is_liquidity_sufficient(pool_liquidity: float) -> bool:
    """
    Проверяет, достаточно ли ликвидности в пуле для безопасной сделки.
    """
    return pool_liquidity >= CRITICAL_POOL_LIQUIDITY

def check_gas_price(network: str, current_gas: float) -> bool:
    """
    Проверяет, что текущая цена газа находится в допустимых пределах.
    """
    from config import GAS_FEE_ETH_THRESHOLD, GAS_FEE_BSC_POLYGON_THRESHOLD
    if network.lower() == "ethereum":
        return current_gas < GAS_FEE_ETH_THRESHOLD
    else:
        return current_gas < GAS_FEE_BSC_POLYGON_THRESHOLD

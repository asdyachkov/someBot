# config.py
import os

# RPC URL для разных блокчейнов
ETH_RPC_URL = os.getenv("ETH_RPC_URL", "https://mainnet.infura.io/v3/2e94ddd5dee14dcbb5cdab190fbede1c")
BSC_RPC_URL = os.getenv("BSC_RPC_URL", "https://bsc-dataseed.binance.org/")
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com/")

# Адреса роутеров DEX (пример, реальные адреса заменить)
UNISWAP_ROUTER_ADDRESS = os.getenv("UNISWAP_ROUTER_ADDRESS", "0xUniswapRouterAddress")
PANCAKESWAP_ROUTER_ADDRESS = os.getenv("PANCAKESWAP_ROUTER_ADDRESS", "0xPancakeSwapRouterAddress")

# Адреса смарт-контрактов для флэш‑займов
AAVE_LENDING_POOL_ADDRESS = os.getenv("AAVE_LENDING_POOL_ADDRESS", "0xAaveLendingPoolAddress")
DYDX_ADDRESS = os.getenv("DYDX_ADDRESS", "0xDyDxAddress")

# Пороговые значения для арбитража
MIN_SPREAD_HIGH = 0.05  # 5% – использовать весь кредитный лимит
MIN_SPREAD_LOW = 0.03   # 3% – использовать 50-70% от лимита

# Настройки газа
GAS_FEE_ETH_THRESHOLD = 30  # gwei для Ethereum
GAS_FEE_BSC_POLYGON_THRESHOLD = 5  # gwei для BSC/Polygon

# Комиссии мостов и флэш‑займов
BRIDGE_FEE_MULTICHAIN = 0.001   # 0.1%
BRIDGE_FEE_CBRIDGE = 0.0005     # 0.05%
FLASHLOAN_FEE = 0.0009          # 0.09%

# Ликвидность пулов (в долларах)
MIN_POOL_LIQUIDITY = 5_000_000   # для минимизации проскальзывания
CRITICAL_POOL_LIQUIDITY = 1_000_000  # критический порог

# Лимит проскальзывания (amountOutMin)
MAX_SLIPPAGE = 0.05  # 5%

# Таймауты (в секундах)
TX_TIMEOUT = 300  # 5 минут для перевода между сетями
SMART_CONTRACT_DEADLINE = 600  # 10 минут

# Интервал мониторинга рынка (секунды)
MONITOR_INTERVAL = 3

# API-ключи и эндпоинты
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "your_etherscan_api_key")
ETHERSCAN_API_URL = "https://api.etherscan.io/v2/api"

TENDERLY_ACCOUNT_ID = os.getenv("TENDERLY_ACCOUNT_ID", "your_account_id")
TENDERLY_PROJECT_SLUG = os.getenv("TENDERLY_PROJECT_SLUG", "your_project_slug")
TENDERLY_ACCESS_KEY = os.getenv("TENDERLY_ACCESS_KEY", "your_access_key")

# Флаг тестового режима. При True бот работает в симуляционном режиме,
# заменяя реальные вызовы случайными, но реалистичными ответами.
IS_TEST_MODE = True

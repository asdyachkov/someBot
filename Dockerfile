# Dockerfile
FROM python:3.13-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Установка Poetry
RUN pip install poetry

# Установка зависимостей проекта
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Установка переменных окружения (замените значения на реальные)
ENV ETH_RPC_URL=https://mainnet.infura.io/v3/2e94ddd5dee14dcbb5cdab190fbede1c
ENV BSC_RPC_URL=https://bsc-dataseed.binance.org/
ENV POLYGON_RPC_URL=https://polygon-rpc.com/
ENV ETHERSCAN_API_KEY=your_etherscan_api_key
ENV TENDERLY_ACCOUNT_ID=your_account_id
ENV TENDERLY_PROJECT_SLUG=your_project_slug
ENV TENDERLY_ACCESS_KEY=your_access_key

CMD ["python", "main.py"]

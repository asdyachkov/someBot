FROM python:3.13-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей отдельно для кэширования
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копирование оставшихся файлов проекта
COPY . /app

CMD ["python", "main.py"]

from aioprometheus import Counter, Gauge, Summary, Registry, render
from aiohttp import web

# Создаем реестр для хранения метрик
registry = Registry()

# Определяем метрики
REQUEST_TIME = Summary("request_processing_seconds", "Время обработки запроса")
TX_COUNTER = Counter("transactions_total", "Общее количество обработанных транзакций")
GAS_PRICE_GAUGE = Gauge("current_gas_price", "Текущая динамическая цена газа")
EXCEPTIONS_COUNTER = Counter("exceptions_total", "Общее количество исключений")
SIMULATED_TRADES_TOTAL = Counter("simulated_trades_total", "Количество симулированных сделок")
SIMULATED_PROFIT_GAUGE = Gauge("simulated_profit", "Прибыль по симуляциям")
SIMULATED_TRADE_DURATION = Summary("simulated_trade_duration_seconds", "Время симуляции сделки")

# Регистрируем метрики в реестре
registry.register(REQUEST_TIME)
registry.register(TX_COUNTER)
registry.register(GAS_PRICE_GAUGE)
registry.register(EXCEPTIONS_COUNTER)
registry.register(SIMULATED_TRADES_TOTAL)
registry.register(SIMULATED_PROFIT_GAUGE)
registry.register(SIMULATED_TRADE_DURATION)


# Обработчик запроса метрик
async def metrics_handler(request):
    accepts_headers = request.headers.getall('Accept', ['*/*'])
    metrics_data, content_type = render(registry, accepts_headers=accepts_headers)

    # Ensure content_type is a string
    if isinstance(content_type, dict):
        content_type = content_type.get('Content-Type', 'text/plain')

    # Remove charset if present
    content_type = content_type.split(';')[0]

    # Decode metrics_data if necessary
    metrics_text = metrics_data.decode('utf-8') if isinstance(metrics_data, bytes) else metrics_data

    return web.Response(text=metrics_text, content_type=content_type)


# Функция для запуска сервера метрик
async def start_metrics_server(port: int = 8001):
    app = web.Application()
    app.router.add_get("/metrics", metrics_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Metrics server started on port {port}")
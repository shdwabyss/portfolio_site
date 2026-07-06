# shadowabyss.dev

Персональный сайт на FastAPI с темным минималистичным дизайном. Русская и английская версии, reverse proxy через Caddy с автоматическими SSL-сертификатами.

Стек: FastAPI, Jinja2, Caddy, Docker

## Что внутри

Одностраничник с переключением языков через query-параметр. Контент загружается из JSON, шаблоны на Jinja2. Все стили — чистый CSS с кастомными переменными и анимациями появления. Карточки с полупрозрачным фоном и grain-эффектом для текстуры.

Middleware логирует все запросы с временем обработки. Кастомные страницы для 404 и 500 ошибок.

Caddy раздает SSL и проксирует на FastAPI-бэкенд. Docker Compose поднимает всё одной командой.

## Запуск

```bash
docker compose up -d
```

Сайт станет доступен на 80/443 портах. Caddy сам получит сертификаты Let's Encrypt для домена из Caddyfile.

## Локальная разработка

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Открыть http://localhost:8000

Переключить язык: http://localhost:8000?lang=en

## Структура

```
app/
├── main.py              # FastAPI приложение
├── core/
│   └── logging.py       # Настройка логирования
├── data/
│   └── locale.json      # Тексты для RU/EN
├── templates/
│   ├── base.html        # Базовый шаблон
│   ├── index.html       # Главная страница
│   ├── 404.html
│   └── 500.html
└── static/
    ├── css/style.css    # Все стили
    └── js/main.js       # Минимальная интерактивность

caddy/
└── Caddyfile            # Конфиг reverse proxy
```

## Кастомизация

Тексты: `app/data/locale.json`  
Цветовая схема: CSS-переменные в `:root` в `style.css`  
Домен: `caddy/Caddyfile` (строка 1)

## Лицензия

MIT — делайте что хотите

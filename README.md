# wallet_service

REST API сервис управления кошельками с операциями пополнения и списания баланса.

Описание

Приложение реализует REST API для работы с кошельками:

- Выполнение операций: пополнение (DEPOSIT) и снятие (WITHDRAW)
- Получение текущего баланса кошелька

Проект построен на FastAPI с асинхронным доступом к PostgreSQL через SQLAlchemy и asyncpg. Запуск в Docker с docker-compose.

Технологии:

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x (асинхронный режим)
- Alembic (миграции)
- Docker & docker-compose
- pytest и pytest-asyncio (тесты)

Установка и запуск

1. Клонирование репозитория

```bash
git clone https://github.com/MrRuzal/wallet_service.git
cd wallet_service
```

2. Создайте файл .env на основе .env.example и настройте параметры подключения к БД

```env
POSTGRES_USER=wallet_user
POSTGRES_PASSWORD=wallet_password
POSTGRES_DB=wallet_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. Запуск через Docker Compose

```bash
docker-compose up --build
```


---

## Миграции

Alembic автоматически применяет миграции при старте контейнера через команду:

```sh
alembic upgrade head
```

Эта команда уже добавлена в `entrypoint.sh`, поэтому **никакие действия вручную выполнять не требуется**.

---

## Тестирование

Для запуска тестов используется `pytest`. Перед запуском убедитесь, что зависимости установлены и проект не требует подключения к реальной БД (используется мок).

```bash
pytest
```

---

## Эндпоинты

- `POST /api/v1/wallets/{wallet_id}/operation` — выполнить операцию пополнения или списания.
- `GET /api/v1/wallets/{wallet_id}` — получить текущий баланс кошелька.

Формат тела запроса для `POST`:

```json
{
  "operation_type": "DEPOSIT", // или "WITHDRAW"
  "amount": 1000
}
```

---

## Структура проекта

- `app/api/v1` — роуты и схемы
- `app/usecases` — бизнес-логика
- `app/infrastructure` — работа с базой данных
- `app/common` — вспомогательные утилиты (логгер и т.п.)

---

## Автор

Разработано в рамках тестового задания. Автор: [MrRuzal](https://github.com/MrRuzal)


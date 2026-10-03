# Change

Бэкенд-приложение для отслеживания личных целей, построенное на **FastAPI**.

Пользователь создаёт **цели (goals)**, разбивает их на **задачи (tasks)** и ведёт **посты (posts)** с заметками о прогрессе.

## Технологии

| Категория | Технология |
|---|---|
| Язык | Python 3.12 |
| Фреймворк | FastAPI |
| База данных | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async, asyncpg) |
| Миграции | Alembic |
| Управление зависимостями | Poetry |
| Тестирование | pytest |
| Линтер | Ruff |
| Статический анализ типов | mypy |
| Контейнеризация | Docker, Docker Compose |

## Структура проекта

```
├── src/
│   ├── main.py            # Точка входа FastAPI-приложения
│   ├── backend/           # Конфигурация (настройки, подключение к БД)
│   ├── models/            # SQLAlchemy-модели (User, Goal, Task, Post)
│   ├── schemas/           # Pydantic-схемы
│   └── enums/             # Перечисления (статусы целей и т.д.)
├── migrations/            # Миграции Alembic
├── tests/                 # Тесты (unit)
├── alembic.ini            # Конфигурация Alembic
├── Dockerfile
├── docker-compose.yaml    # postgres + миграции + приложение
└── pyproject.toml
```

## Быстрый запуск через Docker

Самый простой способ — запустить всё через Docker Compose (PostgreSQL, применение миграций и приложение поднимутся автоматически):

```bash
docker compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

## Настройки для локального запуска

### 1. Предварительные требования

- Python >= 3.12
- [Poetry](https://python-poetry.org/docs/#installation)
- PostgreSQL 16 (локально или через `docker compose up postgres`)

### 2. Установка зависимостей

```bash
poetry install
```

Команда `poetry install` ставит **все** зависимости: и основные из `[project.dependencies]` (fastapi, sqlalchemy и т.д.), и группу разработки `[dependency-groups] dev` (pytest, ruff, mypy).

Для проекта рекомендуется использовать poetry>=2.0 версии. Для активации виртуального окружения можно воспользоваться командой:

```bash
poetry env activate
```

Данная команда выведет путь до виртуального окружения с командой `source`. Эту команду нужно целиком скопировать и вставить в терминал. После чего виртуальное окружение будет активировано.

### 3. Переменные окружения

Создайте файл `.env` в корне проекта (он необходим для хранения security-переменных для локальной разработки):

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres
```

### 4. Применение миграций

```bash
alembic upgrade head
```

### 5. Запуск приложения

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Документация API

После запуска приложения интерактивная документация доступна по адресам:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Вклад в проект: тесты, стиль, типы

Перед отправкой изменений, пожалуйста, убедитесь, что код покрыт тестами и проходит все проверки:

```bash
pytest -vvv          # тесты
ruff check           # проверка стилистики кода
ruff check --fix     # автоматическое исправления большинства стилистических ошибок
mypy                 # статическая проверка типов
```

Тесты находятся в `tests/` и делятся на две категории:
- `integration` - интеграционные тесты, проверяющие взаимодействие отдельных модулей
-  `unit` - юнит-тесты, проверяющие отдельные методы и функционал в изоляции

## Полезные команды Alembic

```bash
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
alembic downgrade -1
alembic current
```

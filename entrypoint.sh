#!/bin/sh
set -e  # Завершает скрипт при ошибке

# Запускаем миграции Alembic
alembic upgrade head

# Запускаем FastAPI
exec uvicorn main:app --host 0.0.0.0 --port 8000

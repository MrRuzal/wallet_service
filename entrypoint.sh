#!/bin/sh
alembic upgrade head
exec uvicorn app.application:app --host 0.0.0.0 --port 8000 --reload
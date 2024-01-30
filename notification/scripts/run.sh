#!/bin/sh
set -e

cd /opt/project/app
alembic upgrade head
uvicorn app_main:app --host 0.0.0.0 --port 5000
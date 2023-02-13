# Project

# Запуск приложения

0. В коренной директории создать файл `.env` со следующими полями:

```
PORT=
HOST=
DB_URL=
USERNAME=
PASSWORD=
JWT_SECRET=
JWT_ALGORITHM=
JWT_EXPIRES_SEC=
```

1. В терминале из коренной директории проекта запустить следующие команды

- с использованием poetry:

```
poetry install
cd project
poetry run alembic upgrade head
poetry run python main.py
```

- без использования poetry:

```
pip install fastapi sqlalchemy pydantic uvicorn python-dotenv psycopg2-binary alembic passlib python-jose python-multipart
cd project
alembic upgrade head
python main.py
```

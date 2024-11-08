FROM python:3.10

WORKDIR /app

RUN pip install pymysql &&  \
    pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry lock --no-update &&  \
    poetry install --only main --no-root

COPY . .

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

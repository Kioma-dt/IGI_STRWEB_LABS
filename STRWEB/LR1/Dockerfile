FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq5 postgresql-client netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/
RUN pip install -r requirements/prod.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

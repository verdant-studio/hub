FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Accept build-time argument
ARG CLIENT_URL

# Make it available as an env var
ENV CLIENT_URL=${CLIENT_URL}

EXPOSE 2000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--workers", "1", "--bind", "0.0.0.0:2000"]


FROM python:3.9-slim

WORKDIR /app


COPY cleaner.py .

ENTRYPOINT ["python", "cleaner.py"]
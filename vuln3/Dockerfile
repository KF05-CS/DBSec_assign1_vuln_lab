FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install flask psycopg2-binary

EXPOSE 5000

CMD ["python", "src/app.py"]
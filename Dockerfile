# docker build -t blk-hacking-ind-gaurav-surolia .

# Using python:3.11-slim because it provides small size, security patches, and Linux base
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5477

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5477"]
FROM python:3-slim
WORKDIR /app

COPY src/ .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN chmod +x /app/ha-cli.py && ln -s /app/ha-cli.py /usr/local/bin/ha

CMD ["python3", "/app/app_service.py"]

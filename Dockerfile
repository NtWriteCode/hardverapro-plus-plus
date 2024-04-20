FROM python:3-slim
WORKDIR /app

COPY src/ .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN chmod +x /app/app_cli.py && ln -s /app/app_cli.py /usr/local/bin/ha

CMD ["python3", "-m hardverapro_pp"]

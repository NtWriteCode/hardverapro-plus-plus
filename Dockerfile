FROM python:3-slim
WORKDIR /app

COPY hardverapro_pp/ .
COPY cli.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN chmod +x /app/cli.py && ln -s /app/cli.py /usr/local/bin/ha

CMD ["python3", "-m hardverapro_pp"]

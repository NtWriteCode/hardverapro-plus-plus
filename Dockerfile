FROM python:3-slim

WORKDIR /project

COPY hardverapro_pp/ /project/hardverapro_pp
COPY cli.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN chmod +x /project/cli.py && ln -s /project/cli.py /usr/local/bin/ha

CMD ["python3", "-m hardverapro_pp"]

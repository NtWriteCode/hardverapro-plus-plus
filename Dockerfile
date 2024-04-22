FROM python:3-slim

WORKDIR /project
HEALTHCHECK CMD curl -f http://localhost:5001

RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY hardverapro_pp/ /project/hardverapro_pp
COPY cli.py .
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x /project/cli.py && ln -s /project/cli.py /usr/local/bin/ha

CMD ["python3", "-m", "hardverapro_pp"]

FROM python:3.10

WORKDIR /opt/app

COPY ./src/data/requirements.txt ./data/requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade -r data/requirements.txt

COPY ./src/ .

CMD ["python3", "bot.py"]

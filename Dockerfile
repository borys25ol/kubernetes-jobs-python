FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

ADD requirements.txt ./

RUN pip install --upgrade -r /app/requirements.txt

ADD main/utils.py main/shuffler.py main/log.py ./

ENTRYPOINT ["python3", "shuffler.py"]

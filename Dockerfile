# syntax=docker/dockerfile:1

FROM python:3.10.1

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]
CMD ["main.py"]
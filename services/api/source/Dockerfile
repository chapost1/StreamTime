FROM python:3.11.0

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt
COPY ./code/ /code/

RUN pytest

ARG APP_PORT=80
ENV APP_PORT=$APP_PORT
EXPOSE $APP_PORT

ENTRYPOINT ["python", "entrypoint.py"]
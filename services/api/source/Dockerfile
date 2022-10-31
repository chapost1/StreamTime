FROM python:3.11.0
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt
COPY ./code/ /code/

EXPOSE 80

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "80"]
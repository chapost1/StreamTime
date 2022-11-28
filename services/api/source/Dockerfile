FROM python:3.11.0
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt
COPY ./code/ /code/

EXPOSE 80

CMD ["python", "index.py"]
FROM python:3.11.0
WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt
COPY ./src/ /src/

EXPOSE 8080

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8080"]
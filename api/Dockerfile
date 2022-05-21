FROM python:3.9.13

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install -r requeriments.txt &&\
    chmod +x api.py

CMD ["uvicorn", "api:app", "--host=0.0.0.0", "--reload"]
FROM python:3.9.13

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install -r requeriments.txt &&\
    chmod +x main.py

CMD [ "bash", "-c", "python main.py --destination_db=${destination_db} --origin_db=${origin_db}" ]
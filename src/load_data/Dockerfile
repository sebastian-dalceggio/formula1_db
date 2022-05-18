FROM python

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install -r requeriments.txt &&\
    chmod +x main.py

CMD [ "python", "/home/app/main.py" ]
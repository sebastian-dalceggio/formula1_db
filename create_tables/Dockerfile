FROM bash:5.1.16

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN apk add --update postgresql &&\
    apk add --update postgresql-contrib &&\
    chmod +x ./create_tables.sh &&\
    chmod +x ./wait_for_postgres.sh

CMD ["bash", "./wait_for_postgres.sh", "bash", "create_tables.sh"]
FROM bash:5.1.16

ENV USER=admin
ENV PASSWORD=pass
ENV HOST=postgres
ENV DATABASE=formula1_db

RUN mkdir -p /home/app

COPY . /home/app

RUN cd ./home/app && ls

RUN apk add --update postgresql &&\
    apk add --update postgresql-contrib &&\
    chmod +x /home/app/create_tables.sh

CMD [ "bash", "/home/app/create_tables.sh" ]
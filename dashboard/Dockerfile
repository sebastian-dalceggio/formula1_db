FROM python:3.9.13

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install -r requeriments.txt &&\
    chmod +x main.py &&\
    chmod +x dashboard_functions.py

CMD streamlit run main.py ${api_url}
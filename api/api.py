from this import d
from sqlalchemy import create_engine
import os
from fastapi import FastAPI
import json
from classes.database import Database

with open("config.json", "r") as f:
    config = json.load(f)
    db = config["database"]
    database = Database(db)
    directory = config["directory"]

app = FastAPI()

@app.get("/get-table/{table}")
def get_table(table):
    f = os.path.join(directory, table + ".sql")
    with open(f) as file:
        query = file.read()
        data = database.download_data(query)
    database.dispose()
    return {"data": data.to_json()}
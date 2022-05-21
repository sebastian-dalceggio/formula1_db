from h11 import Data
import uvicorn
from classes.database import Database
from api import create_api
import json

# app = None

def main(database=None):

    with open("config.json", "r") as f:
        config = json.load(f)
    
    if database == None:
        database = config["database"]

    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=False, type=str, default=None)
    parsed_args = parser.parse_args()
    main(database=parsed_args.database)
    

    

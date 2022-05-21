from classes.load_data import LoadData
import json

def main(destination_db=None, origin_db=None):
    
    with open("tables.json", "r") as f:
        tables = json.load(f)
    
    with open("config.json", "r") as f:
        config = json.load(f)

    if destination_db is None:
        destination_db = config["destination_db"]
        
    if origin_db is None:
        origin_db = config["origin_db"]

    loader = LoadData(destination_db, origin_db)
    loader.load_data(tables)
    loader.dispose()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--destination_db", required=False, type=str, default=None)
    parser.add_argument("--origin_db", required=False, type=str, default=None)
    parsed_args = parser.parse_args()
    main(parsed_args.destination_db, parsed_args.origin_db)
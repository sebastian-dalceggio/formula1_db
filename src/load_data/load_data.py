from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import json
import time

def load_data(destination_db, origin_db, tables):

    destination_engine = create_engine(destination_db)
    origin_engine = create_engine(origin_db)

    for table in tables:
        table_name = table["name"]
        data = pd.read_sql(f"SELECT * FROM {table_name};", origin_engine)

        # All tables in postgresql are lower case
        data.columns = [x.lower() for x in data.columns]

        if "time_columns" in table:
            for column in table["time_columns"]:
                data[column] = pd.to_datetime(data[column], errors='coerce').dt.time

        if "date_columns" in table:
            for column in table["date_columns"]:
                data[column] = pd.to_datetime(data[column])

        if "drop_columns" in table:
            for column in table["drop_columns"]:
                data.drop([column], axis=1, inplace=True)

        if "delete_record" in table:
            for record in table["delete_record"]:
                data.loc[data[record["column_search"]] == record["value"], record["column_to_delete"]] = None
                
        data.replace("", None, inplace=True)
        data.to_sql(table_name, destination_engine, if_exists="append", index=False)

    destination_engine.dispose()
    origin_engine.dispose()
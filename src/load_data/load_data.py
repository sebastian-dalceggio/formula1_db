from sqlalchemy import create_engine, inspect
import pandas as pd
import time
from functools import wraps

def retry(tries=100, time_sleep=2):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kargs):
            attempts = tries
            while True:
                attempts -= 1
                try:
                    return func(*args, **kargs)
                except Exception as e:
                    if attempts:
                        time.sleep(time_sleep)
                        continue
                    else:
                        raise e
        return wrapper
    return inner

class Database():
    TRIES = 100
    TIME_SLEEP = 1
    def __init__(self, db, tries=100, time_sleep=2):
        self.db = db
        self.engine = self.create_engine_(self.db)
        self.inspector = self.create_inspector_(self.engine)

    @retry(tries=TRIES, time_sleep=TIME_SLEEP)
    def create_engine_(self, db):
        return create_engine(db)
    
    @retry(tries=TRIES, time_sleep=TIME_SLEEP)
    def create_inspector_(self, engine):
        return inspect(engine)
    
    def change_db(self, db):
        self.__init__(db)
    
    def dispose(self):
        self.engine.dispose()
    
    @retry(tries=TRIES, time_sleep=TIME_SLEEP)
    def download_data(self, query):
        return pd.read_sql(query, self.engine)
    
    @retry(tries=TRIES, time_sleep=TIME_SLEEP)
    def load_data(self, data, table_name, if_exists="append"):
        data.to_sql(table_name, self.engine, if_exists=if_exists, index=False)

class LoadData():
    def __init__(self, destination_string, origin_string, retries=100, time_sleep=2):
        self.destination = Database(destination_string)
        self.origin = Database(origin_string)
        self.retries = retries
        self.time_sleep = time_sleep

    def change_origin(self, db):
        self.origin.change_db(db)

    def change_destination(self, db):
        self.destination.change_db(db)

    def dispose(self):
        self.destination.dispose()
        self.origin.dispose()

    def load_data(self, tables):
        for table in tables:
            table_name = table["name"]
            data = self.origin.download_data(f"SELECT * FROM {table_name};")

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

            self.destination.load_data(data, table_name)
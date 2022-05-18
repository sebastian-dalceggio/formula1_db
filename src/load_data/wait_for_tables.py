import pandas as pd
from sqlalchemy import create_engine, inspect
import time

def wait_for_tables(destination_db, tables):

    destination_engine = create_engine(destination_db)
    destination_inspector = inspect(destination_engine)
    for table in tables:
        table_name = table["name"]
        while not destination_inspector.has_table(table_name):
            try:
                if destination_inspector.has_table(table_name):
                    break
            except:
                time.sleep(10)
            pass
        
    destination_engine.dispose()

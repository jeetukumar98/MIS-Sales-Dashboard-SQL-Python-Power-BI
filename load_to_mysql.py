
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DB = os.getenv("DB_NAME")

engine = create_engine(url)
# order important hai (foreign keys)
for table in ["customers", "products", "sales", "expenses"]:
    df = pd.read_csv(f"{table}.csv")
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"{table}: {len(df)} rows loaded")

print("Done!")

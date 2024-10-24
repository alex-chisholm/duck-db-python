import duckdb 
import polars as pl
import os

db_name = 'my_db'
md_token = os.getenv('MD_TOKEN')

conn = duckdb.connect(f"md:{db_name}")

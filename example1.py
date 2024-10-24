import duckdb
import polars as pl

duckdb.sql("SELECT 42").show()


r1 = duckdb.sql("SELECT 42 AS i")
duckdb.sql("SELECT i * 2 AS k FROM r1").show()



import duckdb

duckdb.read_csv("bitcoin.csv")                # read a CSV file into a Relation

duckdb.sql("SELECT * FROM 'bitcoin.csv WHERE Open > 20000'")     # directly query a CSV file


# from Polars



polars_df = pl.read_csv("bitcoin.csv")
duckdb.sql("SELECT * FROM polars_df")


# write to polars df
newdf = duckdb.sql("SELECT 42").pl()  


# write to disk

duckdb.sql("SELECT 42").write_csv("out.csv")  
duckdb.sql("SELECT 42").write_parquet("out.parquet") # Write to a Parquet file


# in memory db

con = duckdb.connect()
con.sql("SELECT 42 AS x").show()


# persistent storage

# create a connection to a file called 'file.db'
con = duckdb.connect("file.db")
# create a table and load data into it
con.sql("CREATE TABLE test (i INTEGER)")
con.sql("INSERT INTO test VALUES (42)")
# query the table
con.table("test").show()
# explicitly close the connection
con.close()
# Note: connections also closed implicitly when they go out of scope





# store df to db

# Load CSV into DuckDB
con = duckdb.connect()  # create an in-memory connection

# Replace 'your_file.csv' with the path to your CSV
df = con.execute("SELECT * FROM 'bitcoin.csv'").pl()

# Optionally, you can manipulate or analyze your data here

# Save the dataframe to a DuckDB .db file
con = duckdb.connect('bitcoin.db')  # open/create a .db file
con.execute("CREATE TABLE IF NOT EXISTS bc AS SELECT * FROM df")

# To verify, you can query the data back
result = con.execute("SELECT * FROM bc").fetch_df() # no fetch.pl() yet and defaults to pandas

print(result)
type(result)

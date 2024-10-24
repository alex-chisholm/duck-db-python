import streamlit as st
from datetime import datetime
import duckdb
import os
from dotenv import load_dotenv


# Connect to DuckDB in memory
con = duckdb.connect(":memory:")

# Install and load the MotherDuck extension
con.execute("INSTALL motherduck")
con.execute("LOAD motherduck")

# Get and verify token
token = os.environ.get('MD_TOKEN')
print(token)


# Set the token and connect to MotherDuck
con.execute(f"SET motherduck_token='{token}'")
con.execute("PRAGMA md_connect")

# Create guestbook table if it doesn't exist
con.execute("""
CREATE TABLE IF NOT EXISTS my_db.guestbook (
    name VARCHAR,
    comment VARCHAR,
    datetime TIMESTAMP
)
""")

# Function to get all entries
def get_entries():
    return con.execute("""
        SELECT name, comment, datetime 
        FROM my_db.guestbook 
        ORDER BY datetime DESC
    """).fetchall()

# Function to insert an entry
def add_entry(name, comment):
    con.execute("""
        INSERT INTO my_db.guestbook (name, comment, datetime)
        VALUES (?, ?, ?)
    """, [name, comment, datetime.now()])

# Function to delete all entries
def delete_all_entries():
    con.execute("DELETE FROM my_db.guestbook")

# Streamlit app
st.sidebar.header("Sign the Guestbook")
name = st.sidebar.text_input("Your Name", placeholder="Enter your name")
comment = st.sidebar.text_area("Your Comment", placeholder="Leave a message")
if st.sidebar.button("Submit"):
    if name and comment:
        add_entry(name, comment)
        st.sidebar.success("Your entry has been added!")
    else:
        st.sidebar.error("Please provide both name and comment.")

if st.sidebar.button("Delete All Entries"):
    if st.sidebar.button("Confirm Deletion"):
        delete_all_entries()
        st.sidebar.success("All entries have been deleted!")

# Display the guestbook entries
st.header("Connect Cloud Guestbook")
entries = get_entries()

if not entries:
    st.write("No entries yet. Be the first to sign!")
else:
    for entry in entries:
        st.subheader(entry[0])  # name
        st.write(entry[1])      # comment
        st.write(f"_Posted on {entry[2]}_", unsafe_allow_html=True)
        st.write("---")
import os
import sqlite3
import secrets
from flask import g
from werkzeug.security import generate_password_hash
    
# Adapted from the official Flask Database Tutorial: 
# https://flask.palletsprojects.com/en/stable/tutorial/database/
# https://flask.palletsprojects.com/en/stable/tutorial/views/


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # base directory for where the script is located 
DB_PATH = os.path.join(BASE_DIR, "notes.db")

# Get the db connection per request 
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH) # open the connection to the db path 
        g.db.row_factory = sqlite3.Row # return d object
    return g.db

# Close the Database connection
def close_db(exc=None):
    db = g.pop("db", None) # remove db from flask
    if db is not None: # if the db connection is found
        db.close() # close the connection

# Set up the DB and create the fake sample users
def init_db(): 
    conn = sqlite3.connect(DB_PATH) # open a connection to the path
    with open(os.path.join(BASE_DIR, "schema.sql")) as f: # open the schema file
        conn.executescript(f.read()) # read and execute the "schema.sql" file

# Sample users for now 
    fake_users = [
        ("admin", "adminJ123", "admin@gmail.com", 1),
        ("jake", "jake123", "jake@gmail.com", 0),
        ("shrek", "shrek123", "shrek@gmail.com", 0)
    ]

    for username, password, email, is_admin in fake_users:
        conn.execute(
            "INSERT INTO users (username, password, email, api_key, is_admin) "
            "VALUES (?, ?, ?, ?, ?)",
            # hash the password, generate a secret api key 32-bit
            (username, generate_password_hash(password), email, secrets.token_hex(16), is_admin),
        )
# Add sample posts for the users 
    conn.execute(
         "INSERT INTO posts (user_id, content, created_at) VALUES (2, 'Hello from Jake!', CURRENT_TIMESTAMP)"
    )
    conn.execute(
         "INSERT INTO posts (user_id, content, created_at) VALUES (3, 'Shrek is here!.', CURRENT_TIMESTAMP)"
       )
    conn.commit() # save the changes to the db
    conn.close() 

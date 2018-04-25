"""
Script to (re-)create table 'books' and fill with data from 'books.csv'
"""

import os
import csv
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config

engine = sa.create_engine(Config.DATABASE_URL)
db_session = scoped_session(sessionmaker(bind=engine))

db_session()

db_session.execute("""
    DROP TABLE IF EXISTS users;
""")

db_session.execute("""
    CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
    );
""")

db_session.execute("""
    CREATE INDEX idx_username
    ON users (username);
""")


db_session.commit()
db_session.remove()

print("table 'users' has been created")

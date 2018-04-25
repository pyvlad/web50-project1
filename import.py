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
    DROP TABLE IF EXISTS books;
""")

db_session.execute("""
    CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn CHAR(10) NOT NULL UNIQUE,
    title VARCHAR(100),
    author VARCHAR(100),
    year INTEGER
    );
""")

db_session.execute("""
    CREATE INDEX idx_isbn
    ON books (isbn);
""")

with open("books.csv", "r") as f:
    db_session()
    reader = csv.DictReader(f, fieldnames=None)     # fieldnames=None: use first row as fieldnames
    for row_num, row_dict in enumerate(reader, 1):
        db_session.execute("""
            INSERT INTO books (isbn, title, author, year)
            VALUES (:isbn, :title, :author, :year);
            """, row_dict)
        print("added book {} {isbn} {title} {author} {year}".format(row_num, **row_dict))
    db_session.commit()
    db_session.remove()

db_session.commit()
db_session.remove()

print("table 'books' has been created")

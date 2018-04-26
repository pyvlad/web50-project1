"""
Script to (re-)create table 'reviews'
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
    DROP TABLE IF EXISTS reviews;
""")

db_session.execute("""
    CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    rating SMALLINT CHECK(rating>=1 AND rating<=5),
    book_id INTEGER REFERENCES books(id),
    user_id INTEGER REFERENCES users(id),
    UNIQUE (book_id, user_id)
    );
""")

db_session.execute("""
    CREATE INDEX idx_book_id
    ON reviews (book_id);
""")

db_session.execute("""
    CREATE INDEX idx_user_id
    ON reviews (user_id);
""")

db_session.commit()
db_session.remove()

print("table 'reviews' has been created")

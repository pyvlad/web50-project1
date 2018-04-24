import os

class Config:
    # Check for environment variable
    DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql+psycopg2://web50:crimson@localhost:5432/web50"
    # Configure session to use filesystem
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

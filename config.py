import os

class Config:
    # Check for environment variable
    DATABASE_URL = os.getenv("DATABASE_URL") # or raise RuntimeError("DATABASE_URL is not set")
    # Configure session to use filesystem
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

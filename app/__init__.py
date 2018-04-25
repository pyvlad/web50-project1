from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Config

# Server-side session support
sess = Session()

# Set up database
engine = create_engine(Config.DATABASE_URL)
db_session = scoped_session(sessionmaker(bind=engine))

# App factory function
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    sess.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

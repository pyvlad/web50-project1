from flask import session
from app.main import bp
from app import db_session


@bp.route("/")
def index():
    user_id = session.get("user_id")

    if user_id:
        db_session()
        user = db_session.execute("SELECT * FROM users WHERE id=:user_id",
            {"user_id": session.get('user_id')}).first()
        username = user.username
    else:
        username = "stranger"

    return "Hello, {}!".format(username)

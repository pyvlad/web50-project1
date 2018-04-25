from flask import session, request, render_template
from app.main import bp
from app import db_session


@bp.route("/")
def index():
    user_id = session.get("user_id")
    username = "stranger"

    if user_id:
        db_session()
        user = db_session.execute("SELECT * FROM users WHERE id=:user_id",
            {"user_id": session.get('user_id')}).first()
        username = user.username

    return render_template("index.html", username=username)


@bp.route("/search")
def search():
    key = request.args.get("key")
    value = request.args.get("value")
    results = []
    db_session()
    if key in {"isbn", "author", "title"}:
        results = db_session.execute(
            "SELECT * FROM books WHERE %s LIKE :value" % key,
            {"value": "%" + value + "%"}).fetchall()
    return render_template("search.html", key=key, value=value, results=results)

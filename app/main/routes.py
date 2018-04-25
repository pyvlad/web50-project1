from flask import session, request, render_template, abort
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


@bp.route("/book/<isbn>")
def book(isbn):
    db_session()
    book = db_session.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    if book is None:
        abort(404)
    return render_template("book.html", book=book)

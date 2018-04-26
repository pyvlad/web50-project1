import requests
from flask import session, request, render_template, abort, redirect, url_for, current_app, jsonify
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


@bp.route("/book/<isbn>", methods=["GET", "POST"])
def book(isbn):
    user_id = session.get("user_id")

    if user_id:
        db_session()
        book = db_session.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()
        if book is None:
            abort(404)
        else:
            if request.method == "POST":
                db_session.execute("""
                    INSERT INTO reviews (message, rating, user_id, book_id)
                    VALUES (:message, :rating, :user_id, :book_id);
                    """,
                    {"message": request.form.get('message'),
                    "rating": request.form.get('rating'),
                    "user_id": user_id, "book_id": book.id}
                )
                db_session.commit()
                return redirect(url_for("main.book", isbn=isbn))
            else:
                reviews = db_session.execute("""
                    SELECT user_id, message, rating, username FROM reviews
                    JOIN users ON users.id=reviews.user_id
                    WHERE book_id=:book_id;
                    """, {"book_id": book.id}).fetchall()

                goodreads = {}
                if current_app.config.get("GOODREADS_KEY"):
                    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": current_app.config.get("GOODREADS_KEY"),
                                "isbns": isbn},
                        timeout=5)
                    if res.status_code != 200:
                        raise Exception("Request to goodreads was unsuccessful")
                    goodreads = (res.json())["books"][0]

                return render_template("book.html", book=book, reviews=reviews,
                                        user_id=int(user_id), goodreads=goodreads)
    else:
        abort(403)




@bp.route("/api/book/<isbn>", methods=["GET", "POST"])
def book_api(isbn):
    db_session()
    book = db_session.execute("""
        SELECT books.id, books.title, books.author, books.year,
            COUNT(reviews.rating) AS total_voters,
            AVG(reviews.rating) AS average_rating
        FROM books
        LEFT JOIN reviews ON books.id=reviews.book_id
        WHERE books.isbn=:isbn
        GROUP BY books.id
        """, {"isbn": isbn}).fetchone()

    if book is None:
        return jsonify({"error": "Invalid book isbn"}), 422
    else:
        if book.average_rating is not None:
            average_rating = round(float(book.average_rating), 2)
        else:
            average_rating = None
            
        return jsonify({
            "isbn": isbn,
            "title": book.title,
            "author": book.author,
            "publication_date": book.year,
            "total_voters": book.total_voters,
            "average_rating": average_rating
        })

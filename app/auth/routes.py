from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.auth import bp
from app import db_session


@bp.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if not request.form.get('username'):
            error = "You must submit username"
        elif not request.form.get('password'):
            error = "You must submit password"
        elif request.form.get('password') != request.form.get('password2'):
            error = "Passwords don't match"
        else:
            db_session()
            user = db_session.execute("SELECT * FROM users WHERE username=:username",
                {"username": request.form.get('username')}).first()
            if user:
                error = "This username already exists. Choose another one."
            else:
                password_hash = generate_password_hash(request.form.get('password'))
                db_session.execute("""
                    INSERT INTO users (username, password_hash)
                    VALUES (:username, :password_hash)""",
                    {"username": request.form.get('username'), "password_hash": password_hash})
                db_session.commit()
                session["user_id"] = user.id
                return 'you have been registered'# redirect(url_for('index'))
    return render_template('auth/register.html', error=error)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not request.form.get('username'):
            error = "You must submit username"
        elif not request.form.get('password'):
            error = "You must submit password"
        else:
            db_session()
            user = db_session.execute("SELECT * FROM users WHERE username=:username",
                {"username": request.form.get('username')}).fetchone()
            if user and check_password_hash(user.password_hash, request.form.get('password')):
                session["user_id"] = user.id
                return 'you have been logged in' #redirect(url_for('index'))
            else:
                error = "Login fail. Wrong username/password."
    return render_template('auth/login.html', error=error)


@bp.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    return "you have been logged out"

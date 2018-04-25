from app.auth import bp
from app import db_session


@bp.route("/register", methods=['GET', 'POST'])
def register():
    return "registration"

@bp.route("/login", methods=['GET', 'POST'])
def login():
    return "login"

@bp.route("/logout")
def logout():
    return "logout"

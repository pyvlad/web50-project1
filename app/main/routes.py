from app.main import bp


@bp.route("/")
def index():
    return "Project 1: TODO"

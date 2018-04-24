from app import create_app
from app import db_session

app = create_app()

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

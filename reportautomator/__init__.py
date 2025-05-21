import os
from dotenv import load_dotenv
from flask import Flask

# Load the environment file
load_dotenv()

# Configure the app
def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    from . import db
    db.init_app(app)

    from . import report
    app.register_blueprint(report.bp)

    return app
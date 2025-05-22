import os
from dotenv import load_dotenv
from flask import Flask

# Define global variables
UPLOAD_FOLDER = 'reportautomator\\temp'

# Load the environment file
load_dotenv()

# Configure the app
def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Import app initiations and register blueprints
    from . import db
    db.init_app(app)

    from . import report
    app.register_blueprint(report.bp)


    return app
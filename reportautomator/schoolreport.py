import pandas as pd
from flask import (
    abort,
    current_app,
    flash,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)
from .reportframe import ReportFrame
from reportautomator.db import get_db

class SchoolReportBlueprint:
    def __init__(self, schoolName, schoolCode):
        self.name = schoolName
        self.code = schoolCode
        self.url_prefix = f"/{self.code}"
        self.app = current_app

    def register_blueprint(self):
        bp = Blueprint(self.name, __name__)

        # Home Page - Shows all devices from the provided school that are in the database
        @bp.route("/", methods=("GET", "POST"))
        def index():
            db = get_db()
            command = f"SELECT * FROM report  WHERE schoolcode='{self.code}' ORDER BY warrantyenddate ASC"
            report = db.execute(command).fetchall()
            return render_template("schoolreport/index.html", report=report)
    
        self.app.register_blueprint(bp, url_prefix=self.url_prefix)
    
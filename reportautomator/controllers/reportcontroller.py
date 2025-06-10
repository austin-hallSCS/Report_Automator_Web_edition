import os
import pandas as pd
from sqlite3 import OperationalError
from werkzeug.utils import secure_filename
from flask import (
    abort,
    current_app,
    flash,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    session
)
from ..reportframe import ReportFrame
from reportautomator.db import get_db

class SchoolReportBlueprint:
    def __init__(self, schoolName, schoolCode):
        self.name = schoolName
        self.code = schoolCode
        self.tableName = f"{schoolCode}report"
        self.url_prefix = f"/{self.code}"
        self.app = current_app

    def register_blueprint(self):
        bp = Blueprint(self.name, __name__)

        # Home Page - Shows all devices from the provided school that are in the database
        @bp.route("/", methods=("GET", "POST"))
        def ViewDevices():
            try:
                db = get_db()
                command = f"SELECT * FROM {self.tableName} LEFT JOIN dellkey ON dellkey.serialnum = {self.tableName}.code ORDER BY warrantyenddate ASC"
                report = db.execute(command).fetchall()
            except OperationalError as e:
                return redirect(url_for(f"{self.name}.TableNotFound"))
            return render_template("schoolreport/viewdevices.html", report=report)
        
        # If the provided school does not have an exising table
        @bp.route("/tablenotfound", methods=("GET", "POST"))
        def TableNotFound():
            return render_template("schoolreport/tablenotfound.html", link=url_for(f"{self.name}.UploadReport"))

        # User can upload an excel file and view it
        @bp.route("/uploadreport", methods=("GET", "POST"))
        def UploadReport():
            ALLOWED_EXTENSIONS = {"xlsx", "xls", "xlsm"}
            def allowed_file(filename):
                return "." in filename and \
                filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    
            if request.method == "POST":
                # Check to see if post request has the file part
                if "file" not in request.files:
                    flash("No file part")
                    return redirect(request.url)
        
                file = request.files["file"]

                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == "":
                    flash("No selected file.")
                    return redirect(request.url)
        
                # If the user selects an invalid file type
                elif allowed_file(file.filename) == False:
                    flash("Invalid file extension")
                    return redirect(request.url)
        
                elif file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                    file.save(filepath)

                    return redirect(url_for(f"{self.name}.ViewExcel", filename=file.filename))
        
            return render_template("schoolreport/uploadreport.html")

        # Display a table created from an uploaded excel file
        @bp.route("/viewexcel/<filename>", methods=("GET", "POST"))
        def ViewExcel(filename):
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            data = ReportFrame(filepath, self.code)

            if request.method == "POST":
                db = get_db()

                # Insert dataframe into the dbtable
                data.dataFrame.rename(columns=lambda x: x.replace(" ", "").lower(), inplace=True)
                data.dataFrame.to_sql(self.tableName, db, if_exists="replace", index_label="device_id", dtype={"device_id": "INTEGER PRIMARY KEY"})


                return redirect(url_for(f"{self.name}.ViewDevices"))


            return render_template("schoolreport/viewexcel.html", filename=filename, data=data.dataFrame)
    
        self.app.register_blueprint(bp, url_prefix=self.url_prefix)
    
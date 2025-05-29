import pandas as pd
import os
from werkzeug.utils import secure_filename
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
from .__init__ import *
from .reportframe import ReportFrame
from . import __init__
from reportautomator.db import get_db

def register_Dynamic_Blueprint(name, app, url_prefix):
    bp = Blueprint(f"{name}", __name__)

    

bp = Blueprint("report", __name__, url_prefix="/report")

def check_school_input(school):
    if (school.upper() not in current_app.config["SCHOOLS"]):
        abort(404)

# Home Page - User selects which school they would like to view devices for
@bp.route("/", methods=("GET", "POST"))
def index():
    db = get_db()

    # Get a list of school Names
    c = db.cursor()
    c.row_factory = lambda cursor, row: row[0]
    schoolsList = c.execute("SELECT name FROM schools").fetchall()

    if request.method == "POST":
        schoolName = str(request.form.get("schoolselect"))
        
        # Get the school code of the selected school
        command = f"SELECT code FROM schools WHERE name='{schoolName}'"
        schoolCode = (c.execute(command)).fetchone()
        c.close()

        return redirect(url_for("report.viewreport", school=schoolCode))
        
    return render_template("report/index.html", schools=schoolsList)

# Shows all devices from the provided school that are in the database
@bp.route("/<string:school>", methods=("GET", "POST"))
def viewreport(school):
    check_school_input(school)
    db = get_db()
    command = f"SELECT * FROM report  WHERE schoolcode='{school}' ORDER BY warrantyenddate ASC"
    report = db.execute(command).fetchall()
    return render_template(f"report/viewreport.html", report=report)


# Show the user a form for them to add a new computer to the database - Is probably going to be deprecated.
@bp.route("/addcomputer", methods=("GET", "POST"))
def addcomputer():

    if request.method == "POST":
        computername = request.form["computername"]
        serialnumber = request.form["serialnumber"]
        warrantyenddate = request.form["warrantyenddate"]

        if computername:
            db = get_db()
            command = f"INSERT or REPLACE INTO {school}report (computername, serialnumber, warrantyenddate, code) VALUES (?, ?, ?, ?)"
            db.execute(command, (computername, serialnumber, warrantyenddate, serialnumber[-3:]))
            db.commit()
            return redirect(url_for("report.index"))

    return render_template("report/addcomputer.html")

# User can upload an excel file and view it
@bp.route("/uploadreport", methods=("GET", "POST"))
def uploadreport():
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

            data = ReportFrame(filepath)

            return redirect(url_for("report.viewexcel", filename=file.filename))
        
    return render_template("report/uploadreport.html")

# Display a table created from an uploaded excel file
@bp.route("/viewexcel/<filename>", methods=("GET", "POST"))
def viewexcel(filename):
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    data = ReportFrame(filepath)

    return render_template("report/viewexcel.html", filename=filename, data=data.dataFrame)

@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
import pandas as pd
import os
from werkzeug.utils import secure_filename
from flask import (
    current_app,
    flash,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from .reportframe import ReportFrame
from . import __init__
from reportautomator.db import get_db

bp = Blueprint("report", __name__)

# Home page - shows current report from the database
@bp.route('/', methods=("GET", "POST"))
def index():
    db = get_db()
    report = db.execute(
        "SELECT * FROM report ORDER BY warrantyenddate ASC"
    ).fetchall()
    return render_template("report/index.html", report=report)

# Show the user a form for them to add a new computer to the database
@bp.route("/addcomputer", methods=("GET", "POST"))
def addcomputer():
    if request.method == "POST":
        computername = request.form["computername"]
        serialnumber = request.form["serialnumber"]
        warrantyenddate = request.form["warrantyenddate"]

        if computername:
            db = get_db()
            db.execute(
                "INSERT or REPLACE INTO report (computername, serialnumber, warrantyenddate, code) VALUES (?, ?, ?, ?)",
                (computername, serialnumber, warrantyenddate, serialnumber[-3:])
            )
            db.commit()
            return redirect(url_for("report.index"))

    return render_template('report/addcomputer.html')

# User can upload an excel file and view it
@bp.route('/uploadreport', methods=("GET", "POST"))
def uploadreport():
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'xlsm'}

    def allowed_file(filename):
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    
    if request.method == "POST":
        # Check to see if post request has the file part
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
        
        # If the user selects an invalid file type
        elif allowed_file(file.filename) == False:
            flash("Invalid file extension")
            return redirect(request.url)
        
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            return redirect(url_for("report.viewexcel", filename=file.filename))
        
    return render_template('report/uploadreport.html')

# Display a table created from an uploaded excel file
@bp.route("/viewexcel/<filename>", methods=("GET", "POST"))
def viewexcel(filename):
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    data = ReportFrame(filepath)

    return render_template('report/viewexcel.html', filename=filename, data=data.dataFrame)
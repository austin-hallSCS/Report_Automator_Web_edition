import pandas as pd
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from . import reportframe
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
@bp.get("/uploadreport")
def uploadreport():
    return render_template('report/uploadreport.html')

# Display a table created from an uploaded excel file
@bp.post("/viewexcel")
def viewexcel():
    file = request.files['file']
    file.save(file.filename)

    data = reportframe.Report.prepare_Spreadsheet(file)
    
    return render_template('report/viewexcel.html', filename=file.filename, data=data)
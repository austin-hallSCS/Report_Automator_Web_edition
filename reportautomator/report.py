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

@bp.route('/', methods=("GET", "POST"))
def index():
    db = get_db()
    report = db.execute(
        "SELECT * FROM report ORDER BY warrantyenddate ASC"
    ).fetchall()
    return render_template("report/index.html", report=report)

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

@bp.get("/uploadreport")
def uploadreport():
    return render_template('report/uploadreport.html')

@bp.post("/viewexcel")
def viewexcel():
    file = request.files['file']
    file.save(file.filename)

    data = reportframe.Report.prepare_Spreadsheet(file)
    table = data.to_html(classes='table')

    return render_template('report/viewexcel.html', filename=file.filename, data=data)
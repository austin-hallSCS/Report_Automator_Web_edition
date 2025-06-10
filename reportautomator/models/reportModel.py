import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Report(db.Model):
    device_id = db.Column(db.Integer, primary_key=True)
    computername = db.column(db.String(20), nullable=False)
    topconsoleuser = db.column(db.String(50))
    operatingsystem = db.column(db.String(50))
    serialnumber = db.column(db.String(10), nullable=False, unique=True)
    asettag = db.column(db.String(10))
    manufacturer = db.column(db.String(50))
    model = db.column(db.String(50))
    code = db.column(db.String(3), nullable=False, default=(serialnumber[-3:]))
    schoolCode = db.column(db.String(4), nullable=False)

    def __repr__(self):
        return self.computername
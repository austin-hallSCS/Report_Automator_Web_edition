import os
from flask import Flask, render_template

# Define 404 error handler
def page_not_found(e):
    return render_template("404.html"), 404

# Configure the app
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Import app initiations and register blueprints
    from . import db
    db.init_app(app)

    """
    from . import report
    app.register_blueprint(report.bp)
    """

    with app.app_context():
        from . import schoolreport

        database = db.get_db()
        c = database.cursor()
        c.execute("SELECT Name, Code FROM schools")
        schools = {}
        for (Name, Code) in c:
            schools[Name] = Code
        
        schoolObjects = {name : schoolreport.SchoolReportBlueprint(name, schools[name]) for name in schools}

        for object in schoolObjects:
            schoolObjects[object].register_blueprint()

    return app
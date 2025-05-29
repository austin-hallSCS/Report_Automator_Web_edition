from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

# Base Config
class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = ".\\reportautomator\\static"
    TEMPLATES_FOLDER = ".\\reportautomator\\templates"
    UPLOAD_FOLDER = r".\reportautomator\temp"
    DATABASE = "reportautomator.sqlite"
    SCHOOLS = ("BBE", "BES", "BHS", "BPE", "CRE", "EBW", "EMS", "GBE", "GES", "GHS", "GWE", "HBW", "HES", "HHS", "HMS", "ILE", "JAE",
               "JWW", "KDDC", "LCE", "LCH", "LCM", "LPE", "MCE", "MES", "MHM", "MTC", "NBE", "NSE", "OES", "PEM", "PGE", "PHS", "PWM",
               "RSM", "RTF", "SCE", "SCH", "SCM", "SMS", "TWH", "UES", "VSE", "WBE", "WES", "WFE", "WHE", "WHH", "WHM", "WHS", "WMS",
               "EBW", "SSF", "TC", "CEO", "MTC")

class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = "developmnent"
    DEBUG = True
    TESTING = True
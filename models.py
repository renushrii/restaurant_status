from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import enum

username, password = "root", "root"
host, port, database = "localhost", 3306, "reports"

app = Flask('app')
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
db = SQLAlchemy(app)

class StoreStatusEnum(enum.Enum):
    Active = "active"
    Inactive = "inactive"

class ReportStatusEnum(enum.Enum):
    Running = "running"
    Completed = "completed"


class StorePollStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.BigInteger, nullable=False, index=True)
    timestamp_utc = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(StoreStatusEnum), nullable=False)

class DayOfWeekEnum(enum.Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

class StoreBuisnessHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.BigInteger, nullable=False, index=True)
    day = db.Column(db.Enum(DayOfWeekEnum), nullable=False)
    start_time_local = db.Column(db.Time, nullable=False)
    end_time_local = db.Column(db.Time, nullable=False)

class StoreTimezone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.BigInteger, nullable=False, unique=True, index=True)
    timezone = db.Column(db.String(255), nullable=False)

class ReportStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True) # report_id
    path = db.Column(db.String(255), default="")
    status = db.Column(db.Enum(ReportStatusEnum), nullable=False)

migrate = Migrate(app, db)

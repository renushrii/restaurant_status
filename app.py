import csv, os
from celery import Celery
from flask import Flask, make_response
from models import db, app, ReportStatus, ReportStatusEnum, StorePollStatus, StoreBuisnessHours, StoreTimezone
from sqlalchemy import asc, desc
from datetime import datetime, timedelta
from datetime import datetime

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

def calculate_uptime_downtime(store_id, current_time):
    observations = StorePollStatus.query(
        StorePollStatus.status, StorePollStatus.timestamp_utc
    ).order_by(asc(StorePollStatus.timestamp_utc)).filter(StorePollStatus.store_id == store_id).all()   
    timezone = StoreTimezone.query.get(store_id=store_id).timezone
    
    if not timezone:
        timezone = "America/Chicago"

    if not observations:
        return (0, 0, 0, 0, 0, 0)

    timestamps = []
    for i in range(len(observations)):
        timestamps.append(observations[i]['timestamp_utc'].astimezone(timezone))
    
    business_hours = StoreBuisnessHours.query(
        StoreBuisnessHours.day, StoreBuisnessHours.start_time_local, StoreBuisnessHours.end_time_local
    ).filter(StoreBuisnessHours.store_id == store_id)

    ## First calculate past hour, Monday to Friday
    current_minus_hour = current_time - timedelta(hours=1)
    current_day_week = current_time.weekday()  # 0 is Monday, 6 is Sunday      
    current_day_week = weekdays[current_day_week] # Monday, Tuesday, etc


    business_days = business_hours.get('business_days', [])
    business_start_hour = business_hours.get('business_start_hour', 0)
    business_end_hour = business_hours.get('business_end_hour', 23)

    total_uptime_last_hour = 0
    total_uptime_last_day = 0
    total_uptime_last_week = 0

    total_downtime_last_hour = 0
    total_downtime_last_day = 0
    total_downtime_last_week = 0

    for i in range(len(observations)):
        current_time = observations[i]['timestamp']
        next_time = observations[i + 1]['timestamp'] if i + 1 < len(observations) else datetime.now()

        time_diff = (next_time - current_time).total_seconds() / 60 

        if current_time.weekday() in business_days and business_start_hour <= current_time.hour < business_end_hour:
            total_uptime_last_hour += time_diff

            if current_time.hour == business_start_hour:
                total_uptime_last_day += time_diff

            if current_time.weekday() == business_days[0] and current_time.hour == business_start_hour:
                total_uptime_last_week += time_diff

        else:
            total_downtime_last_hour += time_diff

            if current_time.hour == business_start_hour:
                total_downtime_last_day += time_diff

            if current_time.weekday() == business_days[0] and current_time.hour == business_start_hour:
                total_downtime_last_week += time_diff

    return (
        total_uptime_last_hour,
        total_uptime_last_day,
        total_uptime_last_week,
        total_downtime_last_hour,
        total_downtime_last_day,
        total_downtime_last_week
    )

def generate_report_id():
    report = ReportStatus(status=ReportStatusEnum.Running)
    db.session.add(report)
    db.session.commit()
    return f"{report.id}"

@celery.task
def generate_report(report_id: str, current_time: datetime):
    with app.app_context():
        path = f"data/{report_id}.csv"
        store_ids = StorePollStatus.query.distinct(StorePollStatus.store_id).all()
        with open(path, "w") as f:
            w = csv.writer(f)
            w.writerow(["store_id", "uptime_last_hour", "uptime_last_day", "uptime_last_week", "downtime_last_hour", "downtime_last_day", "downtime_last_week"])

            for store_id in store_ids:
                up_down_time = calculate_uptime_downtime(store_id, current_time)
                w.writerow([store_id, *up_down_time])

        print(f"Report {report_id} completed")
        report = ReportStatus.query.get(report_id)    
        report.status = ReportStatusEnum.Completed
        report.path = path
        db.session.commit()

@app.route("/trigger_report")
def triggerReport():
    # report_id = generate_report_id()
    # async run_report(report_id, datetime.now()) // <-------- time legi
    # asyncio in python
    report_id = generate_report_id() # TODO: implement this function
    generate_report.delay(report_id, datetime.now())
    return report_id

@app.route("/get_report/<report_id>")
async def getReport(report_id: str):
    # check if data/{report_id}.csv exists
    if not os.path.exists(f"data/{report_id}.csv"):
        return "Running"
    
    # get csv_content from data/{report_id}.csv
    with open(f"data/{report_id}.csv") as f:
        csv_content = f.read()

    response = make_response(csv_content)
    response.headers["content-type"] = "text/csv"
    return response


if __name__ == '__main__':
    app.run(debug=True)



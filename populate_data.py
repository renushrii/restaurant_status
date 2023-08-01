from models import db, StorePollStatus, StoreBuisnessHours, StoreTimezone, app, DayOfWeekEnum
import csv
from datetime import datetime

def populate_store_menu_hours():
    with app.app_context():
        with open('restaurant/data/menu_hours.csv') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            adds = 0
            for row in reader:
                Store_id, day_of_the_week, start_time, end_time = row
                start_time = datetime.strptime(start_time,"%H:%M:%S").time()
                end_time = datetime.strptime(end_time,"%H:%M:%S").time()

                store_menu_hours = StoreBuisnessHours(store_id=int(Store_id), day=DayOfWeekEnum(int(day_of_the_week)),start_time_local = start_time, end_time_local = end_time)
                db.session.add(store_menu_hours)
                adds += 1
                if adds == 100:
                    db.session.commit()
                    adds = 0

            if adds != 0:
                db.session.commit()

def populate_store_timezones_data():
    # read restaurant/data/timezones.csv
    with app.app_context():
        with open('restaurant/data/timezones.csv') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            adds = 0
            for row in reader:
                Store_id, timezone = row

                store_timezone = StoreTimezone(store_id=int(Store_id), timezone=timezone)
                db.session.add(store_timezone)
                adds += 1
                if adds == 100:
                    db.session.commit()
                    adds = 0

            if adds != 0:
                db.session.commit()

def populate_store_poll_status_data():
    # read restaurant/data/store_statis.csv
    # and populate the data into StorePollStatus table
    datetime_format_with_ms = '%Y-%m-%d %H:%M:%S.%f %Z'
    datetime_format_without_ms = '%Y-%m-%d %H:%M:%S %Z'
    with app.app_context():
        with open('restaurant/data/store_status.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # skip 
            adds = 0
            for row in reader:
                store_id, status, timestamp_utc = row

                if "." in timestamp_utc:
                    datetime_timestamp_utc = datetime.strptime(timestamp_utc, datetime_format_with_ms)
                else:
                    datetime_timestamp_utc = datetime.strptime(timestamp_utc, datetime_format_without_ms)

                store_poll_status = StorePollStatus(store_id=int(store_id), timestamp_utc=datetime_timestamp_utc, status=status)
                db.session.add(store_poll_status)
                adds += 1
                if adds == 1000:
                    db.session.commit()
                    adds = 0

            if adds != 0:
                db.session.commit()

populate_store_poll_status_data()
populate_store_timezones_data()
populate_store_menu_hours()
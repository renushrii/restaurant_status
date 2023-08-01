# Flask-Celery Report Generation App

This is a Flask web application that uses Celery to generate reports asynchronously. The application calculates uptime and downtime statistics for different stores based on their poll status. The data is then saved to CSV files for easy access.

## Technologies Used

- Python 3: The programming language used for developing the application.
- Flask: The micro web framework used to handle HTTP requests and responses.
- SQLAlchemy: The Python SQL toolkit and Object-Relational Mapping (ORM) library used for database interaction.
- Celery: A distributed task queue used to generate reports asynchronously.
- Redis: A key-value store used as a broker for Celery tasks.

## Requirements

- Python 3.x
- MySQL (or compatible) database for storing data
- Redis (for Celery broker)

## Installation

1. Clone the repository:

```ruby
git clone https://github.com/renushrii/restaurants_status.git
cd restaurants_status
```

2. Install the required packages:

```ruby
pip install -r requirements.txt
```

3. Set up your MySQL database and update the database connection settings in `app.py`:

```ruby
username, password = "your_db_username", "your_db_password"
host, port, database = "your_db_host", 3306, "your_db_name"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
```

4. Make sure you have Redis installed and running. Update the Redis URL in app.py:

```ruby
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
```

## Database Migration
To create the necessary tables in the database, run the following commands in your terminal:

```bash
python models.py db init
python models.py db migrate
python models.py db upgrade
```

## Data Population
To populate the database with sample data, first unzip `restaurant.zip` file then run the following commands in your terminal:

```bash
python populate_data.py
```

## Running the Application
Start the Flask development server:

```bash
python app.py
```

Visit `http://localhost:5000/trigger_report` in your browser to trigger the report generation. The report generation will be done asynchronously using Celery. You will receive a report ID once the process starts.

## Accessing the Report
To access the generated report, visit `http://localhost:5000/get_report/report_id`, where `report_id` is the ID received after triggering the report generation. If the report is still being generated, you will see "Running." Once the report is completed, the CSV file will be available for download.

## Customizing Business Hours
To customize business hours for each store, update the CSV file named `menu_hours.csv` in the `restaurant/data/` folder. The columns in the file are: `store_id`, `day_of_the_week`, `start_time`, and `end_time`. Ensure that the day_of_the_week values are in the range 0 to 6, where 0 represents Monday and 6 represents Sunday.

## Customizing Timezones
To customize timezones for each store, update the CSV file named timezones.csv in the `restaurant/data/` folder. The columns in the file are: `store_id` and `timezone`. The timezone value should be in the format like `America/Chicago`.

## Customizing Poll Status Data
To customize poll status data for each store, update the CSV file named `store_status.csv` in the `restaurant/data/` folder. The columns in the file are: `store_id`, `status`, and `timestamp_utc`. The `timestamp_utc` should be in the format like `YYYY-MM-DD HH:MM:SS` or `YYYY-MM-DD HH:MM:SS.ssssss.`

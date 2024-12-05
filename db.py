#https://docs.timescale.com/self-hosted/latest/install/installation-docker/
#https://docs.timescale.com/quick-start/latest/python/#connect-to-timescaledb

import psycopg2
import numpy as np

def connect():
    CONNECTION = "dbname=postgres user=postgres password=password host=localhost port=5432"
    conn = psycopg2.connect(CONNECTION)
    return conn

def sensortable():
    sensor_table = "CREATE TABLE IF NOT EXISTS sensor (time TIMESTAMPTZ NOT NULL, numberPeople INT NOT NULL);"
    return sensor_table

def hypertable():
    hyper_table = "SELECT create_hypertable('sensor', by_range('time'));"
    return hyper_table

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sensortable())
    try:
        cursor.execute(hypertable())
    finally:
        conn.commit()
        cursor.close()

def insert_data(numberPeople):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor (time, numberPeople) VALUES (NOW(), %s)", (numberPeople))
    conn.commit()
    cursor.close()

def get_latest_data():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor ORDER BY time DESC LIMIT 1;")
    result = cursor.fetchone()
    cursor.close()
    return result

def every_daily_avg():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT time_bucket('1 day'::interval, time), average(stats_agg(numberPeople)) FROM sensor GROUP BY 1;")
    result = cursor.fetchall()
    cursor.close()
    return result

def next_three_hours():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT numberPeople FROM sensor ORDER BY time DESC LIMIT 1;")
    current_people = cursor.fetchone()
    next_3_hours = [round(current_people[0] + np.random.uniform(-3, 3)) for _ in range(3)]
    cursor.close()
    return next_3_hours

def total_today():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(numberPeople) FROM sensor WHERE time::date = CURRENT_DATE;")
    result = cursor.fetchone()
    cursor.close()
    return result

def historical_total():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(numberPeople) FROM sensor;")
    result = cursor.fetchone()
    cursor.close()
    return result

def busiest_time():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM sensor ORDER BY numberPeople DESC LIMIT 1;")
    result = cursor.fetchone()
    cursor.close()
    return result

def least_busy_time():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM sensor ORDER BY numberPeople ASC LIMIT 1;")
    result = cursor.fetchone()
    cursor.close()
    return result


import psycopg2 as psycopg2
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()


def connect_database():
    """
    Connection to work with the remote database on Heroku platform.
    :return: connection
    """
    connection = psycopg2.connect(
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
    )

    return connection


def drop_table():
    connect = connect_database()
    cur = connect.cursor()

    cur.execute('''
        DROP TABLE IF EXISTS predictions CASCADE
        ''')

    connect.commit()


def create_table():
    """
    Create empty table in database.
    :return: None
    """
    connect = connect_database()
    cur = connect.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id serial PRIMARY KEY,
        area NUMERIC(5,2),
        room INT,
        year_of_building INT,
        floor INT,
        total_floor INT,
        city varchar(50),
        predicted_price NUMERIC(10,4)
    );
    ''')

    connect.commit()


def insert_into_table(input_df, prediction) -> None:
    """Inserts the features and predicted prices the into table in database"""
    connect = connect_database()
    cur = connect.cursor()

    input_df['Prediction'] = prediction
    np.round(input_df['Prediction'], decimals=2)

    for i, row in input_df.iterrows():
        sql = "INSERT INTO predictions (area, room, year_of_building, floor, total_floor, city, predicted_price) " \
              "VALUES (" \
              "%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, tuple(row))

    connect.commit()


def select_from_table():
    """ Selects and returns 10 most recent requests and responses in JSON format
    :return: list of 10 most recent requests and responses
    """
    connect = connect_database()
    cur = connect.cursor()
    cur.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()

    result = [f"id: {row[0]}, area: {row[1]}, room: {row[2]}, year_of_building: {row[3]}, floor: {row[4]}, " \
              f"total_floor: {row[5]}, city: {row[6]}, predicted_price: {row[7]}" for row in rows]

    return result
    connect.commit()

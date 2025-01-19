import pymysql
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'website_kesehatan',
    'port': 3307  # Specify port 3307
}

def get_db_connection():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port']  # Add the port to the connection
    )
    return conn



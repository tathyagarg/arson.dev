import os

from psycopg2 import connect as psql_connect

DATABASE_URL = os.getenv('DATABASE_URL')

def connect():
    return psql_connect(DATABASE_URL)

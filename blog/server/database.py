import sqlite3

DATABASE = 'blog.db'

def connect():
    return sqlite3.connect(DATABASE)

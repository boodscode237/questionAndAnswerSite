from flask import g
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor

def connect_db():
    # URI from postgres
    conn = psycopg2.connect('postgres://thoppsilkanxex:c61f236095e2e87e4144732b85ca2e455cd4eba7d3dbe99871e3c61722c66675@ec2-54-166-167-192.compute-1.amazonaws.com:5432/d194s9v7t17t09', cursor_factory=DictCursor)
    conn.autocommit = True
    sql = conn.cursor()
    return conn, sql


def get_db():
    db = connect_db()

    if not hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn = db[0]

    if not hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur = db[1]

    return g.postgres_db_cur


def init_db():
    db = connect_db()

    db[1].execute(open('schema.sql', 'r').read())
    db[1].close()

    db[0].close()


def init_admin():
    db = connect_db()

    db[1].execute('update users set admin = True where name = %s', ('Admin',))

    db[1].close()
    db[0].close()
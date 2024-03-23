import psycopg2

def create_connection():
    conn = psycopg2.connect(
        database="postgres", user='postgres',
        password='1234', host='localhost', port=5432
    )
    return conn


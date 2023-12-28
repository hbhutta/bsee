import os
from dotenv import find_dotenv, load_dotenv
import psycopg2

load_dotenv(find_dotenv())

def create_table():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('DBUSER')} password={os.getenv('DBPASSWORD')} host={os.getenv('DBHOST')} port={os.getenv('DBPORT')}") # dbname and table name are not the same
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS bsee (id INTEGER, place_id VARCHAR, name VARCHAR, city VARCHAR, address VARCHAR, ratings FLOAT, tags VARCHAR[], photo_reference VARCHAR)")
    conn.commit()
    cur.close()
    conn.close()

create_table()
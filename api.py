from flask import Flask, render_template
import psycopg2
import os
import json
from dotenv import load_dotenv, find_dotenv
from random import randint
app = Flask(__name__, static_folder='templates/static', template_folder='templates')

load_dotenv(find_dotenv())

@app.route('/')
def index():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('DBUSER')} password={os.getenv('DBPASSWORD')} host={os.getenv('DBHOST')} port={os.getenv('DBPORT')}") # dbname and table name are not the same
    cur = conn.cursor()
    rand_id = randint(1, 600)
    cur.execute(f"SELECT * FROM bsee WHERE id = {rand_id}")
    data = cur.fetchone()
    cur.close()
    conn.close()
    print(data)
    name = data[2]
    city = data[3]
    address = data[4]
    rating = data[5]
    tags = data[6]
    photo_reference = data[7]

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous"> -->
        <title>Bsee: Explore BC!</title>
    </head>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <h1 style="margin: auto; text-align: center; margin: 1em;"><i>You should visit...</i></h1>
        <div style="display: flex">
            <div style="width: 50%; text-align: center;">
                <img style="margin-left: 2em;" src='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={os.getenv('GOOGLE_MAPS_API_KEY')}'></img>
            </div>
            <div style="width: 50%; Arial, Helvetica, sans-serif;">
                <p><strong style=>Place:</strong> {name}</p>
                <p><strong>City</strong>: {city}</p>
                <p><strong>Address</strong>: {address}</p>
                <p><strong>Rating (Out of 5)</strong>: {rating}</p>
                <p><strong>Tags</strong>: {tags}</p>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run()
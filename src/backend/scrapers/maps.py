GOOGLE_MAPS_API_KEY = 'AIzaSyDgfUC9a0zgeP1VfIYajOJ0uT4I4HiJaLw'

import os
import requests, json
from time import sleep
from pprint import pprint
from classes.place import Place

import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password=R1a4786$ host=localhost port=5432") # dbname and table name are not the same
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS bsee (id serial PRIMARY KEY, name varchar, city varchar, address varchar);")

with open('cities.json', 'r') as f:
    cities = json.load(f)

with open('attractions.json', 'r') as f:
    attractions = json.load(f)

places = []
for city in cities['cities']:
    try: 
        for attraction in attractions[city]["attractions"]:
            attraction = str(attraction)
            attraction = attraction.replace(" ", "%20")
            request = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={attraction}&inputtype=textquery&fields=name,formatted_address&key={GOOGLE_MAPS_API_KEY}")
            try:
                formatted_address = request.json()["candidates"][0]["formatted_address"]
                name = request.json()["candidates"][0]["name"]
                place = Place(name, city, formatted_address)
                places.append(place)
                cur.execute("INSERT INTO bsee (name, city, address) VALUES (%s, %s, %s)", (name, city, formatted_address))
                conn.commit()
                pprint(f'Inserted ({name}, {city}, {formatted_address}) into table.')
                # sleep(0.5)
            except IndexError:
                pprint(f"Couldn't get formatted_address of {attraction} in {city}. Skipped.")
    except KeyError:
        pass
    
# cur.execute("INSERT INTO bsee (name, city, address) VALUES (%s, %s, %s)", ('name', 'city', 'formatted_address'))
conn.commit()
cur.close()
conn.close()









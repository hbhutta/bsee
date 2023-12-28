import os
import random
import requests, json
from time import sleep
from pprint import pprint
from dotenv import find_dotenv, load_dotenv
# from schema.attraction import Attraction

load_dotenv(find_dotenv())

DATA_SIZE=600

import psycopg2

'''
When we retrieve an attraction, we will also get a photo of it using Google Place Photos API
'''
# def retrieve() -> Attraction:
#     conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('DBUSER')} password={os.getenv('DBPASSWORD')} host={os.getenv('DBHOST')} port={os.getenv('DBPORT')}") # dbname and table name are not the same
#     cur = conn.cursor()
    
#     rand_id = random.randint(1, DATA_SIZE)
#     cur.execute(f"SELECT * FROM bsee WHERE id={rand_id}")
#     data = cur.fetchone()

#     attraction = Attraction()
#     _, attraction.name, attraction.city, attraction.address = data 

#     conn.commit()
#     cur.close()
#     conn.close()

#     return attraction

def format_tags(tags: list) -> str:
    tag_string = "{"
    for tag in tags:
        formatted_tag = tag + ', '  # PostgreSQL compatible list of text
        tag_string += formatted_tag
    tag_string = tag_string[:len(tag_string)-2].strip()
    tag_string += '}'
    return tag_string

    
def aggregate_attractions():
    conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('DBUSER')} password={os.getenv('DBPASSWORD')} host={os.getenv('DBHOST')} port={os.getenv('DBPORT')}") # dbname and table name are not the same
    cur = conn.cursor()

    with open(r'C:\Users\haadb\OneDrive\Desktop\Projects\bsee\database\json\cities.json', 'r') as f:
        cities = json.load(f)

    with open(r'C:\Users\haadb\OneDrive\Desktop\Projects\bsee\database\json\attractions.json', 'r') as f:
        attractions = json.load(f)

    id = 1
    for city in cities['cities']:
        try: 
            for attraction in attractions[city]["attractions"]:
                attraction = str(attraction)
                attraction = attraction.replace(" ", "%20")
                request = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={attraction}&inputtype=textquery&fields=name,formatted_address,rating,place_id,photo,type&key={os.getenv('GOOGLE_MAPS_API_KEY')}")
                
                try:
                    formatted_address = request.json()["candidates"][0]["formatted_address"]
                    name = request.json()["candidates"][0]["name"]
                    place_id = request.json()["candidates"][0]["place_id"]
                    rating = str(request.json()["candidates"][0]["rating"])
                    tags = request.json()["candidates"][0]["types"]
                    formatted_tags = format_tags(tags)
                    photo_reference = request.json()["candidates"][0]["photos"][0]["photo_reference"]
                    print(formatted_tags)
                    print('\n\n\n')
                    cur.execute("INSERT INTO bsee (id, place_id, name, city, address, ratings, tags, photo_reference) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (str(id), place_id, name, city, formatted_address, rating, formatted_tags, photo_reference))
                    conn.commit()
                    pprint(f'Inserted ({str(id)}, {place_id}, {name}, {city}, {formatted_address}, {rating}, {format_tags(tags)}, {photo_reference}) into table.')
                    id += 1
                except IndexError:
                    pprint(f"Couldn't get a field of {attraction} in {city}. Skipped.")
        except KeyError:
            pass

    conn.commit()
    cur.close()
    conn.close()


aggregate_attractions()








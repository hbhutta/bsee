import requests
from bs4 import BeautifulSoup
from time import sleep
import json
from pprint import pprint
import re

def find_phone_numbers(text: str) -> list[str]:
    pattern = re.compile(r'\b\d{3}-\d{3}-\d{4}')
    phone_numbers = re.findall(pattern, text)
    return phone_numbers

request = requests.get('https://transcanadahighway.com/british-columbia/towns/')
soup = BeautifulSoup(request.content, features='html.parser')

'''
Enumerate places in B.C.
'''
cities = []
first_wpb = soup.find_all('div', {"class" : "wpb_wrapper"}) 
for first_div in first_wpb:
    second_wpb = first_div.find_all('div', {"class" : "wpb_text_column wpb_content_element"})
    for second_div in second_wpb:
        third_wpb = second_div.find_all('div', {"class" : "wpb_wrapper"}) 
        for third_div in third_wpb:
            uls = third_div.find_all('ul')
            for ul in uls:
                lis = ul.find_all('li')
                for li in lis:
                    if ('Itinerary' not in li.text):
                        if ('🍁' in li.text):
                            # print(li.text[:-2].strip().lower().replace(' ', '-'))
                            cities.append(li.text[:-2].strip().lower().replace(' ', '-').removesuffix(',-bc'))
                            '''
                            - If the string contains / replace it with everything up to / 
                            '''
                            if '/' in li.text:
                                # print('ajfhakjfhakjfhakjahf')
                                idx = li.text.find('/')
                                cities.append(li.text[:idx].strip().lower().replace(' ', '-').removesuffix(',-bc'))
                                # print(li.text[:idx].strip().lower().replace(' ', '-').removesuffix('-'))
                            '''
                            TODO: If the string contains UTF encoded text, remove the encoded text
                            '''
                            if '\\u' in li.text:
                                pass 
                        else: 
                            cities.append(li.text.strip().lower().replace(' ', '-').removesuffix(',-bc'))
                            # print(li.text.strip().lower().replace(' ', '-'))


'''
Remove duplicate cities
'''
count = {}
prepared_cities = []
for city in cities:
    count[city] = 0
for city in cities:
    count[city] += 1
for city in cities:
    if count[city] == 1: prepared_cities.append(city)
cities = prepared_cities
print('Removed duplicates')

pprint(prepared_cities)

'''
Serialize city
'''
print(f'Enumerated {len(cities)} places in B.C.!')
with open('places.json', 'w') as f:
    try:
        json.dump(cities, f)
    except TypeError as t:
        print(t)
    f.close()

'''
Enumerate all the attractions of each place
'''
with open('places.json', 'r') as f:
    try: 
        cities = json.load(f)
        print('Loaded places!')
    except FileNotFoundError as e:
        print('Failed to load places.')

attractions = []
print('Enumerating attractions in each place...')
for place in cities: # Third place
    source = f'https://transcanadahighway.com/british-columbia/{place}'
    
    request = requests.get(source)
    if (request.status_code == 200):
        print(f'Request for information about {place} successful!')
        soup = BeautifulSoup(request.content, features='html.parser')
        first_wpb = soup.find_all('div', {"class" : "wpb_wrapper"}) 
        for first_div in first_wpb:
            print('In first_div')
            second_wpb = first_div.find_all('div', {"class" : "wpb_text_column wpb_content_element"})
            print(second_wpb)
            for second_div in second_wpb:
                print('In second_div')
                third_wpb = second_div.find_all('div', {"class" : "wpb_wrapper"}) 
                for third_div in third_wpb:
                    print('In third_div')
                    try: 
                        h2 = third_div.find('h2')
                    except AttributeError:
                        pass
                    if not h2: pass
                    elif 'Attraction' in h2.text:
                        para = third_div.find('p') 
                        if para.text:
                            para_info = para.text.split('\n') # .text converts <br /> to \n
                            print(third_div.find('h3').text)
                            print(para_info)
                            
                            try:
                                phone_number = find_phone_numbers(para.text)[0] # para_info[1]
                            except IndexError as e:
                                phone_number = ''
                                pass # We can't get the phone number

                            try: 
                                address = para_info[0]
                            except IndexError as e:
                                address = ''
                                pass

                            attractions.append(
                                {
                                    'name': third_div.find('h3').text,
                                    'city': place,
                                    'address': address,
                                    'phone_number': phone_number, # phone_number,
                                    'description': '' # Left blank for now (we won't use TCH's descriptions)
                                }
                            )
                                
                        attraction = {
                            'name': third_div.find('h3').text,
                            'city': '',
                            'address': '',
                            'phone_number': '',
                            'description': '' # Left blank for now (we won't use TCH's descriptions)
                        }
                        attractions.append(attraction)
                        attractions.append(
                            {
                                'name': third_div.find('h3').text,
                                'city': place,
                                'address': '',
                                'phone_number': find_phone_numbers(para.text)[0], # There should only be one phone number
                                'description': '' # Left blank for now (we won't use TCH's descriptions)
                            }
                        )  
                        pprint(attraction)


pprint(attractions)
with open('attractions.json', 'w') as f:
    try:
        json.dump(attractions, f)
    except TypeError as t:
        print(t)
    f.close()

# ...

with open('places_info.json', 'r') as f: 
    saved_places  = json.load(f)
    f.close()

pprint(saved_places)




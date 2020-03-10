import googlemaps
import webbrowser
import config
import mysql.connector
import requests
from constants import BASE_URL

gmaps = googlemaps.Client(config.key)      #global variable gmaps

def direction(origin,destination):
    result = gmaps.directions(origin,destination)
    address = f'origin={origin}&destination={destination}'
    result_url = f'{BASE_URL["direction"]}&{address.lower().replace(" ", "+")}'
    print(result_url)
    webbrowser.open_new(result_url)

def geocoding(search_location):
    result = gmaps.geocode(search_location)
    print("Formatted Address: "+result[0]['formatted_address'])
    print("Latitude: "+str(result[0]['geometry']['location']['lat'])+" "+"Longitude: "+str(result[0]['geometry']['location']['lng']))
    address = search_location
    result_url = f'{BASE_URL["geocoding"]}={address.lower().replace(" ", "+")}'
    webbrowser.open_new(result_url)

def mapsstatic(search_location):
    address = search_location
    result_url = f'https://maps.googleapis.com/maps/api/staticmap?center={address.lower().replace(" ", "+")}&zoom=13&scale=1&size=600x350&maptype=roadmap&key={config.key}&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7C{address.lower().replace(" ", "+")}'
    print(result_url)
    webbrowser.open_new(result_url)

def elevation(search_location):                   #takes "search_location" as input
    result = gmaps.geocode(search_location)             #"result" is geocoded json object
    json = requests.get(f'https://maps.googleapis.com/maps/api/elevation/json?locations={result[0]["geometry"]["location"]["lat"]},{result[0]["geometry"]["location"]["lng"]}&key={config.key}').json()         #API call
    result_value = json['results'][0]['elevation']              #elevation obtained from json
    position = "above" if result_value>0 else "below"
    print(f'{search_location} is {round(result_value,2)} metres {position} sea level')




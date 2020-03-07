import googlemaps
import webbrowser
import config
import mysql.connector
from constants import BASE_URL

gmaps = googlemaps.Client(config.key)
#global variable gmaps

def direction(origin,destination):
    result = gmaps.directions(origin,destination)
    address = "origin="+origin+"&"+"destination="+destination
    address = address.lower()
    address = address.replace(" ","+")
    result_url = "{}&{}".format(BASE_URL['direction'], address.lower().replace(" ", "+"))
    print(result_url)
    webbrowser.open_new(result_url)

def timezone(search_location):
    address = search_location.lower()
    address = address.replace(" ","+")
    result_url = 'https://maps.googleapis.com/maps/api/timezone/json?location=3'+address+'9.6034810,-119.6822510&timestamp=1331766000&key='+config.key
    print(result_url)
    webbrowser.open_new(result_url)

def geocoding(search_location):
    gmaps = googlemaps.Client(config.key)
    result = gmaps.geocode(search_location)
    print("Formatted Address: "+result[0]['formatted_address'])
    print("Latitude: "+str(result[0]['geometry']['location']['lat'])+" "+"Longitude: "+str(result[0]['geometry']['location']['lng']))
    address = search_location.lower()
    address = address.replace(" ","+")
    result_url = "{}={}".format(BASE_URL['geocoding'], address.lower().replace(" ", "+"))
    webbrowser.open_new(result_url)

def mapsstatic(search_location):
    address = search_location.lower()
    address = address.replace(" ","+")
    result_url = "https://maps.googleapis.com/maps/api/staticmap?center="+address+"&zoom=13&scale=1&size=600x350&maptype=roadmap&key="+config.key+"&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7C"+address
    print(result_url)
    webbrowser.open_new(result_url)


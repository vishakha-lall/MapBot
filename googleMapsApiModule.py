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

def add_to_maps_database(origin,destination):
    db = mysql.connector.connect(user=config.user,password=config.password,host=config.host,database=config.database)
    cur = db.cursor()
    cur = db.cursor(buffered=True)
    if destination == "":
        cur.execute("INSERT INTO directions_table(origin_location) VALUES (%s)",(origin,))
        db.commit()
    elif origin == "":
        cur.execute("SELECT id FROM directions_table ORDER BY id DESC")
        res = cur.fetchone()
        last_id = res[0]
        cur.execute('UPDATE directions_table SET destination_location=%s WHERE id=%s',(destination,last_id))
        db.commit()
    else:
        cur.execute("INSERT INTO directions_table(origin_location,destination_location) VALUES (%s,%s)",(origin,destination))
        db.commit()

def get_from_maps_database():
    db = mysql.connector.connect(user=config.user,password=config.password,host=config.host,database=config.database)
    cur = db.cursor()
    cur = db.cursor(buffered=True)
    cur.execute("SELECT id FROM directions_table ORDER BY id DESC")
    res = cur.fetchone()
    last_id = res[0]
    cur.execute('SELECT origin_location FROM directions_table WHERE id=%s', (last_id,))
    res = cur.fetchone()
    origin = res[0]
    cur.execute('SELECT destination_location FROM directions_table WHERE id=%s', (last_id,))
    res = cur.fetchone()
    destination = res[0]
    return origin,destination

def geocoding(search_location):
    gmaps = googlemaps.Client(config.key)
    result = gmaps.geocode(search_location)
    print("Formatted Address: "+result[0]['formatted_address'])
    print("Latitude: "+str(result[0]['geometry']['location']['lat'])+" "+"Longitude: "+str(result[0]['geometry']['location']['lng']))
    address = search_location.lower()
    address = address.replace(" ","+")
    result_url = "{}&{}".format(BASE_URL['geocoding'], address.lower().replace(" ", "+"))
    webbrowser.open_new(result_url)


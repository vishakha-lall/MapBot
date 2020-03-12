import googlemaps
import webbrowser
import config
import mysql.connector
from constants import BASE_URL
import logging
import logger_config

gmaps = googlemaps.Client(config.key)      #global variable gmaps

log = logging.getLogger(__name__)
log.info('Entered module: %s' % __name__)

@logger_config.logger 
def direction(origin,destination):
    result = gmaps.directions(origin,destination)
    address = f'origin={origin}&destination={destination}'
    result_url = f'{BASE_URL["direction"]}&{address.lower().replace(" ", "+")}'
    logging.debug(result_url)
    webbrowser.open_new(result_url)

<<<<<<< HEAD
def timezone(search_location,timestamp):
    address = search_location.lower()
    address = address.replace(" ","+")
    result_url = f'https://maps.googleapis.com/maps/api/timezone/json?location={address}&timestamp={timestamp}&key={config.key}
    print(result_url)
    webbrowser.open_new(result_url)

=======
@logger_config.logger 
>>>>>>> upstream/gssoc-master
def geocoding(search_location):
    result = gmaps.geocode(search_location)
    logging.debug("Formatted Address: "+result[0]['formatted_address'])
    logging.debug("Latitude: "+str(result[0]['geometry']['location']['lat'])+" "+"Longitude: "+str(result[0]['geometry']['location']['lng']))
    address = search_location
    result_url = f'{BASE_URL["geocoding"]}={address.lower().replace(" ", "+")}'
    webbrowser.open_new(result_url)

@logger_config.logger 
def mapsstatic(search_location):
    address = search_location
    result_url = f'https://maps.googleapis.com/maps/api/staticmap?center={address.lower().replace(" ", "+")}&zoom=13&scale=1&size=600x350&maptype=roadmap&key={config.key}&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7C{address.lower().replace(" ", "+")}'
    logging.debug(result_url)
    webbrowser.open_new(result_url)


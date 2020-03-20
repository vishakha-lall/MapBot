import googlemaps
import webbrowser
import config
from constants import BASE_URL
import requests
import logging
import logger_config

gmaps = googlemaps.Client(config.key)      # global variable gmaps

log = logging.getLogger(__name__)
log.info('Entered module: %s' % __name__)


@logger_config.logger
def direction(origin, destination):
    result = gmaps.directions(origin, destination)
    address = f'origin={origin}&destination={destination}'
    result_url = f'{BASE_URL["direction"]}&{address.lower().replace(" ", "+")}'
    logging.debug(result_url)
    webbrowser.open_new(result_url)
    return result_url


@logger_config.logger
def geocoding(search_location):
    result = gmaps.geocode(search_location)
    logging.debug("Formatted Address: "+result[0]['formatted_address'])
    logging.debug("Latitude: "+str(result[0]['geometry']['location']['lat']) + " " + "Longitude: " + str(result[0]['geometry']['location']['lng']))
    address = search_location
    result_url = f'{BASE_URL["geocoding"]}={address.lower().replace(" ", "+")}'
    webbrowser.open_new(result_url)
    return result_url


@logger_config.logger
def mapsstatic(search_location):
    address = search_location
    result_url = f'https://maps.googleapis.com/maps/api/staticmap?center={address.lower().replace(" ", "+")}&zoom=13&scale=1&size=600x350&maptype=roadmap&key={config.key}&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7C{address.lower().replace(" ", "+")}'
    logging.debug(result_url)
    webbrowser.open_new(result_url)
    return result_url


"""Summary or Description of the Function
        Parameters:
        search_location(str): The location entered by user

        Returns:
        result_value(int): elevation(in metres) above/below sea level
    """


def elevation(search_location):
    result = gmaps.geocode(search_location)
    json = requests.get(f'https://maps.googleapis.com/maps/api/elevation/json?locations={result[0]["geometry"]["location"]["lat"]},{result[0]["geometry"]["location"]["lng"]}&key={config.key}').json()
    result_value = json['results'][0]['elevation']
    position = "above" if result_value > 0 else "below"
    print(f'{search_location} is {round(result_value,2)} metres {position} sea level')
    return result_value
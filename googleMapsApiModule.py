import googlemaps
import webbrowser
import config
from constants import BASE_URL
import requests
import logging
import logger_config
from datetime import datetime, date        # noqa: F401
import calendar


gmaps = googlemaps.Client(config.key)      # global variable gmaps

log = logging.getLogger(__name__)
log.info('Entered module: %s' % __name__)


@logger_config.logger
def direction(origin, destination):
    result = gmaps.directions(origin, destination)    # noqa
    address = f'origin={origin}&destination={destination}'
    result_url = f'{BASE_URL["direction"]}&{address.lower().replace(" ", "+")}'
    logging.debug(result_url)
    webbrowser.open_new(result_url)
    return result_url


@logger_config.logger
def get_timestamp(date_time):
    yr, mon, day, hr, mi = map(int, date_time.split())
    d = datetime(yr, mon, day, hr, mi)
    timestamp = calendar.timegm(d.timetuple())
    return timestamp


@logger_config.logger
def get_lat_lng(place):
    response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={config.key}')   # noqa: E501
    resp_json_payload = response.json()
    lat_lng = resp_json_payload['results'][0]['geometry']['location']
    return (lat_lng)


@logger_config.logger
def timezone(place, date_time):  # format of datetime should be YYYY MM DD Hrs Mins and place should be a normal string   # noqa: E501
    lat_lng = get_lat_lng(place)
    timestamp = get_timestamp(date_time)
    response = requests.get(f'https://maps.googleapis.com/maps/api/timezone/json?location={lat_lng["lat"]},{lat_lng["lng"]}&timestamp={timestamp}&key={config.key}')   # noqa: E501
    resp_dict = response.json()
    for key in resp_dict:
        print(f"{key} : {resp_dict[key]}")


@logger_config.logger
def geocoding(search_location):
    result = gmaps.geocode(search_location)
    logging.debug("Formatted Address: "+result[0]['formatted_address'])
    logging.debug("Latitude: "+str(result[0]['geometry']['location']['lat']) + " " + "Longitude: " + str(result[0]['geometry']['location']['lng']))   # noqa: E501
    address = search_location
    result_url = f'{BASE_URL["geocoding"]}={address.lower().replace(" ", "+")}'
    webbrowser.open_new(result_url)
    return result_url


@logger_config.logger
def mapsstatic(search_location):
    address = search_location
    result_url = f'https://maps.googleapis.com/maps/api/staticmap?center={address.lower().replace(" ", "+")}&zoom=13&scale=1&size=600x350&maptype=roadmap&key={config.key}&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7C{address.lower().replace(" ", "+")}'   # noqa: E501
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
    json = requests.get(f'https://maps.googleapis.com/maps/api/elevation/json?locations={result[0]["geometry"]["location"]["lat"]},{result[0]["geometry"]["location"]["lng"]}&key={config.key}').json()   # noqa: E501
    result_value = json['results'][0]['elevation']
    position = "above" if result_value > 0 else "below"
    print(f'{search_location} is {round(result_value,2)} metres {position} sea level')   # noqa: E501
    return result_value

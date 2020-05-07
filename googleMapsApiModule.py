import googlemaps
import urllib
import config
from constants import BASE_URL
import logging
import logger_config

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)

try:
    gmaps = googlemaps.Client(config.key)  # global variable gmaps
except ValueError as e:
    logging.debug(e)
    gmaps = None


def _get_location(location_text):
    """Used to preprocess the input location_text for URL encoding.
    Doesn't do much right now. But provides a place to add such steps in future.
    """
    return location_text.strip().lower()


@logger_config.logger
def direction(origin, destination):
    result = gmaps.directions(origin, destination)
    logging.debug("Summary: " + result[0]["summary"])
    result_url = (
        BASE_URL["direction"]
        + "&"
        + urllib.parse.urlencode(
            {"origin": _get_location(origin), "destination": _get_location(destination)}
        )
    )
    logging.debug(result_url)
    return result_url


@logger_config.logger
def timezone(search_location):
    result = gmaps.geocode(search_location)
    logging.debug("Formatted Address: " + result[0]["formatted_address"])
    latlng = (
        result[0]["geometry"]["location"]["lat"],
        result[0]["geometry"]["location"]["lng"],
    )
    logging.debug(f"Latitude: {latlng[0]} Longitude: {latlng[1]}")
    timezone = gmaps.timezone(latlng)
    timeZoneId = timezone["timeZoneId"]
    import pytz

    tz_obj = pytz.timezone(timeZoneId)
    current_time = pytz.datetime.datetime.now(tz=tz_obj)
    time_in_timezone = pytz.datetime.datetime.strftime(
        current_time, "%a, %d %b %Y %H:%M:%S %Z"
    )
    return timeZoneId, time_in_timezone


@logger_config.logger
def geocoding(search_location):
    result = gmaps.geocode(search_location)
    logging.debug("Formatted Address: " + result[0]["formatted_address"])
    latlng = (
        result[0]["geometry"]["location"]["lat"],
        result[0]["geometry"]["location"]["lng"],
    )
    logging.debug(f"Latitude: {latlng[0]} Longitude: {latlng[1]}")
    place_id = result[0]["place_id"]
    place = gmaps.place(place_id)
    result_url = place["result"]["url"]
    return result_url


@logger_config.logger
def mapsstatic(address, zoom=13, size="600x350"):
    result_url = (
        BASE_URL["mapsstatic"]
        + "?"
        + urllib.parse.urlencode(
            {
                "center": _get_location(address),
                "zoom": zoom,
                "size": size,
                "key": config.key,
            }
        )
    )
    logging.debug(result_url)
    return result_url


@logger_config.logger
def elevation(search_location):
    result = gmaps.geocode(search_location)
    latlng = (
        result[0]["geometry"]["location"]["lat"],
        result[0]["geometry"]["location"]["lng"],
    )
    result = gmaps.elevation(latlng)
    result_value = result[0]["elevation"]
    position = "above" if result_value > 0 else "below"
    logging.debug(
        f"{search_location} is {round(result_value,2)} metres {position} sea level"
    )
    return str(result_value) + " metres"


@logger_config.logger
def places(search_location):
    locations = gmaps.places(search_location)
    N = 3
    place_details = {}
    try:
        filtered_locations = sorted(
            locations["results"],
            key=lambda loc: (loc["user_ratings_total"], loc["rating"]),
            reverse=True,
        )[:N]
    except Exception:
        filtered_locations = locations["results"]
    logging.debug(filtered_locations)
    first_N_places = {res["name"]: res["place_id"] for res in filtered_locations}
    for name, place_id in first_N_places.items():
        place_details[name] = gmaps.place(place_id)["result"]["url"]
    return place_details

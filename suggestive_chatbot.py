import googleMapsApiModule
import logging
import logger_config

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)


@logger_config.logger
def directions_suggestion(origin_text, destination_text):
    """Get Directions."""
    try:
        bot_response = googleMapsApiModule.direction(origin_text, destination_text)
    except Exception as e:
        logging.debug(e)
        return None
    logging.debug(bot_response)
    return bot_response


@logger_config.logger
def geocoding_suggestion(location_text):
    """Find a place."""
    try:
        bot_response = googleMapsApiModule.geocoding(location_text)
    except Exception as e:
        logging.debug(e)
        return None
    logging.debug(bot_response)
    return bot_response


@logger_config.logger
def timezone_suggestion(location_text, tz_option="time"):
    """Get time / Get timezone."""
    try:
        timezone_name, time_in_tz = googleMapsApiModule.timezone(location_text)
    except Exception as e:
        logging.debug(e)
        return None
    if tz_option == "timezone":
        logging.debug(timezone_name)
        return timezone_name
    if tz_option == "time":
        logging.debug(time_in_tz)
        return time_in_tz


@logger_config.logger
def elevation_suggestion(location_text, location_comp_text=None):
    """Find elevation of a place."""
    try:
        location_elev = googleMapsApiModule.elevation(location_text)
    except Exception as e:
        logging.debug(e)
        return None
    if location_comp_text:
        try:
            location_comp_elev = googleMapsApiModule.elevation(location_comp_text)
        except Exception as e:
            logging.debug(e)
            return None
        logging.debug(location_elev, location_comp_elev)
        return (
            str(float(location_elev[:-6]) - float(location_comp_elev[:-6])) + " metres"
        )
    logging.debug(location_elev)
    return location_elev


@logger_config.logger
def mapsstatic_suggestion(location_text, **kwargs):
    """Map of someplace (**kwargs => zoom, size)."""
    try:
        bot_response = googleMapsApiModule.mapsstatic(location_text, **kwargs)
    except Exception as e:
        logging.debug(e)
        return None
    logging.debug(bot_response)
    return bot_response

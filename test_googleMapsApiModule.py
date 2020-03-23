import googleMapsApiModule
import config
import pytest
from googlemaps.exceptions import ApiError
 
class TestClass:
    def test_direction_with_valid_input(self):
        result = googleMapsApiModule.direction('paris','brussels')
        assert result == "https://www.google.com/maps/dir/?api=1&origin=paris&destination=brussels"

    def test_direction_with_invalid_input(self):
        with pytest.raises(ApiError):
            result = googleMapsApiModule.direction('kjajw','qwiuq')
            assert result == "https://www.google.com/maps/dir/?api=1&origin=kjajw&destination=qwiuq"

    def test_geocoding_with_valid_input(self):
        result = googleMapsApiModule.geocoding('denver')
        assert result == "https://www.google.com/maps/search/?api=1&query=denver"

    def test_geocoding_with_invalid_input(self):
        with pytest.raises(IndexError):
            result = googleMapsApiModule.geocoding('kahakd...')
            assert result == "https://www.google.com/maps/search/?api=1&query=kahakd..."

    def test_mapsstatic_with_valid_input(self):
        result = googleMapsApiModule.mapsstatic('sydney')
        assert result == "https://maps.googleapis.com/maps/api/staticmap?center=sydney&zoom=13&scale=1&size=600x350&maptype=roadmap&key="+config.key+"&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7Csydney"

    def test_elevation_with_valid_input(self):
        result = googleMapsApiModule.elevation('moscow')
        assert type(result) is float

    def test_elevation_with_invalid_input(self):
        with pytest.raises(IndexError):
            result = googleMapsApiModule.elevation('hihih')
            assert type(result) is float
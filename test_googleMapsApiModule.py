import googleMapsApiModule
import config
import pytest
from googlemaps.exceptions import ApiError


class TestClass:
    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_direction_with_valid_input(self):
        result = googleMapsApiModule.direction("paris", "brussels")
        assert (
            result
            == "https://www.google.com/maps/dir/?api=1&origin=paris&destination=brussels"
        )

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_direction_with_invalid_input(self):
        with pytest.raises(ApiError):
            result = googleMapsApiModule.direction("kjajw", "qwiuq")
            assert (
                result
                == "https://www.google.com/maps/dir/?api=1&origin=kjajw&destination=qwiuq"
            )

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_geocoding_with_valid_input(self):
        result = googleMapsApiModule.geocoding("denver")
        assert result == "https://www.google.com/maps/search/?api=1&query=denver"

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_geocoding_with_invalid_input(self):
        with pytest.raises(IndexError):
            result = googleMapsApiModule.geocoding("kahakd...")
            assert result == "https://www.google.com/maps/search/?api=1&query=kahakd..."

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_mapsstatic_with_valid_input(self):
        result = googleMapsApiModule.mapsstatic("sydney")
        assert (
            result
            == "https://maps.googleapis.com/maps/api/staticmap?center=sydney&zoom=13&scale=1&size=600x350&maptype=roadmap&key="
            + config.key
            + "&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7Csydney"
        )

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_elevation_with_valid_input(self):
        result = googleMapsApiModule.elevation("moscow")
        assert type(result) is float

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_elevation_with_invalid_input(self):
        with pytest.raises(IndexError):
            result = googleMapsApiModule.elevation("hihih")
            assert type(result) is float

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_places_with_valid_input(self):
        result = googleMapsApiModule.places("princeton university")
        assert result == "ChIJ6baYzdjmw4kRTwKQ-tZ-ugI"

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_places_with_invalid_input(self):
        with pytest.raises(IndexError):
            result = googleMapsApiModule.places("esffsf")
            assert (
                result
                == "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CmRaAAAA8o1VGVvds8zkqh745Pa6t2KcBbMA&key="  # noqa: E501
                + config.key
            )

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_timezone_with_valid_input(self):
        result = googleMapsApiModule.timezone("ohio", "2000 11 21 11 41")
        assert result == "America/New_York"

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_timezone_with_invalid_input(self):
        with pytest.raises(ValueError):
            result = googleMapsApiModule.timezone("wijd..", "2000 18 21 11 41")
            assert result == "America/New_York"

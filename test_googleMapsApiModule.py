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
        result = googleMapsApiModule.geocoding("Nairobi")
        assert (
            result
            == "https://maps.google.com/?q=Nairobi,+Kenya&ftid=0x182f1172d84d49a7:0xf7cf0254b297924c"
        )

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
            == "https://maps.googleapis.com/maps/api/staticmap?center=sydney&zoom=13&size=600x350&key="
            + config.key
        )

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_elevation_with_valid_input(self):
        result = googleMapsApiModule.elevation("moscow")
        assert result.endswith("metres")

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_elevation_with_invalid_input(self):
        with pytest.raises(IndexError):
            result = googleMapsApiModule.elevation("hihih")
            assert type(result) is str

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_places_with_valid_input(self):
        result = googleMapsApiModule.places("princeton university")
        assert result == {
            "Princeton University": "https://maps.google.com/?cid=196608995535880783"
        }

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_places_with_invalid_input(self):
        result = googleMapsApiModule.places("esffsf")
        assert result == {}

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_timezone_with_valid_input(self):
        result = googleMapsApiModule.timezone("ohio")
        assert result[0] == "America/New_York"

    @pytest.mark.skipif(googleMapsApiModule.gmaps is None, reason="No API key provided")
    def test_timezone_with_invalid_input(self):
        with pytest.raises(IndexError):
            result = googleMapsApiModule.timezone("feggergw")
            assert result[0] == "America/New_York"

import googleMapsApiModule
import config
import pytest

@pytest.mark.parametrize('source,destination',
                                            [
                                                ('paris','brussels'),    ## Add places for testing here
                                                ('denver','boston'),
                                                ('efef','weufhw')
                                            ])
class TestClass:
    def test_direction(self,source,destination):
        result = googleMapsApiModule.direction(source,destination)
        assert result == "https://www.google.com/maps/dir/?api=1&origin="+source+"&destination="+destination

    def test_geocoding(self,source,destination):
        result = googleMapsApiModule.geocoding(source)
        assert result == "https://www.google.com/maps/search/?api=1&query="+source

    def test_mapsstatic(self,source,destination):
        result = googleMapsApiModule.mapsstatic(source)
        assert result == "https://maps.googleapis.com/maps/api/staticmap?center="+source+"&zoom=13&scale=1&size=600x350&maptype=roadmap&key="+config.key+"&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:L%7C"+source

    def test_elevation(self,source,destination):
        result = googleMapsApiModule.elevation(source)
        assert type(result) is float


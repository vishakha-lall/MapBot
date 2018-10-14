#converts given geographical coordinates to nearest Address
import googlemaps
import webbrowser
import config

gmaps = googlemaps.Client(key=config.key)
coordinates = [x for x in input("Enter latitude and longitude: ").split()];
result = gmaps.reverse_geocode(coordinates)
print("Formatted Address: "+result[0]['formatted_address'])
result_address=result[0]['formatted_address']
result_address = result_address.lower()
result_address = result_address.replace(" ","+")
url = "https://www.google.com/maps/search/?api=1&query="
result_url = url+result_address
webbrowser.open_new(result_url)

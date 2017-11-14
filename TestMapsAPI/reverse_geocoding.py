#converts given geographical coordinates to nearest Address
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDK7i8tLOzpfgaSVg1bZ-4cQGOXfi_IfTg')
coordinates = [x for x in input("Enter latitude and longitude: ").split()];
result = gmaps.reverse_geocode(coordinates)
print("Formatted Address: "+result[0]['formatted_address'])

#converts a given address to geographical coordinates
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDK7i8tLOzpfgaSVg1bZ-4cQGOXfi_IfTg')
address=str(input("Enter the search location: "))
result = gmaps.geocode(address)
print("Formatted Address: "+result[0]['formatted_address'])
print("Latitude: "+str(result[0]['geometry']['location']['lat'])+" "+"Longitude: "+str(result[0]['geometry']['location']['lng']))

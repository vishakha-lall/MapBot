#calculates travel distance and time between two locations
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDK7i8tLOzpfgaSVg1bZ-4cQGOXfi_IfTg')
origin = str(input("Enter the origin location: "))
destination = str(input("Enter the destination location: "))
result = gmaps.distance_matrix(origin,destination) #other attributes
print("The distance between the given loactions is "+str(result['rows'][0]['elements'][0]['distance']['text'])+" and the approximate travelling time is "+str(result['rows'][0]['elements'][0]['duration']['text']))

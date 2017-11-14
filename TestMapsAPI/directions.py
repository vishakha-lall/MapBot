#calculates the directions from origin to destination
import googlemaps
import webbrowser
gmaps = googlemaps.Client(key='AIzaSyDK7i8tLOzpfgaSVg1bZ-4cQGOXfi_IfTg')
origin = str(input("Enter the origin location: "))
destination = str(input("Enter the destination location: "))
result = gmaps.directions(origin,destination) #other attributes
print("Total distance: "+str(result[0]['legs'][0]['distance']['text']))
print("Calculated duration: "+str(result[0]['legs'][0]['duration']['text']))
print("Steps: ")
for i in range(len(result[0]['legs'][0]['steps'])):
    print("Step "+str(i+1)+" "+str(result[0]['legs'][0]['steps'][i]['html_instructions']))
    print("Continue this step for "+str(result[0]['legs'][0]['steps'][i]['distance']['text'])+" and an approximate of "+str(result[0]['legs'][0]['steps'][i]['duration']['text']))
    print("")
address = "origin="+origin+"&"+"destination="+destination
address = address.lower()
address = address.replace(" ","+")
url = "https://www.google.com/maps/dir/?api=1&"
result_url = url+address
print(result_url)
webbrowser.open_new(result_url)

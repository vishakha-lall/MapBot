def direction(origin,destination):
    import googlemaps
    import webbrowser
    gmaps = googlemaps.Client(key='AIzaSyDK7i8tLOzpfgaSVg1bZ-4cQGOXfi_IfTg')
    result = gmaps.directions(origin,destination) #other attributes
    #print("Total distance: "+str(result[0]['legs'][0]['distance']['text']))
    #print("Calculated duration: "+str(result[0]['legs'][0]['duration']['text']))
    #print("Steps: ")
    #for i in range(len(result[0]['legs'][0]['steps'])):
    #    print("Step "+str(i+1)+" "+str(result[0]['legs'][0]['steps'][i]['html_instructions']))
    #    print("Continue this step for "+str(result[0]['legs'][0]['steps'][i]['distance']['text'])+" and an approximate of "+str(result[0]['legs'][0]['steps'][i]['duration']['text']))
    #    print("")
    address = "origin="+origin+"&"+"destination="+destination
    address = address.lower()
    address = address.replace(" ","+")
    url = "https://www.google.com/maps/dir/?api=1&"
    result_url = url+address
    print(result_url)
    webbrowser.open_new(result_url)

def add_to_maps_database(origin,destination):
    import config
    import mysql.connector
    db = mysql.connector.connect(user=config.user,password=config.password,host=config.host,database=config.database)
    cur = db.cursor()
    cur = db.cursor(buffered=True)
    if destination == "":
        cur.execute("INSERT INTO directions_table(origin_location) VALUES (%s)",(origin,))
        db.commit()
    elif origin == "":
        cur.execute("SELECT id FROM directions_table ORDER BY id DESC")
        res = cur.fetchone()
        last_id = res[0]
        cur.execute('UPDATE directions_table SET destination_location=%s WHERE id=%s',(destination,last_id))
        db.commit()
    else:
        cur.execute("INSERT INTO directions_table(origin_location,destination_location) VALUES (%s,%s)",(origin,destination))
        db.commit()

def get_from_maps_database():
    import config
    import mysql.connector
    db = mysql.connector.connect(user=config.user,password=config.password,host=config.host,database=config.database)
    cur = db.cursor()
    cur = db.cursor(buffered=True)
    cur.execute("SELECT id FROM directions_table ORDER BY id DESC")
    res = cur.fetchone()
    last_id = res[0]
    cur.execute('SELECT origin_location FROM directions_table WHERE id=%s', (last_id,))
    res = cur.fetchone()
    origin = res[0]
    cur.execute('SELECT destination_location FROM directions_table WHERE id=%s', (last_id,))
    res = cur.fetchone()
    destination = res[0]
    return origin,destination

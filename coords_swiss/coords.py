import requests

def get_coords(message_raw=str):
    url = "https://api3.geo.admin.ch/rest/services/api/SearchServer?type=locations&searchText="

    #Datum absplitten
    splitm = message_raw.split(";")
    dateandtime = splitm[0].split(" ")
    date = dateandtime[0].lstrip()
    time = dateandtime[1].lstrip()
    #Meldung splitten
    message = splitm[1].split(",")
    print(message)
    if message[0].lstrip() == "Nachalarmierung":
        # Meldung ist eine Nachalarmierung
        dispo = message[0].lstrip() + ", " + message[1].lstrip() 
        incity = message[2].lstrip()
        city = incity.split(" ")[1]
        address_all = message[3].lstrip()
        if " " in address_all:
            address = address_all.split(" ")
            street = address[0].lstrip()
            house = address[1].lstrip()
        else:
            street = address_all
            house = ""
        if len(message) >= 5:
            add1 = message[4].lstrip()
        else:
            add1 = ""
        if len(message) >= 6:
            add2 = message[5].lstrip()
        else:
            add2 = ""
        if len(message) >= 7:
            add3 = message[6].lstrip()
        else:
            add3 = ""
    else:
        # Meldung ist keine Nachalarmierung
        dispo = message[0].lstrip()
        incity = message[1].lstrip()
        city = incity.split(" ")[1]
        address_all = message[2].lstrip()
        if " " in address_all:
            address = address_all.split(" ")
            street = address[0].lstrip()
            house = address[1].lstrip()
        else:
            street = address_all
            house = ""
        if len(message) >= 4:
            add1 = message[3].lstrip()
        else:
            add1 = ""
        if len(message) >= 5:
            add2 = message[4].lstrip()
        else:
            add2 = ""
        if len(message) >= 6:
            add3 = message[5].lstrip()
        else:
            add3 = ""
    
    params =  {"date": date, "time": time, "dispo": dispo, "city": city, "street": street, "house": house, "add1": add1, "add2": add2, "add3": add3}
    content = requests.get(url + params['street'] + "%20" + params['house'] + "%20" + params['city'])
    if not "fuzzy" in content.json():
        c = content.json()['results'][0]
        return params | {"lat": c['attrs']['lat'], "lon": c['attrs']['lon']}
    else:
        return params
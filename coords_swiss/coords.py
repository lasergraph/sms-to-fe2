import requests

#smsmessage = "18.06.2023 21:58; BMA, in Unterentfelden, Fliederweg 18, Rauch aus dem Dach, 3-Fam Haus"
#smsmessage = "07.08.2023 10:52; Sprinkler, in Oberentfelden, Industriestrasse 50, Müller Immobileien Betriebszentrale,"

def get_coords(message_raw = str):
    url = "https://api3.geo.admin.ch/rest/services/api/SearchServer?type=locations&searchText="

    splitm = message_raw.split(";")
    dateandtime = splitm[0].split(" ")
    date = dateandtime[0].lstrip()
    time = dateandtime[1].lstrip()
    message = splitm[1].split(",")
    dispo = message[0].lstrip()
    incity = message[1].lstrip()
    city = incity.split(" ")[1]
    address_all = message[2].lstrip()
    address = address_all.split(" ")
    street = address[0].lstrip()
    house = address[1].lstrip()
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
        print("https://www.google.com/maps/search/?api=1&query=" + str(c['attrs']['lat']) + "," + str(c['attrs']['lon']))
        return params | {"lat": str(c['attrs']['lat']), "lon": str(c['attrs']['lon'])}
    else:
        return params

# coords = get_coords(smsmessage)
# print(coords)
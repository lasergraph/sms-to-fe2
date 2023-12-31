import subprocess
from datetime import datetime
import time
import requests
import coords

#Variabeln
url = "http://192.168.1.231/rest/external/http/alarm/v2"
dispositiv = ["BMA", "Brand-Klein", "Brand-Mittel", "Brand-Gross", "Elementarereignis", "Oel-, Benzin-, Chemie", "Techn. Hilfeleistung", "Verkehrsregelung", "Stützpunkt", "Nachalarmierung", "Strassenrettung", "NTP Inbetriebnahme", "Sprinkler"]
city = ["Oberentfelden", "Unterentfelden", "Muhen", "Aarau", "Kölliken", "Hirschthal", "Schöftland", "Holziken", "Unterkulm", "Gränichen", "Suhr", "Buchs"]

#Prüfen ob Ortsnamen im Alarmtext vorhanden
def check_city(test: str, city: list):
    for c in city:
        if c in test:
            return True
    return False
        
#Prüfen ob Dispositiv Alarmtext vorhanden      
def check_dispo(test: str, dispositiv:list):
    for c in dispositiv:
        if c in test:
            return True
    return False

#Prüfen ob SMS vorhanden sind.
def get_sms_used():
	rcmd = subprocess.check_output(["gsmctl", "-S", "-t"])
	tt = rcmd.decode().split("\n")
    
	for s in tt:
		if "Used" in s:
			if s.split(" ")[1] == "0":
				return False
			else:
				return True
               
#Neue SMS abrufen
def get_new_sms():
	rcmd = subprocess.check_output(["gsmctl", "-S", "-r", "0"])
	tt = rcmd.decode().split("\n")
	
	for s in tt:
		if "Date" in s:
			smsdate = datetime.strptime(s.split("\t")[2],"%a %b %d %H:%M:%S %Y")
			timestamp = smsdate.strftime("%Y-%m-%dT%H:%M:%S+02:00")
						
	for s in tt:
		if "Sender" in s:
			sender = s.split("\t")[2]
			
	for s in tt:
		if "Status" in s:
			status = s.split("\t")[2]

	for s in tt:
		if "Text" in s:
			text = s.split("\t")[2]
			
	return {"timestamp": timestamp, "sender": sender, "status": status, "text": text}

# Senden des Alarms ohne Koordinaten an Server via HTTP POST Request
def send_alarm_fallback(alarm: dict, url: str):
	# Fallback ohne Koordinaten
	request_data = { 
		'type': "ALARM",
		'timestamp': alarm["timestamp"],
		'sender': alarm["sender"],
		'authorization': alarm["sender"],
		'data': { 
			'message': [
				alarm["text"]
			]
		}
	}
	#Senden Request an FE2 Server
	r = requests.post(url, json = request_data)
	return r

# Senden des Alarms mit Koordinaten an Server via HTTP POST Request
def send_alarm_coord(alarm: dict, url: str, params: dict):
	# Koordinaten im Gebäudeverziechnis gefunden 
	request_data = { 
		'type': "ALARM",
		'timestamp': alarm["timestamp"],
		'sender': alarm["sender"],
		'authorization': alarm["sender"],
		'data': { 
			'message': [
				alarm["text"]
			],
			"location": {
				"coordinate": [
					params["lon"],
					params["lat"]
				],
				"street": params["street"],
				"house": params["house"],
				"city": params["city"]
				},
		}
	}
	#Senden Request an FE2 Server
	r = requests.post(url, json = request_data)
	return r

# Main while Loop
while True:
	new_sms = get_sms_used() #Prüfen auf neue SMS
	if new_sms:
		alarm = get_new_sms() #Neue SMS abrufen
		dispo = check_dispo(alarm["text"], dispositiv)
		if dispo:
			params = coords.get_coords(alarm["text"]) #Koordinaten abrufen
			if "lat" in params: 
				send_alarm_coord(alarm, url, params) #Alarm mit Koordinaten an FE2 senden
			else:
				send_alarm_fallback(alarm, url) #Alarm Koordinaten an FE2 senden
		else:
			send_alarm_fallback(alarm, url) #Alarm ohne Dispo und Koordinaten an FE2 senden 

		subprocess.check_output(["gsmctl", "-S", "-d", "0"]) #SMS löschen
		
	time.sleep(1) 


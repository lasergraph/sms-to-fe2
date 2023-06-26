import subprocess
from datetime import datetime
import time
import requests

#Variabeln
url = "http://192.168.1.231/rest/external/http/alarm/v2"

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
	
# Senden des Alarms an Server via HTTP POST Request
def send_alarm(alarm, url):
	#POST Request erstellen
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


while True:
	new_sms = get_sms_used() #Prüfen auf neue SMS
	if new_sms:
		alarm = get_new_sms() #Neue SMS abrufen
		subprocess.check_output(["gsmctl", "-S", "-d", "0"]) #SMS löschen
		send_alarm(alarm, url) # Alarm an FE2 senden
		
	time.sleep(1) 

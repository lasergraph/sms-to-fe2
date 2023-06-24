import subprocess
from datetime import datetime
import time
import requests
import math

#Variabeln
url = "http://192.168.1.231/rest/external/http/alarm/v2"
now = datetime.now()
refdates = [[2022, 1, 31], [2022, 2, 7], [2022, 2, 14], [2022, 2, 21], [2022, 2, 28], [2022, 3, 7]]

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
	
	
def send_alarm(alarm, url, week):
	#POST Request erstellen
	request_data = { 
		'type': "ALARM",
		'timestamp': alarm["timestamp"],
		'sender': alarm["sender"],
		'authorization': alarm["sender"],
		'data': { 
			'message': [
				alarm["text"]
			],
			'custom': {
				'week': str(week)
      		}	
		}
	}
	
	#Senden Request an FE2 Server
	r = requests.post(url, json = request_data)


#Aktuelle Alarmwoche ermitteln
def get_week(now, refdates):
    for refdate in refdates:
        ref = datetime(refdate[0], refdate[1], refdate[2], 7, 0, 0)    
        delta = now - ref
        r = delta.days/42 - math.floor(delta.days/42)
        if r < 0.166666:
            return refdates.index(refdate)+1





while True:
	new_sms = get_sms_used() #Prüfen auf neue SMS
	if new_sms:
		alarm = get_new_sms() #Neue SMS abrufen
		subprocess.check_output(["gsmctl", "-S", "-d", "0"]) #SMS löschen
		week = get_week(now, refdates) #Wochennummer ermitteln
		send_alarm(alarm, url, week) # Alarm an FE2 senden
		
	time.sleep(1) 


#Alarm_Function for KNZ Aargau // Mokos // Feuerwehr Entfelden-Muhen
# Copyright 2023 by Roman Mauchle (Feuerwehr Entfelden-Muhen)

#Librarys
from datetime import datetime
import math

### Basic Configuration ###

#Startdates for 6 Weeks
refdates = [[2022, 1, 31], [2022, 2, 7], [2022, 2, 14], [2022, 2, 21], [2022, 2, 28], [2022, 3, 7]]

timetable = [
    {"Kdo": "Kommandogruppe 1", "Gruppe1": "Gruppe 1", "Gruppe2": "Gruppe 3", "Subgruppe": "Subgruppe 3a"}, #Woche1
    {"Kdo": "Kommandogruppe 2", "Gruppe1": "Gruppe 1", "Gruppe2": "Gruppe 2", "Subgruppe": "Subgruppe 1b"}, #Woche2
    {"Kdo": "Kommandogruppe 1", "Gruppe1": "Gruppe 2", "Gruppe2": "Gruppe 3", "Subgruppe": "Subgruppe 2b"}, #Woche3
    {"Kdo": "Kommandogruppe 2", "Gruppe1": "Gruppe 1", "Gruppe2": "Gruppe 3", "Subgruppe": "Subgruppe 3b"}, #Woche4
    {"Kdo": "Kommandogruppe 1", "Gruppe1": "Gruppe 1", "Gruppe2": "Gruppe 2", "Subgruppe": "Subgruppe 1a"}, #Woche5
    {"Kdo": "Kommandogruppe 2", "Gruppe1": "Gruppe 2", "Gruppe2": "Gruppe 3", "Subgruppe": "Subgruppe 2a"}  #Woche6
]

dispositiv = {
    "Brand-Klein": ["Kdo", "Subgruppe"],
    "Brand-Mittel": ["Kommandogruppe 1", "Kommandogruppe 2", "Gruppe1","Gruppe2", "Sanitätsgruppe"],
    "Brand-Gross": ["Kommandogruppe 1", "Kommandogruppe 2", "Gruppe 1", "Gruppe 2", "Gruppe 3", "Sanitätsgruppe"],
    "BMA": ["Kdo", "Subgruppe"],
    "Sprinkler": ["Kdo", "Subgruppe"],
    "Elementarereignis": ["Kdo"],
    "Oel-, Benzin-, Chemie": ["Kdo", "Subgruppe"],
    "Techn. Hilfeleistung": ["Kdo"], 
    "Verkehrsregelung" : ["Verkersgruppe"],
    "Strassenrettung": ["Strassenrettung"],
    "NTP Inbetriebnahme": ["Notfalltreffpunkte"]
}

week_test = {
    "Brand-Klein": ["Kdo", "Subgruppe"],
    "Brand-Mittel": ["Gruppe1", "Gruppe2"],
    "Brand-Gross": [],
    "BMA": ["Kdo", "Subgruppe"],
    "Sprinkler": ["Kdo", "Subgruppe"],
    "Elementarereignis": ["Kdo"],
    "Oel-, Benzin-, Chemie": ["Kdo", "Subgruppe"],
    "Techn. Hilfeleistung": ["Kdo"],
    "Verkehrsregelung" : [],
    "Strassenrettung": [],
    "NTP Inbetriebnahme": []
}

### Functions ###

def get_week(now, refdates):
    for refdate in refdates:
        ref = datetime(refdate[0], refdate[1], refdate[2], 7, 0, 0)    
        delta = now - ref
        r = delta.days/42 - math.floor(delta.days/42)
        if r < 0.166666:
            return refdates.index(refdate)+1
        
def get_einheiten(keyword, week):
    r = []
    for d in dispositiv[keyword]:    
        if d in week_test[keyword]:
            r.append(timetable[week-1][d])
        else:
            r.append(d)
    return r

def get_keyword(message):
    for dispo in dispositiv:
        if dispo in message:
            return dispo
        
def get_einheiten_now(message):
    return get_einheiten(get_keyword(message), get_week(datetime.now(), refdates))
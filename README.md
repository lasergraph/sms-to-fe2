# sms-to-fe2
Erweitert den Funktionsumfang eines [Teltonika TRB140](https://teltonika-networks.com/products/gateways/trb140) Gateway das Eingehende SMS als Alarm über die Externe Schnittstelle an einen Alamos FE2 Server gesendet werden können.

## Installation 
- main.py auf TRB140 in Ordner /root/ speichern.(SFTP)
- sms-to-fe2 auf TRB140 in Ordner /etc/init.d/ speichern.(SFTP)
- sms-to-fe2 ausführbar machen ```chmod +x /etc/init.d/sms-to-fe2```
- Sonderzeichen entfernen. ```sed -i -e 's/\r//g' /etc/init.d/sms-to-fe2```
- PiP installieren. ```opkg install python3-pip```
- Pythonmodule Requests und DateTime installieren. ```pip install reguests datetime``` 
- Service aktivieren. ```/etc/init.d/sms-to-fe2 enable```
- Service starten. ```/etc/init.d/sms-to-fe2 start```

## Konfiguration
- In der main.py muss die IP-Adresse des FE2 Server in der Variable ```url``` angepasst werden.
  z.B. ```http://192.168.1.231/rest/external/http/alarm/v2```

## Unterstütztes SMS Schema 
Folgendes SMS Schema wird unterstützt:<br>
- *Datum Zeit*; *Dispositv*, in *Ort*, *Adresse*, *Zusatzinformation 1*, *Zusatzinformation 2*<br>
Dies entspricht dem SMS Schema wie sie im Kanton Aargau von der KNZ(Kantonale Notrufzentrale) verwendet wird.

## Ermitteln der Einsatz-Koordinaten
Für die Schweiz gibt es die Möglichkeit die Koordinaten der enthaltenen Einsatzadresse im [Amtlichen Verzeichnis der Gebäudeadressen](https://www.swisstopo.admin.ch/de/geodata/amtliche-verzeichnisse/gebaeudeadressenverzeichnis.html) abzufragen und an den FE2 Server zu übermitteln.<br>
Dazu müssen die Python Dateien im Ordner coords_swiss verwendet werden. 

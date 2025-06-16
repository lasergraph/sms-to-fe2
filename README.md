# sms-to-fe2
Erweitert den Funktionsumfang eines [Teltonika TRB140](https://teltonika-networks.com/products/gateways/trb140) Gateway das Eingehende SMS als Alarm über die Externe Schnittstelle an einen Alamos FE2 Server gesendet werden können.

## Installation 
### Firmware TRB_R_00.07.04.5
- [basic/main.py](https://github.com/lasergraph/sms-to-fe2/tree/main/basic) auf TRB140 in Ordner /root/ speichern.(sFTP)
- sms-to-fe2 auf TRB140 in Ordner /etc/init.d/ speichern.(sFTP)
- sms-to-fe2 ausführbar machen ```chmod +x /etc/init.d/sms-to-fe2```
- Sonderzeichen entfernen. ```sed -i -e 's/\r//g' /etc/init.d/sms-to-fe2```
- Pip installieren. ```opkg install python3-pip``` (Bei einer neueren Firmware müssen die openwrt Paketquellen hinzugefügt werden.)
- Pythonmodule Requests und DateTime installieren. ```pip install requests datetime``` 
- Service aktivieren. ```/etc/init.d/sms-to-fe2 enable```
- Service starten. ```/etc/init.d/sms-to-fe2 start```

###  Hinweis Neuere Firmware TRB1_R_00.07.06.4 und höher
In neueren Firmware sind nur noch die Teltonika Paketquellen enthalten.
Um Pip zu installieren müssen die normalen openwrt Paketquellen hinzugefügt werden.

In /etc/opkg/customfeeds.conf:
```
src/gz openwrt_core https://downloads.openwrt.org/releases/21.02.0/targets/mdm9x07/generic/packages
src/gz openwrt_base https://downloads.openwrt.org/releases/21.02.0/packages/arm_cortex-a7_neon-vfpv4/base
src/gz openwrt_luci https://downloads.openwrt.org/releases/21.02.0/packages/arm_cortex-a7_neon-vfpv4/luci
src/gz openwrt_packages https://downloads.openwrt.org/releases/21.02.0/packages/arm_cortex-a7_neon-vfpv4/packages
src/gz openwrt_routing https://downloads.openwrt.org/releases/21.02.0/packages/arm_cortex-a7_neon-vfpv4/routing
src/gz openwrt_telephony https://downloads.openwrt.org/releases/21.02.0/packages/arm_cortex-a7_neon-vfpv4/telephony
src/gz openwrt_vuci https://downloads.openwrt.org/releases/21.02.0/packages/arm_cortex-a7_neon-vfpv4/vuci
```
Danach muss ein ```opkg update``` ausgeführt werden um die Paketquellen zu aktualisieren. Danach kann Pip über die Paketquellen installiert werden.

Bei Problemen mit der Python PIP Installation über opkg kann folgender Workaround helfen ([Quelle](https://community.teltonika.lt/t/trb140-python-pip-work-around/9202)):
```
opkg remove python3-pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```
Danach können die Python Module über PIP installiert werden
```
pip install requests
```

## Konfiguration
- In der main.py muss die IP-Adresse des FE2 Server in der Variable ```url``` angepasst werden.
  z.B. ```http://192.168.1.231:83/rest/external/http/alarm/v2```

Es wird der Port verwendet über den die Weboberfäche erreichbar ist.

## Ermitteln der Einsatz-Koordinaten
Für die Schweiz gibt es die Möglichkeit die Koordinaten der enthaltenen Einsatzadresse im [Amtlichen Verzeichnis der Gebäudeadressen](https://www.swisstopo.admin.ch/de/geodata/amtliche-verzeichnisse/gebaeudeadressenverzeichnis.html) abzufragen und an den FE2 Server zu übermitteln.<br>
Dazu müssen die Python Dateien im Ordner [coords_swiss](https://github.com/lasergraph/sms-to-fe2/tree/main/coords_swiss) verwendet werden. 

### Unterstütztes SMS Schema 
Folgendes SMS Schema wird für die Ermittlung von Koordinaten unterstützt:<br>
- *Datum Zeit*; *Dispositv*, in *Ort*, *Adresse*, *Zusatzinformation 1*, *Zusatzinformation 2*<br>

Dies entspricht dem SMS Schema wie sie im Kanton Aargau von der KNZ(Kantonale Notrufzentrale) verwendet wird.

### Konfiguration TRB140 mit SIM ohne Datenoption ###
Das TRB140 leitet den Internetverkehr über das WAN. In der Default Konfiguration ist die WAN Verbindung über die SIM-Karte. Wird eine SIM-Karte ohne Datenoption verwendet muss ein weiters WAN Netzwerk hinzugefügt werden, welches den LAN Port verwendet. Dies wird über die TRB140 Konfigurationsseite gemacht:
- Network > WAN > Add
- Statische IP (nicht die gleiche Adresse wie beim LAN Port verwenden), sowie Gateway Adresse (z.B. 192.168.118.2) konfigurieren.
- Die Konfigurationsseite ist weiterhin über die IP Adresse welche unter LAN definiert wurde erreichbar.



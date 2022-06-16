import urllib.request
import requests
import time
from datetime import datetime

token = "-7cGTsSamQxC5PvY8VcXsbrhBp5Jp1"
zone = 'flo-machines.dynv6.net'
delay = 120 # 2min d'interval

ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

print("###--- Script Update Dynv6 ip_home_server ---###")
print("#- Token:", token)
print("#- Zone:", zone)
print("#- Actual IP:", ip)
print("#- Update delay:", delay)
print("#- Script lancé !")

while True:
    new_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    print("#- ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ", Check IP update: New = ", new_ip, " Old = ", ip)
    if(new_ip != ip):
        print("#-- ", new_ip, " != ", ip, " => IP update request send ...")
        requests.get(f"http://ipv4.dynv6.com/api/update?ipv4={ip}&token={token}&zone={zone}")
        ip = new_ip
    else:
        print("#-- ", new_ip, " == ", ip, " => no update.")

    time.sleep(delay)



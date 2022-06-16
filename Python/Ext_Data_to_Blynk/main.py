###--- Data ext (APIs) -> Blynk ---###
# I)   Import des modules
# II)  Définition des fonctions
# III) Définition des constantes
# IV)  Main
###

# I) Import des modules
from requests import *
from requests.auth import HTTPBasicAuth
from datetime import *

# II)  Définition des fonctions
def Convert_Cron_Date_To_dateTime(cron_date):
    # Attention les cron sont définis de la manière suivante: %d:%H:%M:%S
    # Une date au dormat datetime comporte les années et les mois => ça nous intéresse pas mais par défaut
    # l'année 1900-01 est mise, => on met donc l'année et le mois actuel pour ne pas avoir de pb
    now = datetime.now()
    y, m = now.strftime("%Y"), now.strftime("%m")
    cron_date = cron_date.split(":")
    date = datetime(int(y), int(m), int(cron_date[0]), int(cron_date[1]), int(cron_date[2]), int(cron_date[3]) )

    return date

def Dif_Date(start, end):
    try:
        delta =  start - end
    except:
        try:
            try:    start = Convert_Cron_Date_To_dateTime(start)
            except: end   = Convert_Cron_Date_To_dateTime(end)
            delta = start - end
        except:
            end = Convert_Cron_Date_To_dateTime(end)
            delta = start - end


    # Conversion delta en date
    delta = str(delta).replace("day", "").replace("s", "").replace(" ", "")
    delta = delta.replace(",", ":") if ("," in delta) else "0:" + delta
    if("." in delta): delta = str(delta.split(".")[0])

    return delta

def API_Request(url, keys):
    content = get(url)
    if content.ok:
        content = content.text.replace("null", '"null"')
        data = eval(content)
        for k in keys:
            data = data[k]
        return data

    print("#- ERROR -> Bad request:", url)
    return "null"

def Blynk_update(server, token, vpin, value):
    val = value.split(", ")
    value = val[0]
    for k in range(1, len(val)):
        value = value + "&value=" + val[k]

    url = "http://" + server + "/" + token + "/" + "update" + "/" + vpin + "?value=" + value

    content = get(url)
    if content.ok:
        return "Ok"
    print("ERROR -> Write_Virtual_Value bad request")
    return "null"

def Cron_Update(i, key):
    cron_start[i] = datetime.now()
    token = ext_data[key]["token"]
    vpin = ext_data[key]["vpin"]

    value = API_Request(ext_data[key]["url"], ext_data[key]["api_keys"])
    if (VIEW_MODE):
        print("#- Update at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "=>", key, "-§_", vpin, "_§- >", value)

    Blynk_update(server, token, vpin, value)

def Link_Update(ext_data):

    for i, key in enumerate(ext_data.keys()):
        delta = [int(i) for i in Dif_Date(datetime.now(), cron_start[i]).split(":")]
        cron  = [int(i) for i in ext_data[key]["cron"].split(":")]

        if( cron[0] <= delta[0] and cron[1] <= delta[1] and cron[2] <= delta[2] and cron[3] <= delta[3] ):

            Cron_Update(i, key)


def Get_Gaia():
    r = get("http://flo-machines.dynv6.net:1007/data", auth=HTTPBasicAuth('FI0078', "&X6e@NMf&dduA6%7qoEhbt5vM!T%R5&NWrtFrqwx8mDhmR%ZP&Uu^bR%$Aq&waNsHvi4*AopYLvs8zeAa!XCM^fHr#4Nn8!z@sq7"))
    return eval(r.text)

# III) Définition des constantes
VIEW_MODE = True

gaia = Get_Gaia()
server_info = gaia["server"]
ext_data = gaia["ext_data"]
server = server_info["names"]["public"] +":"+ server_info["ports"]["BlynkWemos"]["externe"]

# IV)  Main
noms_APIs = ""
for key in ext_data.keys():
    noms_APIs += str(key) + " | "
noms_APIs = noms_APIs[:-3]

cron_taches = ""
for key in ext_data.keys():
    cron_taches += str(key) + " -> " + ext_data[key]["cron"] + " | "
cron_taches = cron_taches[:-3]

print("###--- Script Python Data ext (APIs) -> Blynk ---###")
print("#- Server:", server)
print("#- Nb de APis ext. à lier:", len(ext_data.keys()), "/ noms: ", noms_APIs)
print("#- Cron de chaque tâche:", cron_taches)
print("#- Script lancé !")

cron_start = [datetime.now() for element in ext_data.keys()]

# On exécute tous les crons au début
for i, key in enumerate(ext_data.keys()):
    delta = [int(i) for i in Dif_Date(datetime.now(), cron_start[i]).split(":")]
    cron = [int(i) for i in ext_data[key]["cron"].split(":")]

    Cron_Update(i, key)

while True:
    Link_Update(ext_data)

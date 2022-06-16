###---V1 script support BLYNK ---###
# I)   Import des modules
# II)  Définition des constantes et des ponts à créer
# III) Définition des fonctions
# IV)  Main
###

# I)   Import des modules
import requests as r
from datetime import datetime
import math

# II)  Définition des constantes et des ponts à créer

VIEW_MODE = True

type_request = "http://"
server_name = ""  # Choisi automatiquement

chemin_link = "./Link.txt"
chemin_time = "./Time.txt"
chemin_token = "./Token.txt"


# III) Définition des fonctions
def Choix_Server(type_request, S1, S2):
    try:
        r.head(type_request + S1)
        return S1
    except:
        r.head(type_request + S2)
        return S2

def Map(x, in_min, in_max, out_min, out_max):
    val_map = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if(val_map > out_max):  return out_max
    elif(val_map < out_min): return out_min
    else: return val_map

def Find_Name(token):
    for k, val in Tk.items():
        if token == val:
            return k
    return "Token invalide"


def R_fichier(meth, name_file, data):
    with open(name_file, meth) as F:

        if (meth == "w" or meth == "a"): F.write(data)

        if (meth == "r"):
            data_file = F.read()

            return data_file


def Get_Data_File(name_file):
    Data_Link_Brut = R_fichier('r', name_file, '')  # Récupération du fichier
    Data_Link_Brut = Data_Link_Brut.replace("\n", "")  # Formatage => on retire les \n
    Data_Link_Brut = Data_Link_Brut.replace("\t", "")  # Formatage => on retire les \t
    Data_Link_Brut = Data_Link_Brut.replace(" ", "")  # Formatage => on retire les espaces
    Data_Link = eval(Data_Link_Brut)  # Evaluation de la str vers list
    return Data_Link


def Get_Time():
    Str_Time = str(datetime.now().time())
    List_Str_Time = Str_Time.split(':')
    List_Str_Time.pop()

    return List_Str_Time


def Formatage(DATA):
    DATA_Formatee = []
    # Si c'est une liste on cherche élément par élément si y'a un mauvais type
    if (type(DATA) == type([])):
        for k in range(len(DATA)):
            # Si le type est un int on le met en str
            if (type(DATA[k]) == type(10)):
                DATA[k] = str(DATA[k])
            DATA_Formatee[:] = DATA

    # Si DATA est une valeur seule on la met en str et on la met en liste
    else:
        # Si le type est un int on le met en str
        if (type(DATA) == type(10)):
            DATA = str(DATA)

        DATA_Formatee.append(DATA)

    return DATA_Formatee


def Decode_Timer_Input(Data_Brut):
    # Data shape: "sec", "", "Europe/Paris", "jour,jour,...", "7200"
    # Ex brut: ["3600  Europe/Paris 1,2,5,6,7 7200"] => delete [""]
    Data_Brut = Data_Brut.translate({ord(i): None for i in '[""]'})

    # Mise des infos sous forme de liste
    List_Data = Data_Brut.split("\x00")

    # Suppression des infos intiles, obj => ["sec", ... Jours ... ]
    List_Data.remove("Europe/Paris")
    List_Data.remove("7200")
    List_Data.remove("")

    # Convertir les sec en hh:mm
    Sec = int(List_Data[0])
    Heure = int(Sec / 3600)
    Sec = int(Sec % 3600)
    Min = int(Sec / 60)

    List_Data[0] = str(Heure) + ":" + str(Min)

    return List_Data


def Get_Vpin_Value(Token, Vpin):
    url = type_request + server_name + "/" + Token + "/" + "get" + "/" + Vpin
    content = r.get(url)
    if content.ok:
        try:
            return Formatage(content.json())
        except:
            return Formatage(content.text)

    print("ERROR -> Get_Vpin_Value bad response  (", content, " /-->", url, ")")
    return "null"


def Write_Virtual_Value(token, V, value):
    val = value.split(", ")
    value = val[0]
    for k in range(1, len(val)):
        value = value + "&value=" + val[k]

    url = type_request + server_name + "/" + token + "/update/" + V + "?value=" + value
    content = r.get(url)
    if content.ok:
        return "Ok"
    print("ERROR -> Write_Virtual_Value bad request")
    return "null"


def Update_All_State(DATA):
    for Link in DATA:

        # Récupération du nombre de Master Pin
        N = len(Link['Master_Token'])

        for Master in range(N):
            # Récupération de la valeur du Vpin
            Vpin_Value = Get_Vpin_Value(Link['Master_Token'][Master], Link['Master_Vpin'][Master])

            # Si le Vpin est vide (ex: terminal) on met une valeur pas défaut
            if (len(Vpin_Value) == 0):
                try:
                    Link['LastState'][Master] = "Valeur par defaut"
                except:
                    Link['LastState'].append("Valeur par defaut")

                Write_Virtual_Value(Link['Master_Token'][Master], Link['Master_Vpin'][Master], Link['LastState'][Master])
            else:
                Link['LastState'].append(Vpin_Value[-1])


def Link_Maker(DATA):
    # Lecture pont par pont
    for Link in DATA:

        # Récupération du Nb de Master
        N = len(Link['Master_Token'])

        # Récupération des dernières valeurs des Vpin Master + Comptage du Nb d'update
        Cpt_Update = 0
        Value = []
        for M in range(N):
            # Récupération la dernière valeur du Vpin Master
            Value.append( Get_Vpin_Value(Link['Master_Token'][M], Link['Master_Vpin'][M])[-1] )
            if (Value[M] != Link['LastState'][M]): Cpt_Update += 1


        # Si il y a eu une ou plusieurs update alors on update les esclaves sinon rien
        if(Cpt_Update != 0):

            # Check des update des Pin et on compte le Nb de conditions satisfaites
            Cpt_ON, Cpt_OFF = 0, 0
            for M in range(N):
                # 2 cas possibles: switch / push pour le Maître
                # Push mode !!(il y a que le ON)
                if(Link['Master_Mode'][M] == "push"):

                    # Il ya deux push possible: push Master donne sa valeur à Slave | push classique
                    # push classique
                    try:
                        # Vérification si le nouvel état correspond à un l'état ON enregistré
                        # 2 cas possible ON = Value | ON != Value pour activé le pont
                        # ON = Value
                        if (Value[M] == Link['Master_State'][M]['ON']):
                            Cpt_ON += 1
                            if (VIEW_MODE):
                                print(f'\n#- UPDATE: {Link["Name"]}-§_{Find_Name(Link["Master_Token"][M])}-{Link["Master_Vpin"][M]}_§- > {Link["LastState"][M]} to {Value[M]}')
                        # ON != Value
                        elif("!" in Link['Master_State'][M]['ON']):
                            # On récupère la valeur du Vpin
                            Val_Vpin = Link['Master_State'][M]['ON'].split("!")[1]
                            if(Value[M] != Val_Vpin):
                                Cpt_ON += 1
                                if (VIEW_MODE):
                                    print(f'\n#- UPDATE: {Link["Name"]}-§_{Find_Name(Link["Master_Token"][M])}-{Link["Master_Vpin"][M]}_§- > {Link["LastState"][M]} to {Value[M]}')

                    # push Master donne sa valeur à Slave
                    except:
                        if(Link['Master_State'][M] == "$"):
                            Cpt_ON += 1
                            if(VIEW_MODE):
                                print(f'\n#- UPDATE: {Link["Name"]}-§_{Find_Name(Link["Master_Token"][M])}-{Link["Master_Vpin"][M]}_§- > {Link["LastState"][M]} to {Value[M]}')


                # Switch mode !!(il y a le ON et le OFF)
                if(Link['Master_Mode'][M] == "switch"):

                    # Vérification si le nouvel état correspond à un l'état ON enregistré
                    if(Value[M] == Link['Master_State'][M]['ON']):
                        Cpt_ON += 1
                        if (VIEW_MODE):
                            print(f'\n#- UPDATE: {Link["Name"]}-§_{Find_Name(Link["Master_Token"][M])}-{Link["Master_Vpin"][M]}_§- > {Link["LastState"][M]} to {Value[M]}')


                    # Vérification si le nouvel  état correspond à un l'état OFF enregistré
                    elif (Value[M]== Link['Master_State'][M]['OFF']):
                        Cpt_OFF += 1
                        if (VIEW_MODE):
                            print(f'\n#- UPDATE: {Link["Name"]}-§_{Find_Name(Link["Master_Token"][M])}-{Link["Master_Vpin"][M]}_§- > {Link["LastState"][M]} to {Value[M]}')

                # Actualisation de la dernière valeur enregistrée
                Link['LastState'][M] = Value[M]


            # Si toutes les conditions sont remplies, on update les slaves
            # 2 cas possibles: Update du ON / Update du OFF

            # Update du ON
            if(Cpt_ON == N):
                # Actualisation de tous les esclaves
                for k in range(len(Link['Slave_Token'])):
                    # chgmt classique
                    try:
                        if (VIEW_MODE):
                            print(f'#-- {Find_Name(Link["Slave_Token"][k])} ({Link["Slave_Vpin"][k]}) > {Link["Slave_State"][k]["ON"]}')
                        Write_Virtual_Value(Link['Slave_Token'][k], Link['Slave_Vpin'][k], Link['Slave_State'][k]['ON'])


                    # chgmt Master donne sa valeur à Slave
                    except:
                        # chgmt Master donne sa valeur à Slave
                        if (Link['Slave_State'][k].count("$") == 1):

                            M_to_S_Value = Link["Slave_State"][k].replace("$", str(Link['LastState'][k]))

                            if (VIEW_MODE):
                                print(f'#-- {Find_Name(Link["Slave_Token"][k])} ({Link["Slave_Vpin"][k]}) > {M_to_S_Value} ')

                            Write_Virtual_Value(Link['Slave_Token'][k], Link['Slave_Vpin'][k],M_to_S_Value)

                        # chgmt Master donne sa valeur à Slave avec Produit en croix, mode classique
                        elif (Link['Slave_State'][k].count("$") == 2):

                            F_Map = (Link['Slave_State'][k].split("$"))[1].split(",")
                            try:
                                Val = Map(float(Link['LastState'][k]), float(F_Map[0]), float(F_Map[1]), float(F_Map[2]), float(F_Map[3]))
                                Val = str(Val)
                            except:
                                Val = Map(int(float(Link['LastState'][k])), int(float(F_Map[0])), int(float(F_Map[1])), int(float(F_Map[2])), int(float(F_Map[3])))
                                Val = str(math.ceil(Val))

                            if (VIEW_MODE):
                                print(f'#-- {Find_Name(Link["Slave_Token"][k])} ({Link["Slave_Vpin"][k]}) > {Val} ')

                            Write_Virtual_Value(Link['Slave_Token'][k], Link['Slave_Vpin'][k], Val)

                        # chgmt Master donne sa valeur à Slave avec Produit en croix, mode arrondi
                        elif (Link['Slave_State'][k].count("$") == 3):

                            Round = (Link['Slave_State'][k].split("$"))[1]
                            F_Map = (Link['Slave_State'][k].split("$"))[2].split(",")

                            try:
                                Val = Map(float(Link['LastState'][k]), float(F_Map[0]), float(F_Map[1]),
                                          float(F_Map[2]), float(F_Map[3]))
                            except:
                                Val = Map(int(float(Link['LastState'][k])), int(float(F_Map[0])), int(float(F_Map[1])),
                                          int(float(F_Map[2])), int(float(F_Map[3])))
                            print(Round, F_Map, Val)
                            if (Round == "0"):
                                Val = str(math.ceil(Val))
                            elif (Round == "1"):
                                Val = str(float(Val))

                            if (VIEW_MODE):
                                print(f'#-- {Find_Name(Link["Slave_Token"][k])} ({Link["Slave_Vpin"][k]}) > {Val} ')

                            Write_Virtual_Value(Link['Slave_Token'][k], Link['Slave_Vpin'][k], Val)


            # Update du OFF
            if(Cpt_OFF == N):
                # Actualisation de tous les esclaves
                for k in range(len(Link['Slave_Token'])):

                    if (VIEW_MODE): print(f'#-- {Find_Name(Link["Slave_Token"][k])} ({Link["Slave_Vpin"][k]}) > {Link["Slave_State"][k]["OFF"]} ')
                    Write_Virtual_Value(Link['Slave_Token'][k], Link['Slave_Vpin'][k], Link['Slave_State'][k]['OFF'])

def Time_Link_Maker(DATA):
    # On recupère l'heure (Time = [ heure, minute ]
    Time = Get_Time()

    # Lecture pont par pont
    for Link in DATA:
        # On recupère l'heure d'activation (Start_Time = [ heure, minute ]
        Start_Time = Link['Start_Time']
        Start_Time = Start_Time.split(':')

        # Activation de l'automatisation si hh == hh et que min == min et que Anti_Repeat == 1 (permet d'éviter que l'animation s'opère en boucle toute la durée de la minute)
        if (Time[0] == Start_Time[0] and Time[1] == Start_Time[1] and Link['Anti_Repeat']):

            # Link['Anti_Repeat'] => 0 pour éviter la répétition de l'animation
            Link['Anti_Repeat'] = False

            # Récupération du Nb de Master
            N = len(Link['Master_Token'])

            # Récupération des dernières valeurs des Vpin Master + Comptage du nombre du Nb de conditions satisfaites
            Cpt_Conditions = 0
            Value = []
            for M in range(N):
                # Récupération la dernière valeur du Vpin Master
                Value.append(Get_Vpin_Value(Link['Master_Token'][M], Link['Master_Vpin'][M])[-1])

                if(Value[M] == Link['Master_State'][M]): Cpt_Conditions += 1

            # Si toutes les conditions satisfaites
            if(Cpt_Conditions == N):
                for k in range(len(Link['Slave_Token'])):

                    if (VIEW_MODE):
                        print(f'#-- {Find_Name(Link["Slave_Token"][k])} ({Link["Slave_Vpin"][k]}) > {Link["Slave_State"][k]} ')

                    Write_Virtual_Value(Link['Slave_Token'][k], Link['Slave_Vpin'][k], Link['Slave_State'][k])

        elif (Time[0] != Start_Time[0] and Time[1] != Start_Time[1]):
            Link['Anti_Repeat'] = True


# IV)  Main
# On choisit le serveur approprié
server_name = Choix_Server(type_request, "localhost:8080", "flo-machines.dynv6.net:1004") # 92.151.59.2:1004 localhost:8080
# Récupération de toutes les infos sur: les tokens | les ponts | les animations de temps
# Infos sur les Tokens
Tk = Get_Data_File(chemin_token)

# Infos Ponts
Data_Link = Get_Data_File(chemin_link)

# Infos Automatisation de temps
Data_Time = Get_Data_File(chemin_time)

# Affichage du début: infos générales sur les données fournies
# Assemblage des noms de tokens, d'automatisations horaires et de ponts
Tokens_name = ""
for X in Tk.keys():
    Tokens_name += X + " | "
Tokens_names = Tokens_name[:-3]

Links_name = ""
for X in Data_Link:
    Links_name += X['Name'] + " | "
Links_Names = Links_name[:-3]

Times_name = ""
for X in Data_Time:
    Times_name += X['Name'] + " | "
Times_Names = Times_name[:-3]

print("###--- Script Python Blynk ---###")
print("#- Server:", server_name)
print("#- Nb de tokens renseignés:", len(Tk.keys()), "/ noms: ", Tokens_names)
print("#- Nb de ponts actifs:", len(Data_Link), "/ noms: ", Links_Names)
print("#- Nb d'automatisations horaires actifs:", len(Data_Time), "/ noms: ", Times_Names)
print("#- Script lancé !")

# On récupère les valeurs de tous les Vpin
Update_All_State(Data_Link)

# Boucle infini qui va vérifier en permanence s'il y a des updates
while True:
    # Fonction qui crée les ponts
    Link_Maker(Data_Link)
    Time_Link_Maker(Data_Time)

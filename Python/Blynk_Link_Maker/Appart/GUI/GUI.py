# I)   Librairies
import tkinter as tkt
from math import *
#https://www.cours-gratuit.com/tutoriel-python/tutoriel-python-personnaliser-les-widgets-avec-tkinter#_Toc52998646
#https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# Attention fonctionnement de tk (liste Token est incompatible)

# II)  Variables Globales
# 1°) Data Path
chemin_link  = "../Link.txt"
chemin_time  = "../Time.txt"
chemin_token = "../Token.txt"

# 2°) Caractéristiques esthétiques
GUI_Properties = {
    "title"     : "Domotique",
    "iconbitmap": "./Images/Icone.ico",
    "bg"        : "#202020",
    "info_bg"   : "#151515",
    "Tools_Bar_Btn_Color": "#FF6700",
    "Btn_Color": "purple"
}

# 3°) Caractéristiques des Boutons
#- Boutons de la Tools Bar
Tools_Bar_Btn_Size  = [200, 50]
Tools_Bar_Btn_Space = 5

#- Boutons représentatifs des données
Data_Ctn_Btn_Size   = [150, 50]
Data_Ctn_Btn_Space  = 5
Data_Ctn_Btn_Nb_Row = 4

# 4°) Caractéristiques du GUI
Tools_Bar_Size = [0, 0]
Data_Ctn_Size  = [0, 0]
GUI_Size       = [Tools_Bar_Size, Data_Ctn_Size]

DATA_DISPLAYED = "Aucune Data sélectionnée"
Entry_Data = dict()

# III) Fonctions
#- Fonctions de manipulation des données du .txt
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

def Find_Name(token):
    for k, val in Tk.items():
        if token == val:
            return k
    return "Token invalide"
# IV)  Class
#- Classe pour l'app GUI
class GUI(tkt.Tk):
    # I)   Fonctions propres au fonctionnement de l'app

    #- 1°) Changement des données affichées (passer des tokens aux Link)
    def Display_Data(self, Data_Type):
        # - Suppression des Widgets du Frame qu'on va utiliser
        global Data_Ctn
        for widget in Data_Ctn.winfo_children():
            widget.destroy()

        # - Récupération de la liste des données qu'on veut afficher
        Data = []
        global DATA_DISPLAYED
        if (Data_Type == "Token"): DATA_DISPLAYED = "Token"; Data = Tk
        if (Data_Type == "Link"):  DATA_DISPLAYED = "Link"; Data = DATA_LINK
        if (Data_Type == "Time"):  DATA_DISPLAYED = "Time"; Data = DATA_TIME

        # - Détermination du Nb de lignes
        try:
            Nb_Btn = len(Data)
        except:
            Nb_Btn = len(Data.keys())
        Nb_Rows = ceil(Nb_Btn / Data_Ctn_Btn_Nb_Row)  # Arrondi à l'unité sup

        # - Actualisation de la taille du GUI
        global Tools_Bar_Size, Data_Ctn_Size, GUI_Size
        Data_Ctn_Size = [
            (Data_Ctn_Btn_Size[0] * Data_Ctn_Btn_Nb_Row) + (Data_Ctn_Btn_Space * 2 * Data_Ctn_Btn_Nb_Row),
            (Data_Ctn_Btn_Size[1] * Nb_Rows) + (Data_Ctn_Btn_Space * 2 * Nb_Rows)
        ]
        GUI_Size = [Tools_Bar_Size, Data_Ctn_Size]

        # - Redimesionnement du GUI car nouveaux Btns
        self.geometry(f'{max(GUI_Size[0][0], GUI_Size[1][0])}x{GUI_Size[0][1] + GUI_Size[1][1]}')

        try:
            # - Affichage nouveaux Btns Link | Time
            for k, Btn in enumerate(Data):
                # - Détermination de la position du Btn dans la grid
                x = k % Data_Ctn_Btn_Nb_Row
                y = k // Data_Ctn_Btn_Nb_Row
                # - Création du Btn
                self.Make_Btn(Name=Btn["Name"],
                              Ctn=Data_Ctn,
                              x=x, y=y,
                              Font_Color="white",
                              Back_Color=GUI_Properties["Btn_Color"],
                              w=Data_Ctn_Btn_Size[0], h=Data_Ctn_Btn_Size[1],
                              Space=Data_Ctn_Btn_Space,
                              CallBack_Arg=("Details_Btn-" + Data_Type + ":" + Btn["Name"])
                              )
        except:
            # - Affichage nouveaux Btns Token
            for k, key in enumerate(Data.keys()):
                # - Détermination de la position du Btn dans la grid
                x = k % Data_Ctn_Btn_Nb_Row
                y = k // Data_Ctn_Btn_Nb_Row
                # - Création du Btn
                self.Make_Btn(Name=key,
                              Ctn=Data_Ctn,
                              x=x, y=y,
                              Font_Color="white",
                              Back_Color=GUI_Properties["Btn_Color"],
                              w=Data_Ctn_Btn_Size[0], h=Data_Ctn_Btn_Size[1],
                              Space=Data_Ctn_Btn_Space,
                              CallBack_Arg=("Details_Btn-" + "Token" + ":" + key))

    #- 2°) CallBack des boutons
    def Btn_CallBack(self, Btn_pressed):
        #- On récupère le type de boutons qui a été pressé
        Btn_Type, Btn_Name = Btn_pressed.split("-")[:]

        #- Distinction des fonctions appelées par rapport au Type des Btns (Change_to | Data | Add | Quit | Details_Btn | Add_Slave | Add_Link)
        #-- Tools_Bar
        if (Btn_Type == "Change_to"): self.Display_Data(Btn_Name)
        #-- Data
        #if (Btn_Type == "Data"): self.Display_Btn_Details(Btn_Name)
        #-- Add
        if (Btn_Type == "Add"): self.Add_Object()
        #-- Quit
        if (Btn_Type == "Quit"): self.Quit()
        #-- Details_Btn
        if (Btn_Type == "Details_Btn"): self.Display_Details_Btn(Btn_Name)
        #-- Add_Slave
        if (Btn_Type == "Add_Slave"): self.Add_Slave()
        #-- Add_Master
        if (Btn_Type == "Add_Master"): self.Add_Master()
        #-- Save_New_Link
        if (Btn_Type == "Save_New_Link"): self.Save_New_Link()
        #-- Save_New_Time
        if (Btn_Type == "Save_New_Time"): self.Save_New_Time()
        #-- Save_New_Token
        if (Btn_Type == "Save_New_Token"): self.Save_New_Token()
        #-- Supp_Btn
        if (Btn_Type == "Supp"): self.Supp_Btn(Btn_Name)

    #- 3°) Affichage du détails d'un bouton
    def Display_Details_Btn(self, Btn_pressed):
        # - On récupère le type de donnée du btn et son nom
        Btn_Data, Btn_Name = Btn_pressed.split(":")[:]

        # - Récupération de la liste qui contient les infos du Btn (Tk | Link | Time)
        Data_List = []
        if (Btn_Data == "Token"):
            self.Display_Details_Token({Btn_Data: Btn_Name})
            return
        if (Btn_Data == "Link"): Data_List = DATA_LINK
        if (Btn_Data == "Time"): Data_List = DATA_TIME

        # - Récupération du dict correspondant au Btn
        Btn_Dict = {}
        for btn in Data_List:
            if (btn["Name"] == Btn_Name):
                Btn_Dict = btn
                break

        # - Appel de la fonction spécialisée dans le type de btn à détailler
        if (Btn_Data == "Link"): self.Display_Details_Link_Btn(Btn_Dict)
        if (Btn_Data == "Time"): self.Display_Details_Time_Btn(Btn_Dict)

    #- 4°) Affichage détails Token Btn
    def Display_Details_Token(self, Data_Dict_Brut):
        Data_Dict = {}
        Data_Dict[Data_Dict_Brut['Token']] = Tk[(Data_Dict_Brut['Token'])]

        global Data_Ctn
        #- Suppression des Widgets du Frame qu'on va utiliser
        for widget in Data_Ctn.winfo_children():
            widget.destroy()

        #- Détermination des dimensions prises par l'affichage des données
        #-- Taille du nom du Btn
        Btn_Name_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            ((Data_Ctn_Btn_Size[1] * 1) + (Data_Ctn_Btn_Space * 2 * 2)) // 2 + 1 * Data_Ctn_Btn_Size[1]
            # Il faut penser au bonton de suppression
        ]
        #-- Taille de la partie Token
        Token_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 2) + (Data_Ctn_Btn_Space * 2 * 2),
            (Data_Ctn_Btn_Size[1] * 1) + Data_Ctn_Btn_Size[1] // 2 + (Data_Ctn_Btn_Space * 2 * 1)
            # ! Il faut penser au titre de la partie
        ]
        #-- Taille générale
        global Tools_Bar_Size, Data_Ctn_Size, GUI_Size
        Data_Ctn_Size = [
            max(Btn_Name_Size[0], Token_Part_Size[0]),
            Btn_Name_Size[1] + Token_Part_Size[1]
        ]

        #- Actualisation de la taille du GUI
        GUI_Size = [Tools_Bar_Size, Data_Ctn_Size]

        #- Redimesionnement du GUI
        self.geometry(f'{max(GUI_Size[0][0], GUI_Size[1][0])}x{GUI_Size[0][1] + GUI_Size[1][1]}')

        #- Création de la structure d'affichage
        #-- 3 parties: Nom Btn | Master part | Slave part
        #-- Disposition: Alignés sur une même la même colonne verticale
        #-- Contenant: Data_Ctn

        #--- Nom Btn, taille fixe, collé en haut
        Btn_Name = tkt.Frame(Data_Ctn, width=Btn_Name_Size[0], height=Btn_Name_Size[1])
        Btn_Name['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Btn_Name.configure(bg=GUI_Properties["bg"])
        Btn_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #--- Token part, taille variable, au milieu
        Token_Part = tkt.Frame(Data_Ctn, width=(Token_Part_Size[0]), height=Token_Part_Size[1])
        Token_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Token_Part.configure(bg=GUI_Properties["bg"])
        Token_Part.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #- Affichage des données dans la structure
        #-- Supprimer Btn
        self.Make_Btn(Name="Supprimer",
                      Ctn=Btn_Name,
                      x=0, y=0,
                      Font_Color="white",
                      Back_Color="red",
                      w=Data_Ctn_Btn_Size[0], h=Data_Ctn_Btn_Size[1],
                      Space=Data_Ctn_Btn_Space,
                      CallBack_Arg=("Supp-" + "Token:" + [X for X in Data_Dict.keys()][0])
                      )
        #-- Nom du Btn
        Label_Btn_Name = tkt.Label(Btn_Name,
                                   fg="white",
                                   bg=GUI_Properties["bg"],
                                   text=str([X for X in Data_Dict.keys()][0]))
        Label_Btn_Name.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #-- Partie Token
        Label_Master_Part_Name = tkt.Label(Token_Part,
                                           fg="white",
                                           bg=GUI_Properties["bg"],
                                           text=str([X for X in Data_Dict.values()][0]))
        Label_Master_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

    #- 5°) Affichage détails Link Btn
    def Display_Details_Link_Btn(self, Data_Dict):
        global Data_Ctn
        #- Suppression des Widgets du Frame qu'on va utiliser
        for widget in Data_Ctn.winfo_children():
            widget.destroy()

        #- Détermination des dimensions prises par l'affichage des données
        #-- Taille du nom du Btn
        Btn_Name_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            ((Data_Ctn_Btn_Size[1] * 1) + (Data_Ctn_Btn_Space * 2 * 2))//2 + 1*Data_Ctn_Btn_Size[1] # Il faut penser au bonton de suppression
        ]

        #-- Taille de la partie Maitre
        # --- Détermination du Nb d'esclaves
        Nb_Master = len(Data_Dict["Master_Token"])

        Master_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            int(((Data_Ctn_Btn_Size[1]//2) * Nb_Master) + Data_Ctn_Btn_Size[1] + (Data_Ctn_Btn_Space * 2 * Nb_Master))
        ]
        #-- Taille de la partie Esclave
        #--- Détermination du Nb d'esclaves
        Nb_Slave = len(Data_Dict["Slave_Token"])

        Slave_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            int(((Data_Ctn_Btn_Size[1]//2) * Nb_Slave) + Data_Ctn_Btn_Size[1] + (Data_Ctn_Btn_Space * 2 * Nb_Slave))
        ]
        #-- Taille générale
        global Tools_Bar_Size, Data_Ctn_Size, GUI_Size
        Data_Ctn_Size = [
            max(Btn_Name_Size[0], Master_Part_Size[0], Slave_Part_Size[0]),
            Btn_Name_Size[1] + Master_Part_Size[1] + Slave_Part_Size[1]
        ]

        #- Actualisation de la taille du GUI
        GUI_Size = [Tools_Bar_Size, Data_Ctn_Size]

        #- Redimesionnement du GUI
        self.geometry(f'{max(GUI_Size[0][0], GUI_Size[1][0])}x{GUI_Size[0][1] + GUI_Size[1][1]}')

        #- Création de la structure d'affichage
        #-- 3 parties: Nom Btn | Master part | Slave part
        #-- Disposition: Alignés sur une même la même colonne verticale
        #-- Contenant: Data_Ctn

        #--- Nom Btn, taille fixe, collé en haut
        Btn_Name = tkt.Frame(Data_Ctn, width=Btn_Name_Size[0], height=Btn_Name_Size[1])
        Btn_Name['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Btn_Name.configure(bg=GUI_Properties["bg"])
        Btn_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #--- Master part, taille variable, au milieu
        Master_Part = tkt.Frame(Data_Ctn, width=(Master_Part_Size[0]), height=Master_Part_Size[1])
        Master_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Master_Part.configure(bg=GUI_Properties["bg"])
        Master_Part.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #--- Slave part, taille variable, en bas
        Slave_Part = tkt.Frame(Data_Ctn, width=(Slave_Part_Size[0]), height=Slave_Part_Size[1])
        Slave_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Slave_Part.configure(bg=GUI_Properties["bg"])
        Slave_Part.grid(row=2, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #- Affichage des données dans la structure
        #-- Supprimer Btn
        self.Make_Btn(Name="Supprimer",
                      Ctn=Btn_Name,
                      x=0, y=0,
                      Font_Color="white",
                      Back_Color="red",
                      w=Data_Ctn_Btn_Size[0], h=Data_Ctn_Btn_Size[1],
                      Space=Data_Ctn_Btn_Space,
                      CallBack_Arg=("Supp-" + "Link:" + Data_Dict["Name"])
                      )
        #-- Nom du Btn
        Label_Btn_Name = tkt.Label(Btn_Name,
                                   fg="white",
                                   bg=GUI_Properties["bg"],
                                   text=Data_Dict["Name"])
        Label_Btn_Name.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #-- Partie Maitre
        #--- Nom de la partie
        Label_Master_Part_Name = tkt.Label(Master_Part,
                                           fg="white",
                                           bg=GUI_Properties["bg"],
                                           text="Master")
        Label_Master_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Master):
            self.Make_Label("Master_Token"+ ": " + Find_Name(str(Data_Dict["Master_Token"][k])), Master_Part, 0, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Master_Mode" + ": " + str(Data_Dict["Master_Mode"][k]),             Master_Part, 1, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Master_Vpin" + ": " + str(Data_Dict["Master_Vpin"][k]),             Master_Part, 2, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Master_State"+ ": " + str(Data_Dict["Master_State"][k]),            Master_Part, 3, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Partie Esclave
        #--- Nom de la partie
        Label_Slave_Part_Name = tkt.Label(Slave_Part,
                                          fg="white",
                                          bg=GUI_Properties["bg"],
                                          text="Slave")
        Label_Slave_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Slave):
            self.Make_Label("Slave_Token"+": "+ Find_Name(str(Data_Dict["Slave_Token"][k])), Slave_Part, 0, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Slave_Mode" +": "+ str(Data_Dict["Slave_Mode"][k])            , Slave_Part, 1, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Slave_Vpin" +": "+ str(Data_Dict["Slave_Vpin"][k])            , Slave_Part, 2, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Slave_State"+": "+ str(Data_Dict["Slave_State"][k])           , Slave_Part, 3, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

    #- 6°) Affichage détails Time Btn
    def Display_Details_Time_Btn(self, Data_Dict):
        global Data_Ctn
        #- Suppression des Widgets du Frame qu'on va utiliser
        for widget in Data_Ctn.winfo_children():
            widget.destroy()

        #- Détermination des dimensions prises par l'affichage des données
        #-- Taille du nom du Btn
        Btn_Name_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            ((Data_Ctn_Btn_Size[1] * 1) + (Data_Ctn_Btn_Space * 2 * 2)) // 2 + 1 * Data_Ctn_Btn_Size[1]
            # Il faut penser au bonton de suppression
        ]
        #-- Taille du nom du Hours
        Hours_Part_Size = [
            Data_Ctn_Btn_Size[0]+ (Data_Ctn_Btn_Space * 2),
            Data_Ctn_Btn_Size[1] + (Data_Ctn_Btn_Space * 2)
            # Il faut penser au bonton de suppression
        ]
        #-- Taille de la partie Maitre
        #--- Détermination du Nb d'esclaves
        Nb_Master = len(Data_Dict["Master_Token"])

        Master_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            (Data_Ctn_Btn_Size[1] * Nb_Master) + Data_Ctn_Btn_Size[1] // 2 + (Data_Ctn_Btn_Space * 2 * Nb_Master)
            # ! Il faut penser au titre de la partie
        ]
        #-- Taille de la partie Esclave
        #--- Détermination du Nb d'esclaves
        Nb_Slave = len(Data_Dict["Slave_Token"])

        Slave_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            (Data_Ctn_Btn_Size[1] * Nb_Slave) + Data_Ctn_Btn_Size[1] // 2 + (Data_Ctn_Btn_Space * 2 * Nb_Slave)
            # ! Il faut penser au titre de la partie
        ]
        #-- Taille générale
        global Tools_Bar_Size, Data_Ctn_Size, GUI_Size
        Data_Ctn_Size = [
            max(Btn_Name_Size[0], Master_Part_Size[0], Slave_Part_Size[0], Hours_Part_Size[0]),
            Btn_Name_Size[1] + Master_Part_Size[1] + Slave_Part_Size[1] + Hours_Part_Size[1]
        ]

        #- Actualisation de la taille du GUI
        GUI_Size = [Tools_Bar_Size, Data_Ctn_Size]

        #- Redimesionnement du GUI
        self.geometry(f'{max(GUI_Size[0][0], GUI_Size[1][0])}x{GUI_Size[0][1] + GUI_Size[1][1]}')

        #- Création de la structure d'affichage
        #-- 5 parties: Hours_Part_Size | Nom Btn | Hours part | Master part | Slave part
        #-- Disposition: Alignés sur une même la même colonne verticale
        #-- Contenant: Data_Ctn

        #--- Nom Btn, taille fixe, collé en haut
        Btn_Name = tkt.Frame(Data_Ctn, width=Btn_Name_Size[0], height=Btn_Name_Size[1])
        Btn_Name['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Btn_Name.configure(bg=GUI_Properties["bg"])
        Btn_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #--- Hours part
        Hours_Part = tkt.Frame(Data_Ctn, width=Hours_Part_Size[0], height=Hours_Part_Size[1])
        Hours_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Hours_Part.configure(bg=GUI_Properties["bg"])
        Hours_Part.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #--- Master part, taille variable, au milieu
        Master_Part = tkt.Frame(Data_Ctn, width=(Master_Part_Size[0]), height=Master_Part_Size[1])
        Master_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Master_Part.configure(bg=GUI_Properties["bg"])
        Master_Part.grid(row=2, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #--- Slave part, taille variable, en bas
        Slave_Part = tkt.Frame(Data_Ctn, width=(Slave_Part_Size[0]), height=Slave_Part_Size[1])
        Slave_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Slave_Part.configure(bg=GUI_Properties["bg"])
        Slave_Part.grid(row=3, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #- Affichage des données dans la structure
        #-- Supprimer Btn
        self.Make_Btn(Name="Supprimer",
                      Ctn=Btn_Name,
                      x=0, y=0,
                      Font_Color="white",
                      Back_Color="red",
                      w=Data_Ctn_Btn_Size[0], h=Data_Ctn_Btn_Size[1],
                      Space=Data_Ctn_Btn_Space,
                      CallBack_Arg=("Supp-" + "Time:" + Data_Dict["Name"])
                      )
        #-- Nom du Btn
        Label_Btn_Name = tkt.Label(Btn_Name,
                                   fg="white",
                                   bg=GUI_Properties["bg"],
                                   text=Data_Dict["Name"])
        Label_Btn_Name.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #-- Partie Hours
        #--- Nom de la partie
        Label_Master_Part_Name = tkt.Label(Hours_Part,
                                           fg="white",
                                           bg=GUI_Properties["bg"],
                                           text="Hours")
        Label_Master_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #-- Info de la partie
        self.Make_Label("Start_Time" + ": " + str(Data_Dict["Start_Time"]), Hours_Part, 0, 1, "white",
                        GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Partie Maitre
        #--- Nom de la partie
        Label_Master_Part_Name = tkt.Label(Master_Part,
                                           fg="white",
                                           bg=GUI_Properties["bg"],
                                           text="Master")
        Label_Master_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Master):
            self.Make_Label("Master_Token"+ ": " + Find_Name(str(Data_Dict["Master_Token"][k])), Master_Part, 0, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Master_Vpin" + ": " + str(Data_Dict["Master_Vpin"][k]),             Master_Part, 2, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Master_State"+ ": " + str(Data_Dict["Master_State"][k]),            Master_Part, 3, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Partie Esclave
        #--- Nom de la partie
        Label_Slave_Part_Name = tkt.Label(Slave_Part,
                                          fg="white",
                                          bg=GUI_Properties["bg"],
                                          text="Slave")
        Label_Slave_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Slave):
            self.Make_Label("Slave_Token"+": "+ Find_Name(str(Data_Dict["Slave_Token"][k])), Slave_Part, 0, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Slave_Vpin" +": "+ str(Data_Dict["Slave_Vpin"][k])            , Slave_Part, 2, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Label("Slave_State"+": "+ str(Data_Dict["Slave_State"][k])           , Slave_Part, 3, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

    #- 7°) Supprimer un Btn
    def Supp_Btn(self, Btn_pressed):
        #- On récupère le type de donnée du btn et son nom
        Btn_Data, Btn_Name = Btn_pressed.split(":")[:]

        #- Récupération de la liste qui contient les infos du Btn (Tk | Link | Time)
        Data_List = []
        if (Btn_Data == "Token"):
            del Tk[Btn_Name]; R_fichier("w", chemin_token, str(Tk)); self.Display_Data(DATA_DISPLAYED); return
        if (Btn_Data == "Link"): Data_List = DATA_LINK
        if (Btn_Data == "Time"): Data_List = DATA_TIME

        #- Récupération du numéro dans la liste du Btn
        for k, btn in enumerate(Data_List):
            if (btn["Name"] == Btn_Name):
                del Data_List[k]
                R_fichier("w", chemin_link, str(DATA_LINK))
                R_fichier("w", chemin_time, str(DATA_TIME))
                break

        self.Display_Data(DATA_DISPLAYED)

    #- 8°) Redimensionner le GUI
    def ReSize_Gui(self):
        global Btn_Name_Size, Hours_Part_Size, Master_Part_Size, Slave_Part_Size, Options_Part_Size, Nb_Slave, Nb_Master

        # - Détermination des dimensions prises par l'affichage des données
        # -- Taille du nom du Btn
        Btn_Name_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            ((Data_Ctn_Btn_Size[1] * 1) + (Data_Ctn_Btn_Space * 2 * 2)) // 2
        ]
        # -- Taille du nom du Hours
        if DATA_DISPLAYED == "Time":
            Hours_Part_Size = [
                Data_Ctn_Btn_Size[0] + (Data_Ctn_Btn_Space * 2),
                Data_Ctn_Btn_Size[1] + (Data_Ctn_Btn_Space * 2)
                # Il faut penser au bonton de suppression
            ]
        else:
            Hours_Part_Size = [0, 0]

        # -- Taille de la partie Maitre
        Master_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            ((Data_Ctn_Btn_Size[1] // 2) * Nb_Master) + Data_Ctn_Btn_Size[1] + (Data_Ctn_Btn_Space * 2 * Nb_Master)
        ]
        # -- Taille de la partie Esclave
        Slave_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            ((Data_Ctn_Btn_Size[1] // 2) * Nb_Slave) + Data_Ctn_Btn_Size[1] + (Data_Ctn_Btn_Space * 2 * Nb_Slave)
        ]
        # -- Taille de la partie Options
        # --- 2 options => Créer | Validé
        Options_Part_Size = [
            Slave_Part_Size[0],
            Data_Ctn_Btn_Size[1] // 2
        ]

        # -- Taille générale
        global Tools_Bar_Size, Data_Ctn_Size, GUI_Size
        Data_Ctn_Size = [
            max(Btn_Name_Size[0], Master_Part_Size[0], Slave_Part_Size[0], Options_Part_Size[0], Hours_Part_Size[0]),
            Btn_Name_Size[1] + Master_Part_Size[1] + Slave_Part_Size[1] + Options_Part_Size[1] + Hours_Part_Size[1]
        ]

        # - Actualisation de la taille du GUI
        GUI_Size = [Tools_Bar_Size, Data_Ctn_Size]

        # - Redimesionnement du GUI
        self.geometry(f'{max(GUI_Size[0][0], GUI_Size[1][0])}x{GUI_Size[0][1] + GUI_Size[1][1]}')

    #- 9°) Ajouter un Token
    def Add_Token(self):
        # - Suppression des Widgets du Frame qu'on va utiliser
        global Data_Ctn
        for widget in Data_Ctn.winfo_children():
            widget.destroy()

        # Dimmension GUI
        Nom_Token_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            ((Data_Ctn_Btn_Size[1] * 1) + (Data_Ctn_Btn_Space * 2 * 2)) // 2
        ]
        Token_Part_Size = [
            (Data_Ctn_Btn_Size[0] * 4) + (Data_Ctn_Btn_Space * 2 * 4),
            (Data_Ctn_Btn_Size[1] // 2) + Data_Ctn_Btn_Size[1] + (Data_Ctn_Btn_Space * 2)
        ]
        Options_Part_Size = [
            Token_Part_Size[0],
            Data_Ctn_Btn_Size[1] // 2
        ]

        # -- Taille générale
        global Tools_Bar_Size, GUI_Size
        Data_Ctn_Size = [
            max(Nom_Token_Size[0], Token_Part_Size[0], Options_Part_Size[0]),
            Nom_Token_Size[1] + Token_Part_Size[1] + Options_Part_Size[1]
        ]

        # - Actualisation de la taille du GUI
        GUI_Size = [Tools_Bar_Size, Data_Ctn_Size]

        # - Redimesionnement du GUI
        self.geometry(f'{max(GUI_Size[0][0], GUI_Size[1][0])}x{GUI_Size[0][1] + GUI_Size[1][1]}')

        # - Création de la structure d'affichage
        # -- 3 parties: Nom Token | Token part | Option part
        # -- Disposition: Alignés sur une même la même colonne verticale
        # -- Contenant: Data_Ctn
        # --- Nom Token, taille fixe, collé en haut
        Nom_Token = tkt.Frame(Data_Ctn, width=Nom_Token_Size[0], height=Nom_Token_Size[1])
        Nom_Token['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Nom_Token.configure(bg=GUI_Properties["bg"])
        Nom_Token.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        # --- Token part, taille fixe, au milieu
        Token_Part = tkt.Frame(Data_Ctn, width=(Token_Part_Size[0]), height=Token_Part_Size[1])
        Token_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Token_Part.configure(bg=GUI_Properties["bg"])
        Token_Part.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        # --- Options part, taille fixe, en bas
        Options_Part = tkt.Frame(Data_Ctn, width=(Options_Part_Size[0]), height=Options_Part_Size[1])
        Options_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Options_Part.configure(bg=GUI_Properties["bg"])
        Options_Part.grid(row=2, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        # - Affichage des clés à compléter
        # -- Nom du Btn
        self.Make_Entry("Device Name: ", Nom_Token, 0, 0, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        # -- Token part
        self.Make_Entry("Token key: ", Token_Part, 0, 1, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        # - Affichage des options
        # -- Btn Validée, pour enregistrer les données
        self.Make_Btn("Validé", Options_Part, 2, 0, "black", "white", Data_Ctn_Btn_Size[0] // 2,Data_Ctn_Btn_Size[1] // 2, Data_Ctn_Btn_Space, ("Save_New_Token-" + "Token"))

    #- 10°) Ajouter un Link
    def Add_Link(self):

        #- Suppression des Widgets du Frame qu'on va utiliser
        global Data_Ctn
        for widget in Data_Ctn.winfo_children():
            widget.destroy()

        #Dimmension GUI
        global Nb_Slave
        try: Nb_Slave = Nb_Slave
        except: Nb_Slave = 1 # Par défaut

        global Nb_Master
        try: Nb_Master = Nb_Master
        except: Nb_Master = 1 # Par défaut
        self.ReSize_Gui()

        #- Création de la structure d'affichage
        #-- 4 parties: Nom Btn | Master part | Slave part | Options Part
        #-- Disposition: Alignés sur une même la même colonne verticale
        #-- Contenant: Data_Ctn
        #--- Nom Btn, taille fixe, collé en haut
        global Btn_Name_Size
        Btn_Name = tkt.Frame(Data_Ctn, width=Btn_Name_Size[0], height=Btn_Name_Size[1])
        Btn_Name['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Btn_Name.configure(bg=GUI_Properties["bg"])
        Btn_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #--- Master part, taille variable, au milieu
        global Master_Part_Size
        Master_Part = tkt.Frame(Data_Ctn, width=(Master_Part_Size[0]), height=Master_Part_Size[1])
        Master_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Master_Part.configure(bg=GUI_Properties["bg"])
        Master_Part.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #--- Slave part, taille variable, au milieu
        global Slave_Part_Size
        Slave_Part = tkt.Frame(Data_Ctn, width=(Slave_Part_Size[0]), height=Slave_Part_Size[1])
        Slave_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Slave_Part.configure(bg=GUI_Properties["bg"])
        Slave_Part.grid(row=2, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #--- Options part, taille variable, en bas
        global Options_Part
        Options_Part = tkt.Frame(Data_Ctn, width=(Options_Part_Size[0]), height=Options_Part_Size[1])
        Options_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Options_Part.configure(bg=GUI_Properties["bg"])
        Options_Part.grid(row=3, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #- Affichage des clés à compléter
        #-- Nom du Btn
        self.Make_Entry("Name: ", Btn_Name, 0, 0, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Partie Maitre
        #--- Nom de la partie
        Label_Master_Part_Name = tkt.Label(Master_Part,
                                               fg="white",
                                               bg=GUI_Properties["bg"],
                                               text="Master")
        Label_Master_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Master):
            self.Make_Entry(str(k) + ".Master_Token: ", Master_Part, 0, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Master_Mode: " , Master_Part, 1, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Master_Vpin: " , Master_Part, 2, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Master_State: ", Master_Part, 3, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Partie Esclave
        #--- Nom de la partie
        Label_Slave_Part_Name = tkt.Label(Slave_Part,
                                          fg="white",
                                          bg=GUI_Properties["bg"],
                                          text="Slave")
        Label_Slave_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Slave):
            self.Make_Entry(str(k) + ".Slave_Token: ", Slave_Part, 0, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Slave_Mode: " , Slave_Part, 1, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Slave_Vpin: " , Slave_Part, 2, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Slave_State: ", Slave_Part, 3, 1+k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #- Affichage des options
        #-- Btn + Master, pour ajouter un esclave
        self.Make_Btn("+ Master", Options_Part, 0, 0, "white", "green", Data_Ctn_Btn_Size[0] // 2, Data_Ctn_Btn_Size[1] // 2, Data_Ctn_Btn_Space, ("Add_Master-" + "Link"))
        #-- Btn + Slave, pour ajouter un esclave
        self.Make_Btn("+ Slave ", Options_Part, 1, 0, "white", "green", Data_Ctn_Btn_Size[0] // 2, Data_Ctn_Btn_Size[1] // 2, Data_Ctn_Btn_Space, ("Add_Slave-" + "Link"))
        #-- Btn Validée, pour enregistrer les données
        self.Make_Btn("Validé",   Options_Part, 2, 0, "black", "white", Data_Ctn_Btn_Size[0] // 2, Data_Ctn_Btn_Size[1] // 2, Data_Ctn_Btn_Space, ("Save_New_Link-" + "Link"))

    #- 11°) Ajouter un Time
    def Add_Time(self):

        #- Suppression des Widgets du Frame qu'on va utiliser
        global Data_Ctn
        for widget in Data_Ctn.winfo_children():
            widget.destroy()

        #Dimmension GUI
        global Nb_Slave
        try: Nb_Slave = Nb_Slave
        except: Nb_Slave = 1 # Par défaut

        global Nb_Master
        try: Nb_Master = Nb_Master
        except: Nb_Master = 1 # Par défaut
        self.ReSize_Gui()

        #- Création de la structure d'affichage
        #-- 5 parties: Nom Btn | Hours part | Master part | Slave part | Options Part
        #-- Disposition: Alignés sur une même la même colonne verticale
        #-- Contenant: Data_Ctn
        #--- Nom Btn, taille fixe, collé en haut
        global Btn_Name_Size
        Btn_Name = tkt.Frame(Data_Ctn, width=Btn_Name_Size[0], height=Btn_Name_Size[1])
        Btn_Name['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Btn_Name.configure(bg=GUI_Properties["bg"])
        Btn_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #--- Hours part
        global Hours_Part_Size
        Hours_Part = tkt.Frame(Data_Ctn, width=Hours_Part_Size[0], height=Hours_Part_Size[1])
        Hours_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Hours_Part.configure(bg=GUI_Properties["bg"])
        Hours_Part.grid(row=1, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space, sticky="n")

        #--- Master part, taille variable, au milieu
        global Master_Part_Size
        Master_Part = tkt.Frame(Data_Ctn, width=(Master_Part_Size[0]), height=Master_Part_Size[1])
        Master_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Master_Part.configure(bg=GUI_Properties["bg"])
        Master_Part.grid(row=2, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #--- Slave part, taille variable, au milieu
        global Slave_Part_Size
        Slave_Part = tkt.Frame(Data_Ctn, width=(Slave_Part_Size[0]), height=Slave_Part_Size[1])
        Slave_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Slave_Part.configure(bg=GUI_Properties["bg"])
        Slave_Part.grid(row=3, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #--- Options part, taille variable, en bas
        global Options_Part
        Options_Part = tkt.Frame(Data_Ctn, width=(Options_Part_Size[0]), height=Options_Part_Size[1])
        Options_Part['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Options_Part.configure(bg=GUI_Properties["bg"])
        Options_Part.grid(row=4, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)

        #- Affichage des clés à compléter
        #-- Nom du Btn
        self.Make_Entry("Name: ", Btn_Name, 0, 0, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Start Hours
        self.Make_Entry("Start_Time: ", Hours_Part, 0, 0, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Partie Maitre
        #--- Nom de la partie
        Label_Master_Part_Name = tkt.Label(Master_Part,
                                           fg="white",
                                           bg=GUI_Properties["bg"],
                                           text="Master")
        Label_Master_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Master):
            self.Make_Entry(str(k) + ".Master_Token: ", Master_Part, 0, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Master_Vpin: " , Master_Part, 1, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Master_State: ", Master_Part, 2, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #-- Partie Esclave
        #--- Nom de la partie
        Label_Slave_Part_Name = tkt.Label(Slave_Part,
                                          fg="white",
                                          bg=GUI_Properties["bg"],
                                          text="Slave")
        Label_Slave_Part_Name.grid(row=0, column=0, padx=Data_Ctn_Btn_Space, pady=Data_Ctn_Btn_Space)
        #--- Infos de la partie
        for k in range(Nb_Slave):
            self.Make_Entry(str(k) + ".Slave_Token: ", Slave_Part, 0, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Slave_Vpin: " , Slave_Part, 1, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)
            self.Make_Entry(str(k) + ".Slave_State: ", Slave_Part, 2, 1 + k, "white", GUI_Properties["info_bg"], Data_Ctn_Btn_Space)

        #- Affichage des options
        #-- Btn + Master, pour ajouter un esclave
        self.Make_Btn("+ Master", Options_Part, 0, 0, "white", "green", Data_Ctn_Btn_Size[0] // 2, Data_Ctn_Btn_Size[1] // 2, Data_Ctn_Btn_Space, ("Add_Master-" + "Time"))
        #-- Btn + Slave, pour ajouter un esclave
        self.Make_Btn("+ Slave ", Options_Part, 1, 0, "white", "green", Data_Ctn_Btn_Size[0] // 2, Data_Ctn_Btn_Size[1] // 2, Data_Ctn_Btn_Space, ("Add_Slave-" + "Time"))
        #-- Btn Validée, pour enregistrer les données
        self.Make_Btn("Validé", Options_Part, 2, 0, "black", "white", Data_Ctn_Btn_Size[0] // 2, Data_Ctn_Btn_Size[1] // 2, Data_Ctn_Btn_Space, ("Save_New_Time-" + "Time"))

    #- 12°) Ajouter un esclave lors de la création d'un lien
    def Add_Slave(self):
        global Nb_Slave
        Nb_Slave += 1
        self.ReSize_Gui()
        if DATA_DISPLAYED == "Link": self.Add_Link()
        if DATA_DISPLAYED == "Time": self.Add_Time()

    #- 13°) Ajouter un Maitre lors de la création d'un lien
    def Add_Master(self):
        global Nb_Master
        Nb_Master += 1
        self.ReSize_Gui()
        if DATA_DISPLAYED == "Link": self.Add_Link()
        if DATA_DISPLAYED == "Time": self.Add_Time()

    #- 14°) Ajouter un Token au fichier texte
    def Save_New_Token(self):
        global Entry_Data

        Tk[str(Entry_Data["Device Name: "].get())] = str(Entry_Data["Token key: "].get())
        self.Btn_CallBack("Change_to-" + DATA_DISPLAYED)

    #- 15°) Ajouter un Lien au fichier texte
    def Save_New_Link(self):
        global Entry_Data
        New_Link = {
            "Name"        : str(Entry_Data["Name: "].get()),
            "Master_Token": list(),
            "Master_Mode" : list(),
            "Master_Vpin" : list(),
            "Master_State": list(),

            'Slave_Token': list(),
            'Slave_Mode' : list(),
            'Slave_Vpin' : list(),
            'Slave_State': list(),

            'LastState': list()
        }
        # Master data
        k = 0
        while True:
            try:
                New_Link["Master_Token"].append( Tk[str(Entry_Data[str(k) + ".Master_Token: "].get())])
                New_Link["Master_Mode"].append(  str(Entry_Data[str(k)    + ".Master_Mode: "].get()))
                New_Link["Master_Vpin"].append(  str("V" + Entry_Data[str(k)    + ".Master_Vpin: "].get()))
                # Si c'est pas un dict on fait pas le eval
                if( eval(Entry_Data[str(k) + ".Master_State: "].get()) == ""):
                    New_Link["Master_State"].append( Entry_Data[str(k)    + ".Master_State: "].get())
                else:
                    New_Link["Master_State"].append(eval(Entry_Data[str(k) + ".Master_State: "].get()))
                k += 1
            except: break
        # Slave data
        k = 0
        while True:
            try:
                New_Link["Slave_Token"].append(Tk[str(Entry_Data[str(k) + ".Slave_Token: "].get())])
                New_Link["Slave_Mode"].append(str(Entry_Data[str(k) + ".Slave_Mode: "].get()))
                New_Link["Slave_Vpin"].append(str("V" + Entry_Data[str(k) + ".Slave_Vpin: "].get()))
                # Si c'est pas un dict on fait pas le eval
                if( eval(Entry_Data[str(k)    + ".Master_State: "].get()) == ""):
                    New_Link["Slave_State"].append( Entry_Data[str(k)    + ".Slave_State: "].get())
                else:
                    New_Link["Slave_State"].append(eval(Entry_Data[str(k) + ".Slave_State: "].get()))
                k += 1
            except:
                break

        New_Link['LastState'] = []

        DATA_LINK.append(New_Link)
        self.Btn_CallBack("Change_to-"+ DATA_DISPLAYED )

    #- 16°) Ajouter un Time au fichier texte
    def Save_New_Time(self):
        global Entry_Data
        New_Time = {
            "Name": str(Entry_Data["Name: "].get()),
            "Start_Time": str(Entry_Data["Start_Time: "].get()),
            "Master_Token": list(),
            "Master_Vpin": list(),
            "Master_State": list(),

            'Slave_Token': list(),
            'Slave_Vpin': list(),
            'Slave_State': list(),

            'Anti_Repeat': 1
        }
        # Master data
        k = 0
        while True:
            try:
                New_Time["Master_Token"].append(Tk[str(Entry_Data[str(k) + ".Master_Token: "].get())])
                New_Time["Master_Vpin"].append(str("V" + Entry_Data[str(k) + ".Master_Vpin: "].get()))
                New_Time["Master_State"].append(str(Entry_Data[str(k) + ".Master_State: "].get()))
                k += 1
            except:
                break
        # Slave data
        k = 0
        while True:
            try:
                New_Time["Slave_Token"].append(Tk[str(Entry_Data[str(k) + ".Slave_Token: "].get())])
                New_Time["Slave_Vpin"].append(str("V" + Entry_Data[str(k) + ".Slave_Vpin: "].get()))
                New_Time["Slave_State"].append( str(Entry_Data[str(k) + ".Slave_State: "].get()))

                k += 1
            except:
                break

        DATA_TIME.append(New_Time)
        self.Btn_CallBack("Change_to-" + DATA_DISPLAYED)

    #- 17°) Quitter et enregistrer les changements
    def Quit(self):
        R_fichier("w", chemin_link, str(DATA_LINK))
        R_fichier("w", chemin_time, str(DATA_TIME))
        R_fichier("w", chemin_token, str(Tk))
        self.destroy()

    #- 18°) Création d'un nouvel objet dans le dict
    def Add_Object(self):
        if(DATA_DISPLAYED == "Token"): self.Add_Token()
        if(DATA_DISPLAYED == "Link"):  self.Add_Link()
        if(DATA_DISPLAYED == "Time"):  self.Add_Time()


    # II)  Fonctions propres à l'esthétique
    #- 1°) Création de boutons
    def Make_Btn(self, Name, Ctn, x, y, Font_Color, Back_Color, w, h, Space, CallBack_Arg):
        #- Création du Ctn du bouton aux bonnes dimensions
        Btn_Ctn = tkt.Frame(Ctn, width=w, height=h)
        Btn_Ctn['highlightthickness'] = 0 # Suppression de la bordure du Frame
        Btn_Ctn.configure(bg=GUI_Properties["bg"])
        Btn_Ctn.grid(row=y, column=x, padx=Space, pady=Space)

        #- Création du Btn
        Btn = tkt.Button(Btn_Ctn,
                         fg=Font_Color,
                         bg=Back_Color,
                         activebackground="yellow",
                         relief="flat",
                         borderwidth=10,
                         text=Name,
                         command=lambda: self.Btn_CallBack(CallBack_Arg))
        #-- Placement du Bouton dans son container (1 = 100% de la largeur du parent)
        Btn.place(relwidth=1, relheight=1)

    #- 2°) Création des labels
    def Make_Label(self, Name, Ctn, x, y, Font_Color, Back_Color, Space):
        label = tkt.Label(Ctn,
                          fg=Font_Color,
                          bg=Back_Color,
                          text=Name)
        label.grid(row=y, column=x, padx=Space, pady=Space)

    #- 3°) Création des entrées de texte
    def Make_Entry(self, Name, Ctn, x, y, Font_Color, Back_Color, Space):
        #- Création du Ctn du Label et de l'entrée de Text
        Sous_Ctn = tkt.Frame(Ctn)
        Sous_Ctn['highlightthickness'] = 0  # Suppression de la bordure du Frame
        Sous_Ctn.configure(bg=GUI_Properties["bg"])
        Sous_Ctn.grid(row=y, column=x, padx=Space, pady=Space)

        self.Make_Label(Name, Sous_Ctn, 0, 0, Font_Color, Back_Color, 0)


        global Entry_Data
        Entry = tkt.Entry(Sous_Ctn,
                          fg=Font_Color,
                          bg=Back_Color,
                          width= 15
                          )
        Entry_Data[Name] = Entry
        Entry.grid(row=0, column=1)


    # III) Fonctions générales
    #- 1°) Création du GUI
    def Make_GUI(self):
        # Création GUI:
        #- 1°) Déterminer les dimensions Width x Height en fonction du contenu
        #-- Il y a 5 Boutons: Btn_Token | Btn_Link | Btn_Time | Btn_Créer | Btn_Quitter
        #-- Disposition: Alignés sur une même ligne horizontale
        #-- Contenant: Tools_Bar
        global Tools_Bar_Size
        Tools_Bar_Size = [
            (Tools_Bar_Btn_Size[0] * 5) + (Tools_Bar_Btn_Space * 2 * 5),
            (Tools_Bar_Btn_Size[1] * 1) + (Tools_Bar_Btn_Space * 2 * 1)
        ]
        #-- On actualise la taille du GUI
        GUI_Size[0][:] = Tools_Bar_Size[:]

        #- 2°) Création de la fenêtre
        #-- Paramètres propres à la taille
        self.geometry(f'{max(GUI_Size[0][0], GUI_Size[1][0])}x{GUI_Size[0][1] + GUI_Size[1][1]}')
        self.resizable(True, True)
        #-- Paramètres de l'esthtiques statiques: Titre, Icone, Couleur bg, ...
        self.title(       GUI_Properties["title"]     )
        #self.iconbitmap(  GUI_Properties["iconbitmap"])
        self.configure(bg=GUI_Properties["bg"]        )

        #- 3°) Création de la structure du GUI
        #-- 2 parties: Tools Bar | Data Container
        #-- Disposition: Alignés sur une même la même colonne verticale
        #-- Contenant: Fenêtre de l'app (le GUI lui même)
        #--- Tools Bar, taille fixe, collé en haut
        global Tools_Bar
        Tools_Bar = tkt.Frame(self, width=Tools_Bar_Size[0], height=Tools_Bar_Size[1])
        Tools_Bar['highlightthickness'] = 0 # Suppression de la bordure du Frame
        Tools_Bar.configure(bg=GUI_Properties["bg"])
        Tools_Bar.grid(row=0, column=0, sticky="n")
        #--- Data Container, taille variable, collé en bas
        global Data_Ctn
        Data_Ctn = tkt.Frame(self, width=Tools_Bar_Size[0], height=Tools_Bar_Size[1])
        Data_Ctn['highlightthickness'] = 0 # Suppression de la bordure du Frame
        Data_Ctn.configure(bg=GUI_Properties["bg"])
        Data_Ctn.grid(row=1, column=0, sticky="s")

        #- 4°) Création des boutons de la ToolS Bar
        #-- Il y a 5 Boutons: Btn_Token | Btn_Link | Btn_Time | Btn_Créer | Quitter
        #--- Btn_Token
        self.Make_Btn(Name="Token",
                      Ctn=Tools_Bar,
                      x=0, y=0,
                      Font_Color="white",
                      Back_Color=GUI_Properties["Tools_Bar_Btn_Color"],
                      w=Tools_Bar_Btn_Size[0], h=Tools_Bar_Btn_Size[1],
                      Space= Tools_Bar_Btn_Space,
                      CallBack_Arg= "Change_to-Token"
                      )
        #--- Btn_Link
        self.Make_Btn(Name="Link",
                      Ctn=Tools_Bar,
                      x=1, y=0,
                      Font_Color="white",
                      Back_Color=GUI_Properties["Tools_Bar_Btn_Color"],
                      w=Tools_Bar_Btn_Size[0], h=Tools_Bar_Btn_Size[1],
                      Space= Tools_Bar_Btn_Space,
                      CallBack_Arg="Change_to-Link"
                      )
        #--- Btn_Time
        self.Make_Btn(Name="Time",
                      Ctn=Tools_Bar,
                      x=2, y=0,
                      Font_Color="white",
                      Back_Color=GUI_Properties["Tools_Bar_Btn_Color"],
                      w=Tools_Bar_Btn_Size[0], h=Tools_Bar_Btn_Size[1],
                      Space= Tools_Bar_Btn_Space,
                      CallBack_Arg="Change_to-Time"
                      )
        #--- Btn_Créer
        self.Make_Btn(Name="Créer",
                      Ctn=Tools_Bar,
                      x=3, y=0,
                      Font_Color="white",
                      Back_Color=GUI_Properties["Tools_Bar_Btn_Color"],
                      w=Tools_Bar_Btn_Size[0], h=Tools_Bar_Btn_Size[1],
                      Space= Tools_Bar_Btn_Space,
                      CallBack_Arg="Add-Créer"
                      )
        #--- Btn_Quitter
        self.Make_Btn(Name="Quitter",
                      Ctn=Tools_Bar,
                      x=4, y=0,
                      Font_Color="white",
                      Back_Color=GUI_Properties["Tools_Bar_Btn_Color"],
                      w=Tools_Bar_Btn_Size[0], h=Tools_Bar_Btn_Size[1],
                      Space= Tools_Bar_Btn_Space,
                      CallBack_Arg="Quit-Save"
                      )

# V)   Main
# Récupération de toutes les infos sur: les tokens | les ponts | les animations de temps
# Infos sur les Tokens
Tk = Get_Data_File(chemin_token)

# Infos Ponts
DATA_LINK = Get_Data_File(chemin_link)

# Infos Automatisation de temps
DATA_TIME = Get_Data_File(chemin_time)

app = GUI()
app.Make_GUI()

app.mainloop()

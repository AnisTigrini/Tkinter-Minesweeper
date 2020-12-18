"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
import os
import simpleaudio as sa
from tkinter import messagebox, Tk, Frame, Button, PhotoImage, Label, Message, StringVar, Entry, filedialog
from tableau import Tableau
from bouton_case import BoutonCase
from case import Case as la_case_de_jeu


class InterfacePartie(Tk):
    def __init__(self):
        """ Initialisation d'un object d'InterfacePartie. 
        
        Attributes:
        

            resizable (tuple): Garde la fenêtre d'une grandeur fixe.
            compteur_de_tour (int): Compte le nomrbe de tour jouer.
            dictionnaireBoutons (dict): Dictionnaire possédant comme clé un tuple contenant les coordonnées d'une case et comme valeur un instanciation de la calsse case.
            liste_case_devoilee (liste): Liste possédant les case ayant été dévoilées.
            nombre_case_devoile (liste): Liste possédant le nombre actif de case dévoilées.
            dansPartie (bool): Détermine si un utilisateur est dans une partie.
            statut_partie (str): Détermine si la partie est gagné ou perdu.(Trois valeurs possibles : 'gagné', 'perdu' ou None)
            fenetre_jeu (bool): Détermine si l'utilisateur est dans une fenêtre de jeu.
        """ 

        super().__init__()

        # 1) Nom de la fenêtre et faire en sorte qu'on ne peux pas changer la grandeur et le compteur de tour.
        self.title("Démineur")
        self.resizable(0,0)
        self.compteur_de_tour = 0
        self.dictionnaireBoutons = dict()
        self.liste_case_devoilee = []
        self.nombre_case_devoile = []
        self.dansPartie = False
        self.statut_partie = None
        self.fenetre_jeu = False
        
        # 2) Charger l'image de la mine et la placer dans self.imageBombe pour 
        # l'utiliser quand on en a besoin.
        self.base_folder = os.path.dirname(__file__)
        image_path = os.path.join(self.base_folder, "bombe.gif")
        self.imageBombe = PhotoImage(file = image_path)
        self.wave_obj_one = sa.WaveObject.from_wave_file(os.path.join(self.base_folder, 'song.wav'))
        self.wave_obj_two = sa.WaveObject.from_wave_file(os.path.join(self.base_folder, 'surprise.wav'))

        # 3) Initialiser un paramètre qui va contenir un instance de l'objet "Tableau".
        self.tableau_mines = None

        # 4) Établir un "Frame" de bouton sur l'objet InterfacePartie pour placer les boutons importants dessus.
        bouton_frame = Frame(self)
        bouton_frame.grid()

        # 4.1) Boutton nouvelle partie.
        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        # 4.2) Boutton quitter.
        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitterPartie)
        bouton_quitter.grid(row=0, column=1)

        # 4.3) Boutton des règles du jeu
        bouton_regles = Button(bouton_frame, text="?", command=self.reglesDuJeu)
        bouton_regles.grid(row=0, column=2)

        # 4.4) Boutons pour annuler et sauvegarder
        bouton_frame_deux = Frame(self)
        bouton_frame_deux.grid()
        bouton_annuler = Button(bouton_frame_deux, text="Annuler Coup", command=self.annuler_coup)
        bouton_annuler.grid(row=0, column=0)
        bouton_sauvegarder = Button(bouton_frame_deux, text="Sauvegarder", command=self.sauvegarder_partie)
        bouton_sauvegarder.grid(row=0, column=1)

        # 4.5) Montrer le nombre de coups que l'utilisateur a joué. On crée un attribut compteur_tk (objet StringVar)
        # car l'objet label peut le prendre en paramètre et fera une mise à jour à chaque fois que le texte
        # dans l'objet change. 
        self.comteur_tk = StringVar()
        self.comteur_tk.set("Nombre de coups: " + str(self.compteur_de_tour))
        message_frame_un = Frame(self)
        message_frame_un.grid()
        nombre_de_coups_joues = Label(message_frame_un, 
            textvariable= self.comteur_tk, fg = "blue")
        nombre_de_coups_joues.grid(row=0, column=0)

        # 5) Définir un cadre qui contiendra les boutons reliés au jeux et placer ces derniers dessus.
        # Définir le message de bienvenue et l'afficher à l'utilisateur.
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        messageBienvenue = """
        Bienvenue dans le jeu de démineur.\n
        Pour commencer, cliquer sur l'onglet "Nouvelle Partie".
        """
        Label(self.cadre, text=messageBienvenue, bg="light blue" ,fg="red", font = "Helvetica 10 bold italic").grid()

        # 6) Avoir un 'Frame' pour d'autres informations
        self.autre_info = Frame(self)
        self.autre_info.grid()

    def devoiler_case(self, event):
        """
        Dévoile le contenu d'une case clické par l'utilisateur. Si cette case contient 0 on dévoile ses voisins. Si la case contient
        une mine un son est joué et la partie se termine(un message s'affiche). S'il ne reste plus de case à dévoiler la 
        partie est gagné(un message s'affiche).
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
            event : Évenement engendrer par l'utilisateur.
        """
        # 1) Déterminer de ou viens l'input de l'utilisateur en utilisant "grid_info()".
        # On saura quel bouton est clické.
        bouton = event.widget
        rangee_x = bouton.grid_info()["row"] + 1
        colonne_y = bouton.grid_info()["column"] + 1
        case = self.dictionnaireBoutons[(rangee_x, colonne_y)].case
        
        # 2) On va décrémenter le compteur seulement si la case n'a pas été dévoilée.
        if not case.est_devoilee:       
            self.compteur_de_tour += 1
            self.comteur_tk.set("Nombre de coups : " + str(self.compteur_de_tour))     
            
            # 2.1) Si la case n'est pas minée, on va la dévoiler (et ses voisins si '0'). 
            if not case.est_minee:
                cases_devoilees = self.tableau_mines.devoiler_case(rangee_x, colonne_y)
                nombre_c = 0

                # 2.2) On prend l'ensemble des cases dévoilés par la classe Tableau et on les ajoute
                # à la liste des cases dévoilés (on en a besoin pour annuler les coups plus tard)
                if cases_devoilees != None:
                    for ma_c in cases_devoilees:
                        if ma_c not in self.liste_case_devoilee:
                            self.liste_case_devoilee.append(ma_c)
                            nombre_c += 1
                
                self.nombre_case_devoile.append(nombre_c)
                
                # 2.3) On dévoile les cases sur l'interface tkinter.
                for case_coord in self.liste_case_devoilee:
                    mon_bouton = self.dictionnaireBoutons[case_coord]
                    mon_bouton.bouton_tk["text"] = mon_bouton.nombre_mine_voisines
                    mon_bouton.bouton_tk["fg"] = mon_bouton.couleur

            # 3) Dans le cas ou la case clické contient une mine.
            else:
                #3.1) Détruire les autre infos et montrer le message de perte.
                self.detruire_autre_info()
                self.wave_obj_two.play()
                self.statut_partie = 'perdu'
                Label(self.autre_info, text="Désolé! Vous avez perdu!", 
                    bg="red" ,fg="black", font = "Helvetica 15 bold italic").grid()
                
                
                nombre_de_cases_devoilees = 0
                self.tableau_mines.nombre_cases_sans_mine_a_devoiler = 0

                # 3.2) Parcourir le dictionnaire et enlever l'event '<Button-1>' lorsqu'on perd
                # Pour ne pas avoir de comportements bizards.
                for key, value in self.dictionnaireBoutons.items():
                    value.bouton_tk.unbind('<Button-1>')
                    
                    # 3.3) Montrer la solution et ajouter les cases dans la liste des cases dévoilées
                    # pour laisser l'utilisateur annuler le coup.
                    if key not in self.liste_case_devoilee:
                        self.liste_case_devoilee.append(key)
                        value.case.est_devoilee = True
                        nombre_de_cases_devoilees += 1

                        # 3.4) Charger de l'information importante sur les cases qui sont des mines.
                        if value.case.est_minee:
                            value.imageBombe = self.imageBombe
                            value.bouton_tk['image'] = self.imageBombe
                            value.bouton_tk["height"] = 24
                            value.bouton_tk["width"] = 18
                        
                        else:
                            value.bouton_tk["text"] = value.nombre_mine_voisines
                            value.bouton_tk["fg"] = value.couleur
                
                self.nombre_case_devoile.append(nombre_de_cases_devoilees)
        
        # 4) Jouer le son dans le cas ou on a gagné ou que la partie est en cours
        if self.statut_partie == None or self.statut_partie == 'gagné':
            self.wave_obj_one.play()

        # 5) S'il ne reste plus de mines et que toutes les cases sont dévoilées, afficher le message de victoire.
        if not self.tableau_mines.contient_cases_a_devoiler() and self.statut_partie != 'perdu':
            self.detruire_autre_info()
            self.statut_partie = 'gagné'
            Label(self.autre_info, text="Félicitations! Vous avez gagné!", 
                bg="green" ,fg="red", font = "Helvetica 15 bold italic").grid()
            
            for key, value in self.dictionnaireBoutons.items():
                value.bouton_tk.unbind('<Button-1>')


    def nouvelle_partie(self):
        """
        Création d'une nouvelle partie. Demande le nombre de lignes et de colonnes. Possibilité de charger une ancienne partie 
        sauvegarder en fichier ou de retourner dans une partie déjà commencée.
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
        """
        # 1) Remettre le cadre principal à neuf en le détruisant.
        self.detruireCadre()
        self.detruire_autre_info()

        self.fenetre_jeu = False
        
        # 2) Option #1 : Demander de rentrer un nombre de ligne, de colonnes et de mines.
        Label(self.cadre, text="OPTION 1 : COMMENCER UNE NOUVELLE PARTIE", font=("Courier", 10),fg="red").grid(columnspan = 2)

        Label(self.cadre, text="Nombre de ligne").grid(row=2,column=0)
        Label(self.cadre, text="Nombre de colonnes").grid(row=3,column=0)
        Label(self.cadre, text="Nombre de mines").grid(row=4,column=0)

        nombre_ligne = Entry(self.cadre)
        nombre_ligne.grid(row=2, column=1)
        nombre_colonne = Entry(self.cadre)
        nombre_colonne.grid(row=3, column=1)
        nombre_mine = Entry(self.cadre)
        nombre_mine.grid(row=4, column=1)

        
        Button(self.cadre, text="Créer Nouvelle Partie!",
        command = lambda : self.validerNouvellePartie(
            nombre_ligne.get(), nombre_colonne.get(), nombre_mine.get())).grid(columnspan = 2)

        # 3) Option #2 : Demander de rentrer un fichier.
        Label(self.cadre, text="OPTION 2 : TÉLÉCHARGER UNE PARTIE EXISTANTE", font=("Courier", 10) ,fg="red").grid(columnspan = 2)
        Label(self.cadre, text="Clicques sur ce bouton pour reprendre une partie existante.")
        Button(self.cadre, text="Télécharger Partie!", command=self.fichierTexte).grid(columnspan=2)

        # 4) Si on est dans une partie commencé, on donne l'option d'y retourner à partir de cette fenêtre
        if self.dansPartie:
            Label(self.autre_info, text="OPTION 3 : RETOURNER À LA PARTIE COMMENCÉ", font=("Courier", 10),fg="red").grid(columnspan = 2)
            Button(self.autre_info, text="Retour au jeu", command=self.jouer).grid(columnspan = 2)

        
    def reglesDuJeu(self):
        """
        Définie et donne à l'utilisateur les règles du jeu de démineur.

        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
        """

        # 1) Définir un "str" contenant les règles de notre jeu.
        reglesDuJeu = """
        1) Le but du jeu est de découvrir toutes les cases libres sans faire exploser les mines.\n
        2) Pour libérer une case, faire un clic gauche (clic normal).\n
        3) Le compteur en haut indique le nombre de coups joués.\n
        4) Le chiffre qui s'affiche sur les cases cliquées indique le nombre de mines se trouvant\n
        à proximité : à gauche ou à droite, en haut ou en bas, ou en diagonale.
        """

        # 2) Pour que sa ressemble plus ou moins à une "single page application", on va détruire le "Frame"
        # de l'attribut "self.cadre" et en recréer un nouveau pour mettre les informations relatives aux
        # régles du jeu.
        self.detruireCadre()
        self.detruire_autre_info()

        self.fenetre_jeu = False

        regles = Label(self.cadre, text=reglesDuJeu, bg='lightgreen', font=('times', 11, 'italic'))
        regles.grid(padx=10, pady=10)

        # 3) Si le joueur est dans une partie et qu'il a clické sur les règles, lui donner l'option de revenir.
        if self.dansPartie:
            Button(self.autre_info, text="Retour au jeu", command=self.jouer).grid()

    
    def quitterPartie(self):
        """
        Si utilisateur veut quitter la partie on valide sa décision avec un message de vérification pour ne pas qu'il perde 
        sa partie par accident.
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
        """

        # 1) Le message que l'on veut afficher et afficher le message avec messagebox.
        message = "Êtes vous sur de voulour quitter maintenant?"
        decision = messagebox.askquestion("Quitter", message)

        # 2) Messagebox retourne un "str" en fonction de ce que l'utilisateur à cliqué.
        # Si c'est "yes", on quitte le jeu.
        if decision == "yes":
            self.quit()

    
    def jouer(self):
        """
        Création de l'interface d'une partie selon les cases qui ont été dévoiler antérieurement.
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
        """

        # 1) On détruit le cadre précédent.
        self.detruireCadre()
        self.detruire_autre_info()
        

        self.fenetre_jeu = True

        # 2) On fait une boucle pour créer les boutons sur le cadre principal lorsque la fonction jouer()
        # se fait appeler pour la première fois (dictionnaireBoutons est vide)
        if len(self.dictionnaireBoutons) == 0:
            for i in range(self.tableau_mines.dimension_rangee):
                for j in range(self.tableau_mines.dimension_colonne):
                    bouton = BoutonCase(self.cadre, i+1, j+1, self.tableau_mines.obtenir_case( i+1, j+1))
                    bouton.bouton_tk.grid(row=i, column=j)
                    bouton.bouton_tk.bind('<Button-1>', self.devoiler_case)
                    self.dictionnaireBoutons[(i+1, j+1)] = bouton

        # 3) Dans le cas ou les boutons on déjà été initialisé, on va reconstruire la partie à partir des infos
        # que l'on a déjà (dans le dictionnaireBoutons).
        else:
            for i in range(self.tableau_mines.dimension_rangee):
                for j in range(self.tableau_mines.dimension_colonne):
                    # 3.1) Les boutons exitent dans le dictionnaire mais ne sont pas relié à un frame.
                    # On va donc les relier.
                    bouton = self.dictionnaireBoutons[(i+1, j+1)]
                    bouton.changer_cadre(self.cadre)
                    bouton.bouton_tk.grid(row=i, column=j)
                    if self.statut_partie == None:
                        bouton.bouton_tk.bind('<Button-1>', self.devoiler_case)

        # 4) Afficher si on a gagné ou perdu lorsque le joueur avait quitté la fenêtre de jeu.
        if self.statut_partie == 'gagné':
            Label(self.autre_info, text="Félicitations! Vous avez gagné!", 
                bg="green" ,fg="red", font = "Helvetica 15 bold italic").grid()
        
        elif self.statut_partie == 'perdu':
            Label(self.autre_info, text="Désolé! Vous avez perdu!", 
                bg="red" ,fg="black", font = "Helvetica 15 bold italic").grid()


    def validerNouvellePartie(self, nombre_ligne, nombre_colonne, nombre_mine):
        """
        Vérification des valeurs entrées par l'utilisateur nécessaire à la création d'une partie. 
        Message d'erreur qui s'affiche en cas d'erreur.
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
            nombre_ligne(int): Nombre de lignes que contient une partie.
            nombre_colonne(int): Nombre de colonnes que contient une partie.
            nombre_mine(int): Nombre de mines que contient une partie.
        """

        # 1) Pour éviter des erreurs, s'assurer que l'utilisateur nous donne bien des nombres.        
        if nombre_ligne.isnumeric() and nombre_colonne.isnumeric() and nombre_mine.isnumeric():
            # 2) Convertir les valeurs en nombres.
            nombre_ligne = int(nombre_ligne)
            nombre_colonne = int(nombre_colonne)
            nombre_mine = int(nombre_mine)

            # 3) S'assurer que les valeurs sont au dessus de 0 et que le nombre de mines est inférieur à la
            # taille du tableau.
            if nombre_ligne > 0 and nombre_colonne > 0 and nombre_mine > 0 and nombre_mine <= nombre_colonne * nombre_ligne:
                # 3.1) Créer une nouvelle instance de tableau
                self.tableau_mines = Tableau(nombre_ligne, nombre_colonne, nombre_mine)
                # 3.2) Appeler la méthode jouer qui va générer les boutons sur l'interface.
                # Il faut aussi réinitialiser tout les paramètres initiaux.
                self.compteur_de_tour = 0
                self.statut_partie = None
                self.dansPartie = True
                self.dictionnaireBoutons = dict()
                self.liste_case_devoilee = []
                self.nombre_case_devoile = []
                self.jouer()
            
            # 4) Afficher message d'erreur nombre de mines supérieur à taille du tableau.
            else:
                self.detruire_autre_info()
                Label(self.autre_info, text="Le nombre de mine est plus grand que la taille du tableau", 
                bg="black" ,fg="red", font = "Helvetica 10 bold italic").grid()
         
         # 5) Afficher message d'erreur si valeur entrée n'est pas numérique.
        else:
            self.detruire_autre_info()
            Label(self.autre_info, text="une des valeurs n'est pas numérique", 
            bg="black" ,fg="red", font = "Helvetica 10 bold italic").grid()

    def fichierTexte(self):
        """
        Va chercher les informations d'un fichier pour les utiliser dans une future partie. Les informations sont 
        instauré dans les attributs et caractéristiques d'une occurence de partie.
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
        """   

        # 1) Imposer à l'utilisateur de nous envoyer un fichier texte.
        fichier_texte = filedialog.askopenfile(mode='r',title="Séléctionnez un fichier", filetypes=(('text file', '.txt'),))

        # 2) Toujours essayer d'ouvrir le fichier.

        lecture_fichier = open(fichier_texte.name, 'r')
        lecture_fichier = lecture_fichier.readlines()

        # 3) Définir quelques variables dont on aura besoin pour reconstruire le jeu.
        count = 0
        liste_case_devoilee = []
        nombre_case_devoilee = []
        case_sans_mine_restante = 0
        dictionaire_de_case = dict()
        nombre_rangee = 0
        nombre_colonne = 0
        nombre_mines = 0

        try:
        # 4) Parcourrir le fichier ligne par ligne.
            for line in lecture_fichier:
                # 5) Ligne 0 = nombre de cases restantes sans mines à dévoiler.
                if count == 0:
                    case_sans_mine_restante = int(line)

                # 6) Ligne 1 = liste des cases qui ont été dévoilées 
                if count == 1 and line != 'None\n':
                    line = line.split(':')
                    for n in line:
                        newN = n.split(',')
                        if newN[0].isnumeric() and newN[1].isnumeric():
                            ma_tuple = (int(newN[0]), int(newN[1]))
                            liste_case_devoilee.append(ma_tuple)

                # 7) Ligne 2 = Nombre de cases dévoilés à chaque coup.              
                elif count == 2 and line != 'None\n':
                    line = line.split(',')
                    
                    for n in line:
                        if n.isnumeric():
                            n = int(n)
                            nombre_case_devoilee.append(n)

                # 8) Ligne 3 et au dessus, représentent les objets de type cases
                elif count > 2:
                    line = line.split(':')
                    ma_tuple = None

                    newLine = line[0].split(',')

                    if newLine[0].isnumeric() and newLine[1].isnumeric():
                        mon_x = int(newLine[0])
                        mon_y = int(newLine[1])
                        ma_tuple = (mon_x, mon_y)

                        # 8.1) Trouver la taille du tableau à partir des éléments max et min des cases.
                        if mon_x > nombre_rangee:
                            nombre_rangee = mon_x

                        if mon_y > nombre_colonne:
                            nombre_colonne = mon_y
                    
                    # 8.2) Créer objet case
                    case = la_case_de_jeu()

                    # 8.3) Changer l'objet cases en fonction des informations sur le fichier texte.
                    if line[1][0] == "Y":
                        case.est_minee = True
                        nombre_mines += 1

                    if line[1][1] == "Y":
                        case.est_devoilee = True
                    
                    if line[1][2].isnumeric():
                        case.nombre_mines_voisines = int(line[1][2])
                        
                    if ma_tuple != None:
                        dictionaire_de_case[ma_tuple] = case
                
                count += 1

            # 9) Création de l'objet Tableau et modification à travers les informations du fichier texte.
            self.tableau_mines = Tableau(nombre_rangee, nombre_colonne, nombre_mines)
            self.tableau_mines.dictionnaire_cases = dictionaire_de_case
            self.tableau_mines.nombre_cases_sans_mine_a_devoiler = case_sans_mine_restante

            # 10) Mettre à jour la liste des cases et la liste des cases dévoilées et le dictionaire de boutons.
            self.liste_case_devoilee = liste_case_devoilee
            self.nombre_case_devoile = nombre_case_devoilee
            self.dictionnaireBoutons = dict()
            # 11) Création des objets BoutonCase (avec valeurs appropriés) et mettre dans le dictionaire de boutons.
            for key, value in dictionaire_de_case.items():
                self.dictionnaireBoutons[key] = BoutonCase(self.cadre, key[0], key[1], value)
            
            # 12) Mettre à jour les variables d'état de la partie.
            self.compteur_de_tour = len(self.nombre_case_devoile)
            self.comteur_tk.set("Nombre de coups : " + str(self.compteur_de_tour))
            self.dansPartie = True
            self.statut_partie = None
            self.jouer()


        # 13) Afficher un message à l'utilisateur au cas ou le fichier n'a pas pu être traité
        except:
            self.detruire_autre_info()
            Label(self.autre_info, text="Désolé! Nous ne sommes pas parvenu à traiter le fichier!", 
                bg="red" ,fg="black", font = "Helvetica 13 bold italic").grid()
    
    def detruireCadre(self):
        """
        Sert à remmettre le cadre de jeu à neuf. On le détruit et on le reconstruit.
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
        """

        # 1) Cette méthode va servire à remettre le cadre du jeu à neuf. On le détruit et le reconstruit.
        # Je le met dans une fonction pour maximiser la réusabilité du code.
        self.cadre.destroy()
        self.cadre = Frame(self)
        self.cadre.grid()

    def detruire_autre_info(self):
        # 1) Détruire et reconstruire le cadre d'autre informations.
        self.autre_info.destroy()
        self.autre_info = Frame(self)
        self.autre_info.grid()

    def annuler_coup(self):
        # 1) On peut annuler seulement lorsqu'on a commencé une partie (il y a des cases dévoilées)
        # et qu'on est dans la fenêtre de jeu.
        if len(self.nombre_case_devoile) > 0 and self.fenetre_jeu:
            if self.statut_partie == 'gagné' or self.statut_partie == 'perdu':
                self.statut_partie = None
                self.detruire_autre_info()

                # 2) Lorsqu'on a perdu ou gagné, on enlève les événements aux boutons.On fait la tâche 
                # inverse de redonner les événements si l'utilisateur annule un coup (perdu ou gagné) 
                for key, value in self.dictionnaireBoutons.items():
                    value.bouton_tk.bind('<Button-1>', self.devoiler_case)


            # 3) Déterminer le nombre de cases dévoilés au dernier coup
            nombre_case_devloilees = self.nombre_case_devoile[-1]

            # 3.1) Mettre à jour le compteur
            self.compteur_de_tour -= 1
            self.comteur_tk.set("Nombre de coups : " + str(self.compteur_de_tour))

            # 4) Passer à travers les cases dévoilés lors du dernier coup et les rendre cachés
            for nombre in range(0, nombre_case_devloilees):
                mes_coordonnes = self.liste_case_devoilee[- (nombre + 1)]
                mon_objet = self.dictionnaireBoutons[mes_coordonnes]

                mon_objet.case.est_devoilee = False
                mon_objet.texte = " "
                mon_objet.bouton_tk["text"] = " "

                # 4.1) Incrémenter le nombre de cases sans mine (objet Tableau) seulement si la case dévoilée
                # n'étais pas miné
                if not mon_objet.case.est_minee:
                    self.tableau_mines.nombre_cases_sans_mine_a_devoiler += 1
                
                # 4.2) Ajuster la case d'image si c'étais une mine
                else:
                    mon_objet.bouton_tk['image'] = ''
                    mon_objet.bouton_tk["height"] = 1
                    mon_objet.bouton_tk["width"] = 2
                
            # 5) Enlever les cases dévoilés dans la liste des cases dévoilés et enlever le nombre de cases dévoilés
            # dans la liste de nombre de cases dévoilés
            for nombre in range(0, nombre_case_devloilees):
                self.liste_case_devoilee.pop(-1)

            self.nombre_case_devoile.pop(-1)

    def sauvegarder_partie(self):
        """
        Sauvegarde une partie dans une fichier texte si elle n'est pas terminée
        
        Args:
            self : Occurence d'une partie(objet de la classe InterfacePartie).
        """

        # 1) Sauvegarder une partie seulement si elle n'est pas terminée
        if self.dansPartie and self.statut_partie == None and self.fenetre_jeu:
            try:
                # 2) Demander à l'utilisateur de sauvegarder le fichier
                my_file = filedialog.asksaveasfilename(title="Séléctionnez un fichier", filetypes=(('Text File', '.txt'),))
                # 3) Ouvrir et fermer pour s'assurer que le fichier est vierge et réouvrir avec 'append'.                
                clear_file = open(my_file, 'w')
                clear_file.close()
                my_file = open(my_file, 'a')
                
                # 4) Écrire le nombre de mine sans cases à dévoiler dans la première ligne
                my_file.write(str(self.tableau_mines.nombre_cases_sans_mine_a_devoiler) + '\n')
                
                # 5) Si la partie et commencé on va écrire les deux listes qu'on utilise.
                # Sinon on va écrire 'None'.
                if len(self.liste_case_devoilee) > 0:
                    for coord in self.liste_case_devoilee:
                        my_x, my_y = coord
                        message = str(my_x) + ',' +str(my_y) + ':'
                        my_file.write(message)
                    
                    my_file.write('\n')

                    for nombre in self.nombre_case_devoile:
                        message = str(nombre) + ','
                        my_file.write(message)
                    
                    my_file.write('\n')

                else:
                    my_file.write('None\n')
                    my_file.write('None\n')

                
                # 6) Écrire chacune des cases et ses propriétés dans le fichier texte.
                dictionaire_case = self.tableau_mines.dictionnaire_cases

                for key, value in dictionaire_case.items():
                    mon_x, mon_y = key
                    position = str(mon_x) + ',' + str(mon_y) + ':'
                    est_minee = 'N'
                    est_devoilee = 'N'
                    nombre_mines = value.nombre_mines_voisines

                    if value.est_minee:
                        est_minee = 'Y'
                    
                    if value.est_devoilee:
                        est_devoilee = 'Y'

                    position += est_minee + est_devoilee + str(nombre_mines) + '\n'

                    my_file.writelines(position)
                
                my_file.close()

            # 7) Afficher un message d'erreur si quelque chose se passe mal.
            except:
                self.detruire_autre_info()
                Label(self.autre_info, text="Désolé! Nous ne sommes pas parvenu à traiter le fichier!", 
                    bg="red" ,fg="black", font = "Helvetica 13 bold italic").grid()
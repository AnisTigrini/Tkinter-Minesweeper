# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Tableau. Un tableau est utilisé pour jouer une partie du jeu Démineur.

Auteurs: Anis Tigrini
"""

from case import Case
from random import randint


class Tableau():
    """
    Tableau du jeu de démineur, implémenté avec un dictionnaire de cases.
    
    Warning:
        Si vous ajoutez des attributs à la classe Tableau, n'oubliez pas de les documenter ici.

    Attributes:
        dimension_rangee (int): Nombre de rangées du tableau
        dimension_colonne (int): Nombre de colonnes du tableau
        nombre_mines (int): Nombre de mines cachées dans le tableau

        nombre_cases_sans_mine_a_devoiler (int) : Nombre de cases sans mine qui n'ont pas encore été dévoilées
            Initialement, ce nombre est égal à dimension_rangee * dimension_colonne - nombre_mines

        dictionnaire_cases (dict): Un dictionnaire de case en suivant le format suivant:
            Les clés sont les positions du tableau sous la forme d'un tuple (x, y), 
                x étant le numéro de la rangée, y étant le numéro de la colonne.
            Les éléments sont des objets de la classe Case.
    """
    def __init__(self, dimension_rangee=5, dimension_colonne=5, nombre_mines=5):
        """ Initialisation d'un objet tableau.
        
        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau (valeur par défaut: 5)
            dimension_colonne (int): Nombre de colonnes du tableau (valeur par défaut: 5)
            nombre_mines (int): Nombre de mines cachées dans le tableau (valeur par défaut: 5)
        """ 
    
        self.dimension_rangee = dimension_rangee
        self.dimension_colonne = dimension_colonne
        self.nombre_mines = nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la fonction initialiser_tableau().
        self.dictionnaire_cases = {}

        self.initialiser_tableau()

        self.nombre_cases_sans_mine_a_devoiler = self.dimension_rangee * self.dimension_colonne - self.nombre_mines

    
    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Valide les coordonnées reçues en argument. Les coordonnées sont considérées valides si elles se trouvent bien
        dans les dimensions du tableau.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        
        Returns:
            bool: True si les coordonnées (x, y) sont valides, False autrement
        """
        rangee_valide = rangee_x >= 1 and rangee_x <= self.dimension_rangee
        colonne_valide = colonne_y >= 1 and colonne_y <= self.dimension_colonne
        return rangee_valide and colonne_valide
    
    def obtenir_case(self, rangee_x, colonne_y):
        """
        Récupère une case à partir de ses numéros de ligne et de colonne
        
        Args:
            rangee_x (int) : Numéro de la rangée de la cas
            colonne_y (int): Numéro de la colonne de la case
        Returns:
            Case: Une référence vers la case obtenue
            (ou None si les coordonnées ne sont pas valides)
        """
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return None
        
        coordonnees = (rangee_x, colonne_y)
        return self.dictionnaire_cases[coordonnees]

    def obtenir_voisins(self, rangee_x, colonne_y):
        """
        Retourne une liste de coordonnées correspondant aux cases voisines d'une case. Toutes les coordonnées retournées
        doivent être valides (c'est-à-dire se trouver à l'intérieur des dimensions du tableau).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut connaître les cases voisines
            colonne_y (int): Numéro de la colonne de la case dont on veut connaître les cases voisines

        Returns:
            list : Liste des coordonnées (tuple x, y) valides des cases voisines de la case dont les coordonnées
            sont reçues en argument
        """
        voisinage = ((-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1))

        liste_coordonnees_cases_voisines = []

        # TODO: Générer la liste des coordonnées valides des cases voisine. Le tuple voisinage est là pour vous aider.
        # 1) Faire une boucle pour toutes les valeurs du voisinage de la case
        for voisin in voisinage:
            # 2) Déstructurer la tuple pour s'assurer d'avoir les valeurs numériques
            x,y = voisin
            # 3) S'assurer que la tuple obtenue est entre 1 et la dimension maximale du tableau
            if x + rangee_x >= 1 and x + rangee_x <= self.dimension_rangee and y + colonne_y >= 1 and y + colonne_y <= self.dimension_colonne:
                # 4) Si c'est le cas, l'ajouter à notre liste sous forme de tuple.
                liste_coordonnees_cases_voisines.append((x + rangee_x, y + colonne_y))

        # 5) Retourner la liste des voisins
        return liste_coordonnees_cases_voisines

    def initialiser_tableau(self):
        """
        Initialise le tableau à son contenu initial en suivant les étapes suivantes:
            1) On crée chacune des cases du tableau (cette étape est programmée pour vous).
            2) On y ajoute ensuite les mines dans certaines cases qui sont choisies au hasard
                (attention de ne pas choisir deux fois la même case!).
                - À chaque fois qu'on ajoute une mine dans une case, on obtient la liste de 
                  ses voisins (pour se faire, utilisez la méthode obtenir_voisins)
                - Pour chaque voisin, on appelle la méthode ajouter_une_mine_voisine de la case correspondante.
        """
        for rangee_x in range(1, self.dimension_rangee+1):
            for colonne_y in range(1, self.dimension_colonne+1):
                coordonnees = (rangee_x, colonne_y)
                self.dictionnaire_cases[coordonnees] = Case()
        
        # TODO: À compléter (étape 2)
        # Nous vous suggérons d'utiliser dans la fonction randint(a,b) du module random qui 
        # retourne un entier aléatoire compris entre a et b inclusivement.
        nombre_de_mine = self.nombre_mines
        # 1) On fait une boucle correspondant au nombre de mines
        while nombre_de_mine > 0:
            # 2) On choisit une coordonnée aléatoire entre 1 et la taille max du tableau
            #   on y accède et on lui ajoute une mine.
            coordonnee_x = randint(1, self.dimension_rangee)
            coordonnee_y = randint(1, self.dimension_colonne)
            
            # 3) On ajoute une mine seulement lorsque la case n'est pas miné et on décrémente nombre de mine
            if self.obtenir_case(coordonnee_x, coordonnee_y).est_minee == False:
                nombre_de_mine -= 1
                self.obtenir_case(coordonnee_x, coordonnee_y).ajouter_mine()
                # 4) On fait une boucle et appelle la méthode ajoute_une_mine_voisine sur l'objet case voisin
                for case_voisine in self.obtenir_voisins(coordonnee_x, coordonnee_y):
                    # 5) L'élément 0 de case_voisine est "X" et l'élément 1 est "Y"
                    self.obtenir_case(case_voisine[0], case_voisine[1]).ajouter_une_mine_voisine()


    def valider_coordonnees_a_devoiler(self, rangee_x, colonne_y):
        """
        Valide que les coordonnées reçues en argument sont celles d'une case que l'on peut dévoiler 
        (donc que les coordonnées sont valides et que la case correspondante n'a pas encore été dévoilée).
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        
        Returns
            bool: True si la case à ces coordonnées (x, y) peut être dévoilée, False autrement (donc si la
                  case a déjà été dévoilée ou que les coordonnées ne dont pas valides).
        """  
        # TODO: À compléter
        # 1) Vérifier que les coordonées sont valides
        if self.valider_coordonnees(rangee_x, colonne_y):
            # 2) On retourne "Vrai" si la case n'a pas encore été dévoilée
            if self.obtenir_case(rangee_x, colonne_y).est_devoilee == False:
                return True
        # 3) Dans le cas que le case à été dévoilée, on retourne "False"
        return False
        
    def afficher_solution(self):
        """
        Méthode qui affiche le tableau de la solution à l'écran. La solution montre les 
        mines pour les cases qui en contiennent et la valeur du nombre de mines voisines 
        pour les autres cases.
        
        Important: Vous n'avez pas à modifier cette méthode, mais vous pouvez vous
        en inspirer pour écrire la méthode afficher_tableau().
        """
        print() # Retour de ligne
        
        for rangee_x in range(0, self.dimension_rangee+1):
            
            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0: 
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |' 
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne 
                    # (si y > 10, on affiche seulement l'unité pour éviter les décalages)
                    car = f'{colonne_y%10}' 
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|' 
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)  
                    if case_xy.est_minee:
                        car = 'M'
                    else:
                        car = str(case_xy.nombre_mines_voisines)
                
                # Afficher le caractère suivit d'un espace (sans retour de ligne)
                print(car, end=" ")
            
            # À la fin de chaque ligne
            print() # Retour de ligne
            if rangee_x == 0: # Ligne horizontale de l'en-tête
                print('--+-' + '--'*self.dimension_colonne) 
         
    def afficher_tableau(self):
        """
        Méthode qui affiche le tableau à l'écran. Le tableau montre le contenu des cases dévoilées 
        (mine ou nombre de mines voisines) ou un point pour les cases non dévoilées.
        """
        # TODO: À compléter
        print() # Retour de ligne
        
        for rangee_x in range(0, self.dimension_rangee+1):
            
            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0: 
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |' 
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne 
                    # (si y > 10, on affiche seulement l'unité pour éviter les décalages)
                    car = f'{colonne_y%10}' 
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|' 
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)  
                    if case_xy.est_devoilee:
                        car = str(case_xy.nombre_mines_voisines)
                    else:
                        car = "*"
                
                # Afficher le caractère suivit d'un espace (sans retour de ligne)
                print(car, end=" ")
            
            # À la fin de chaque ligne
            print() # Retour de ligne
            if rangee_x == 0: # Ligne horizontale de l'en-tête
                print('--+-' + '--'*self.dimension_colonne)         
        
    
    def contient_cases_a_devoiler(self):
        """
        Méthode qui indique si le tableau contient des cases à dévoiler.
        
        Returns:
            bool: True s'il reste des cases à dévoiler, False autrement.

        """
        # TODO: À compléter
        return self.nombre_cases_sans_mine_a_devoiler > 0

    def devoiler_case(self, rangee_x, colonne_y):
        """
        Méthode qui dévoile le contenu de la case dont les coordonnées sont reçues en argument. Si la case ne
        contient pas de mine, on décrémente l'attribut qui représente le nombre de cases sans mine à dévoiler. 
        Aussi, si cette case n'est voisine d'aucune mine, on dévoile ses voisins. 
       
        Args:
            rangee_x (int) : Numéro de la rangée de la case à dévoiler
            colonne_y (int): Numéro de la colonne de la case à dévoiler
        """
        # TODO: À compléter   
        # 1) Obtenir la case et la dévoiler et exécuter le code si la case retournée est valide (pas égal à "None")
        la_case = self.obtenir_case(rangee_x, colonne_y)
        # 1.1) On vérifie que la case est valide avant d'exécuter le code plus loin.
        if la_case != None and not la_case.est_devoilee:
            la_case.devoiler()
            # 2) Regarder si la case ne contient pas de mine avant de décrémenter le nombre de case sans mine à dévoiler
            if self.contient_mine(rangee_x, colonne_y) == False:
                self.nombre_cases_sans_mine_a_devoiler -= 1
                
                # 3) On regarde si la case n'est pas voisine d'une mine (case 0). Si ce n'est pas le cas, on va récupérer les cases voisines
                liste_des_cases_voisins = []
                if la_case.est_voisine_d_une_mine() == False:
                    liste_des_cases_voisins = self.obtenir_voisins(rangee_x, colonne_y)
                    liste_des_cases_voisins.append((rangee_x, colonne_y))

                    for case_voisine in liste_des_cases_voisins:
                        r_x, c_y = case_voisine
                        ma_case = self.obtenir_case(r_x, c_y)
                        
                        if ma_case != None:
                            if not ma_case.est_voisine_d_une_mine():
                                liste_des_cases_ajouter = self.obtenir_voisins(r_x, c_y)
                                for une_case in liste_des_cases_ajouter:
                                    if une_case not in liste_des_cases_voisins:
                                        liste_des_cases_voisins.append(une_case)

                    # 4) On va faire une boucle pour dévloiler ces cases voisines (si elle n'ont pas déjà été dévoilées)
                    for case_voisine in liste_des_cases_voisins:
                        if self.dictionnaire_cases[case_voisine].est_devoilee == False:
                            self.dictionnaire_cases[case_voisine].devoiler()
                            self.nombre_cases_sans_mine_a_devoiler -= 1
                    

                else:
                    liste_des_cases_voisins.append((rangee_x, colonne_y))

                return liste_des_cases_voisins
        
    def contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en argument contient une mine.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut vérifier si elle contient une mine
        
        Returns:
            bool: True si la case à ces coordonnées (x, y) contient une mine, False autrement.
        """
        # TODO: À compléter   
        return self.obtenir_case(rangee_x, colonne_y).est_minee


#### Tests unitaires (à compléter) ###

def test_initialisation():
    tableau_test = Tableau()

    assert tableau_test.contient_cases_a_devoiler()
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == tableau_test.dimension_colonne * \
        tableau_test.dimension_rangee - tableau_test.nombre_mines

def test_valider_coordonnees():

    tableau_test = Tableau()
    dimension_x, dimension_y = tableau_test.dimension_rangee, tableau_test.dimension_colonne

    assert tableau_test.valider_coordonnees(dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x+1, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x, dimension_y+1)
    assert not tableau_test.valider_coordonnees(-dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(0, 0)
    
def test_obtenir_voisins():
    # TODO: À compléter. 
    tableau_test = Tableau()
    # 1) On regarde les coordonnées extrèmes et milieu du tableau
    assert tableau_test.obtenir_voisins(1,1) == [(1,2), (2,1), (2,2)]
    assert tableau_test.obtenir_voisins(5,5) == [(4,4), (4,5), (5,4)]
    assert tableau_test.obtenir_voisins(2,2) == [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]
    
    # *** On garde en tête que cette fonction aura toujours des bons paramètre car la validation des entrées
    # de l'utilisateur se font dans le fichier partie.py (coordonnées dans le tableau + entrée numérique). ***
    
def test_valider_coordonnees_a_devoiler():
    # TODO: À compléter. 
    # On part du principe qu'on a un tableau 5*5
    tableau_test = Tableau()
    # 1) On s'assure que les coordonées mauvaise x ou y retourne "False"
    assert not tableau_test.valider_coordonnees_a_devoiler(-1, 2)
    assert not tableau_test.valider_coordonnees_a_devoiler(2, 8)
    assert not tableau_test.valider_coordonnees_a_devoiler(8, 8)

    # 2) Aucune case n'a été encore dévoilée, donc si on choisis une case valide au hasard, on devrait
    #   se faire retourner "True"
    assert tableau_test.valider_coordonnees_a_devoiler(1, 1)
    assert tableau_test.valider_coordonnees_a_devoiler(2, 2)
    assert tableau_test.valider_coordonnees_a_devoiler(5, 5)
    
def test_devoiler_case():
    # TODO: À compléter. 
    # On part du principe qu'on a un tableau 5*5
    tableau = Tableau()
    
    # 1) Dévoiler quelques cases à l'intérieur du tableau et s'assurer que c'est fidèle à la solution
    tableau.devoiler_case(1,1)
    assert tableau.obtenir_case(1,1).est_devoilee

    tableau.devoiler_case(3,3)
    assert tableau.obtenir_case(3,3).est_devoilee

    tableau.devoiler_case(5,5)
    assert tableau.obtenir_case(5,5).est_devoilee

    
def test_case_contient_mine():
    # TODO: À compléter. 
        # On part du principe qu'on a un tableau 5*5
    tableau_test = Tableau()

    # 1) Quand on génére le tableau, il met 5 mines dans des emplacement aléatoires.
    # on va aller chercher ces 5 mines en parcourant le tableau et s'assurer, avec des "assert"
    # qu'ils sont bel et bien là ou ils sont supposé être.
    coordCaseMine = []

    for range_x in range(1,6):
        for colonne_y in range(1,6):
            case = tableau_test.obtenir_case(range_x, colonne_y)
            
            # 1.1) Si la case est minée, on va l'ajouter les coord à notre tableau "caseMine"
            if case.est_minee:
                coordCaseMine.append((range_x, colonne_y))
    
    # 2) Vérifier que le tableau "coordCaseMine" contient bien 5 case minées
    assert len(coordCaseMine) == 5

    # 4) Faire les vérifications au niveau de la position des case
    for coord in coordCaseMine:
        case = tableau_test.obtenir_case(coord[0], coord[1])
        assert case.est_minee


if __name__ == '__main__':

    # Les cinq prochaines lignes de code sont là pour vous aider à tester votre
    # première tentative d'implémentation des méthodes initialiser_tableau et afficher_tableau.
    
    tableau_test = Tableau()
    print('\nTABLEAU:')
    tableau_test.afficher_tableau()
    print('\nSOLUTION:')   
    tableau_test.afficher_solution()
    
    print('Tests unitaires...')
    test_initialisation()
    test_valider_coordonnees()
    test_obtenir_voisins()
    test_valider_coordonnees_a_devoiler()
    test_devoiler_case()
    test_case_contient_mine()
    print('Tests réussis!')
    
    
    
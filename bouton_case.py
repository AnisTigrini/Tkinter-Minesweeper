"""
TODO: Ajoutez les docstrings et modifier le code au besoin.

On va préférer l'encapsulation à l'héritage
"""

from tkinter import Button

class BoutonCase():
    # 1) Constructeur standard avec un objet case et un objet nouton Tkinter en tant que paramètres
    def __init__(self, parent,rangee_x, colonne_y, case):
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        self.imageBombe = None
        self.case = case
        self.nombre_mine_voisines = case.nombre_mines_voisines
        self.texte = " "
        self.bouton_tk = Button(parent, text=self.texte, padx=1, pady=3, height=1, width=2)

        dict_couleurs = {0:"grey", 1:"green", 2:"blue"}

        if self.nombre_mine_voisines > 2:
            self.couleur = "red"
        else:
            self.couleur = dict_couleurs[self.nombre_mine_voisines]

    # 2) Cette fonction va servir à recharger le boutons dans l'interface lorsque l'utlisateur clique sur
    # une autre fenêtre (avec les informations qu'on aura enregistré sur leur état comme le texte si dévoilé,
    # l'image de bombe si c'est une bombe etc.).
    def changer_cadre(self, nouveau_cadre):
        self.bouton_tk.destroy()
        self.bouton_tk = Button(nouveau_cadre, text=self.texte, padx=1, pady=3, height=1, width=2)
        
        if self.case.est_devoilee:
            if self.imageBombe != None:
                self.bouton_tk['image'] = self.imageBombe
                self.bouton_tk["height"] = 24
                self.bouton_tk["width"] = 18

            else:
                self.bouton_tk["text"] = self.nombre_mine_voisines
                self.bouton_tk["fg"] = self.couleur

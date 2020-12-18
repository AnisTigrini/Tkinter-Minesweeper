# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Case. Une case peut contenir une mine
et être dans différents états de dévoilement.

Auteur: Anis Tigrini
"""


class Case:
    """
    Une case du tableau du jeu de démineur.
    
    Attributes:
        est_minee (bool): True si la case contient une mine, False autrement
        est_devoilee (bool): True si la case a été dévoilée, False autrement
        nombre_mines_voisines (int): Le nombre de mines présentes dans le voisinage de la case.
    """

    def __init__(self):
        """ 
        Initialisation de la classe avec des valeurs par défaut.
        """
        self.est_minee = False
        self.est_devoilee = False
        self.nombre_mines_voisines = 0

    def devoiler(self):
        """
        Cette méthode modifie le statut de la case lorsque son contenu est dévoilé.
        """
        self.est_devoilee = True

    def ajouter_mine(self):
        """
        Cette méthode permet d'ajouter une mine à la case en modifiant un attribut.
        """
        self.est_minee = True 
        
    def ajouter_une_mine_voisine(self):
        """
        Méthode qui incrémente l'attribut nombre_mines_voisines
        """
        self.nombre_mines_voisines += 1

    def est_voisine_d_une_mine(self):
        """
        Méthode qui indique si la case est voisine d'une mine ou nom
        Returns:
            bool: True si la case est voisine d'une mine, False autrement.
        """
        return self.nombre_mines_voisines > 0
    
    
if __name__ == '__main__':
    print('Tests unitaires...')
    
    une_case = Case()    
    assert not une_case.est_minee 
    assert not une_case.est_devoilee
    assert une_case.nombre_mines_voisines == 0
    
    une_case.devoiler()
    assert une_case.est_devoilee
    
    une_case.ajouter_mine()
    assert une_case.est_minee
    
    assert not une_case.est_voisine_d_une_mine()
    for i in range(1,5):
        une_case.ajouter_une_mine_voisine()
        assert une_case.nombre_mines_voisines == i
        assert une_case.est_voisine_d_une_mine()
    
    print('Tests réussis!')
    
    
    
    
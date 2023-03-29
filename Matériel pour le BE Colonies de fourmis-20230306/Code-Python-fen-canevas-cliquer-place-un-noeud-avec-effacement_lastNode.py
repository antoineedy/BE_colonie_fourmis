# Mars 2019
# Crée une fenetre, un canevas, place le noeud de départ
# Puis onclique pour placer les autres noeuds.
# Possibilité d'effacer les noeuds en allanat en arrière.
# Deux listes contiennent les noeuds et leurs coordonnées


from tkinter import *
from tkinter.messagebox import showinfo
import random


# --------------------------------------------------------


class ZoneAffichage(Canvas):
    def __init__(self, parent, w=500, h=400, _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h
        self.__liste_noeuds = []

        # Pour avoir un contour pour le Canevas
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)


    def get_dims(self):
        return (self.__w, self.__h)

    def not_used_keep_dessiner_graphe(self):
        for b in self.__liste_noeuds:
            b.deplacement()
        self.after(50, self.dessiner_graphe)  # Important, sinon on fera une seul execution

    def creer_noeud(self, x_centre, y_centre, rayon , col, fill_color="white"):
        noeud=Balle(self, x_centre, y_centre, rayon , col)
        self.pack()
        return noeud

    def action_pour_un_clique(self, event):
        print("Trace : (x,y) = ", event.x, event.y)
        #showinfo('Résultat ', "Arrrgh : vous avez dans la fenetre" + '\nThanks !')
        
        # Placer un noeud à l'endroit cliqué
        self.__fen_parent.placer_un_noeud(event.x, event.y)


    def not_used_set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)

    def placer_un_noeud_sur_canevas(self, x_centre, y_centre, col=None, fill_color="white"):
        w,h = self.get_dims()
        rayon=5
        if col == None :
            col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])

        node=self.creer_noeud(x_centre, y_centre, rayon , col, fill_color)
        self.update()

        self.__fen_parent.set_coordonnes_du_last_node(x_centre, y_centre)
        return node.get_node_ident()


class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('ESSAI GRAPHE')
        self.__zoneAffichage = ZoneAffichage(self)

        self.__zoneAffichage.pack()

        # ----------------------------
        # Création d'un widget Button (bouton Effacer)
        self.__boutonEffacer = Button(self, text='undo last node', command=self.undo_last_noeud).pack(side=LEFT, padx=5, pady=5)

        # Création d'un widget Button (bouton Effacer)
        self.__boutonEffacer = Button(self, text='Effacer', command=self.effacer).pack(side=LEFT, padx=5, pady=5)
        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self, text='Quitter', command=self.destroy).pack(side=LEFT, padx=5, pady=5)

        self.__zoneAffichage.bind('<Button-1>', self.__zoneAffichage.action_pour_un_clique)

        self.__liste_d_ident_d_objets_crees=[]
        self.__liste_coordonnes_centre_des_nodes=[]

        self.placer_noeud_depart()

    def add_a_node_to_your_list(self, noeud) :
        self.__liste_d_ident_d_objets_crees.append(noeud)
        
    def placer_un_noeud(self, x, y):
        node=self.__zoneAffichage.placer_un_noeud_sur_canevas(x,y)
        self.add_a_node_to_your_list(node)
        self.set_coordonnes_du_last_node(x,y)
        self.__liste_coordonnes_centre_des_nodes.append((x,y))


    def set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)

    def get_last_node(self):
        return self.__last_node

    def placer_noeud_depart(self):
        w,h = self.__zoneAffichage.get_dims()
        x_centre, y_centre=20, h//2
        node= self.__zoneAffichage.placer_un_noeud_sur_canevas(x_centre, y_centre, col="red", fill_color="red")
        self.add_a_node_to_your_list(node)
        self.__liste_coordonnes_centre_des_nodes.append((x_centre, y_centre))

    #--------------------------
    #

    def undo_last_noeud(self):
        print("Avant undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))
        if len(self.__liste_d_ident_d_objets_crees)==1 :
            print("Peut pas enlever noeud départ")
            return

        x_centre,  y_centre=self.get_last_node()

        last_node=self.__liste_d_ident_d_objets_crees.pop()

        # Pour supprimer, il faut can_id du noeud, pas le noeud lui mm !!
        self.__zoneAffichage.delete(last_node)
        self.__zoneAffichage.update()

        x_last_node,y_last_node=self.__liste_coordonnes_centre_des_nodes.pop()
        self.set_coordonnes_du_last_node(x_last_node,y_last_node)
        print("Après undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))

        

    def ajout_noeud(self):
        # Dessin d'un petit cercle
        x_centre,  y_centre = self.not_used_generer_un_point_XY_dans_une_bande()
        print("(x,y) =", x_centre, ' , ', y_centre)

        rayon=5
        col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])
        self.__zoneAffichage.creer_noeud(x_centre, y_centre, rayon , col)
        self.__zoneAffichage.update()
        self.__last_node=(x_centre, y_centre)


    def effacer(self):
        """ Efface la zone graphique """
        self.__zoneAffichage.delete(ALL)
        self.__liste_d_ident_d_objets_crees.clear()
        self.__liste_coordonnes_centre_des_nodes.clear()
        self.placer_noeud_depart()
#--------------------------
class Balle:
    def __init__(self, canvas, cx, cy, rayon, couleur, fill_color="white"):
        self.__cx, self.__cy = cx, cy
        self.__rayon = rayon
        self.__color = couleur
        self.__can = canvas  # Il le faut pour les déplacements

        self.__canid = self.__can.create_oval(cx - rayon, cy - rayon, cx + rayon, cy + rayon, outline=couleur, fill=fill_color)
        # Pour 3.6 : col: object  # essaie typage !

    def get_node_ident(self):
        return self.__canid

    def NoNeed_Here_not_used_generer_un_point_XY_dans_une_bande(self, last_x, last_y):
        w,h = self.__can.get_dims()
        #last_x, last_y=self.__last_node
        delta_x_centre = random.randint(10, 50); delta_y_centre = random.randint(10, 50)
        hasard_x=random.randint(0, 1); hasard_y=random.randint(0, 1)

        x_centre = last_x+random.randint(10, 50)* 1 if hasard_x else -1
        y_centre = last_y+random.randint(10, 50)* 1 if hasard_y else -1
        if x_centre < 0 :  x_centre*=-1
        if y_centre < 0 :  y_centre*=-1
        return (x_centre, y_centre)

    # Un seul déplacement
    def not_used_keep_deplacement(self):
        self.__can.move(self.__canid, 0, 0)


# ------------------------------------------------------
# Réutilisation des formes

# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()

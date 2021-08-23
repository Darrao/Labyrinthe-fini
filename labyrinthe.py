from graphe import graphe
from pilefile import pile
from tkinter import *
from time import sleep
from random import randint
from sys import setrecursionlimit

setrecursionlimit(10000)


def trace_lab(Tab_Lab):
    l_case = 800//largeur
    h_case = 600//hauteur
    canvas.delete("all")
    for i in range(largeur):
        for j in range(hauteur):
            if (Tab_Lab[i][j]&0b0001) == 1:
                canvas.create_line((i*l_case, j*h_case),((i+1)*l_case,j*h_case))
            if (Tab_Lab[i][j]&0b0010) == 2:
                canvas.create_line(((i+1)*l_case, j*h_case),((i+1)*l_case,(j+1)*h_case))
            if (Tab_Lab[i][j]&0b0100) == 4:
                canvas.create_line((i*l_case, (j+1)*h_case),((i+1)*l_case,(j+1)*h_case))
            if (Tab_Lab[i][j]&0b1000) == 8:
                canvas.create_line((i*l_case, j*h_case),(i*l_case,(j+1)*h_case))
    canvas.update()
            
def main_droite():
    """ Directions : Ouest = 3, Sud = 2, Est = 1, Nord = 0"""
    direction = 1
    x = 0
    y = 0
    bonhomme(x, y)
    while not(x == largeur-1 and y == 0):
        #print(x,y)
        if direction == 1 :
            if Tab[x][y]&0b0100 == 0 and y < hauteur-1:
                direction = 2
                y += 1
            elif Tab[x][y]&0b0010 == 0 and x < largeur-1:
                x += 1
            elif Tab[x][y]&0b0001 == 0 and y > 0:
                direction = 0
                y -= 1
            else :
                direction = 3
                x -= 1

        elif direction == 2 :
            if Tab[x][y]&0b1000 == 0 and x > 0:
                direction = 3
                x -= 1
            elif Tab[x][y]&0b0100 == 0 and y < hauteur-1:
                y += 1
            elif Tab[x][y]&0b0010 == 0 and x < largeur-1:
                direction = 1
                x += 1
            else :
                direction = 0
                y -= 1
        
        elif direction == 3 :
            if Tab[x][y]&0b0001 == 0 and y > 0:
                direction = 0
                y -= 1
            elif Tab[x][y]&0b1000 == 0 and x > 0:
                x -= 1
            elif Tab[x][y]&0b0100 == 0 and y < hauteur-1:
                direction = 2
                y += 1
            else :
                direction = 1
                x += 1

        else :
            if Tab[x][y]&0b0010 == 0 and x < largeur-1:
                direction = 1
                x += 1
            elif Tab[x][y]&0b0001 == 0 and y > 0:
                y -= 1
            elif Tab[x][y]&0b1000 == 0 and x > 0:
                direction = 3
                x -= 1
            else :
                direction = 2
                y += 1
        bonhomme(x, y)

def bonhomme(x, y, color = "green"):
    l_case = 800//largeur
    h_case = 600//hauteur
    sleep(1/(largeur*hauteur))
    canvas.create_oval(x*l_case, y*h_case, (x+1)*l_case, (y+1)*h_case, fill = color)
    canvas.update()

def gen_graph():
    """None->Graphe
        Renvoie le graphe correspondant au labyrinthe affiché"""
    L = []
    for i in range(hauteur*largeur):
        L.append(str(i))
    G = graphe(L)
    for i in range(largeur):
        for j in range(hauteur):
            if Tab[i][j]&0b0001 == 0:
                G.ajouter_arete(str(i+largeur*j), str(i+largeur*(j-1)), 1)
            if Tab[i][j]&0b0010 == 0:
                G.ajouter_arete(str(i+largeur*j), str(i+1+largeur*j), 1)
            if Tab[i][j]&0b0100 == 0:
                G.ajouter_arete(str(i+largeur*j), str(i+largeur*(j+1)), 1)
            if Tab[i][j]&0b1000 == 0:
                G.ajouter_arete(str(i+largeur*j), str(i-1+largeur*j), 1)
    #print(G)
    return G

def Trouve_chemin(T):
    """ Dict{String : [int, String]}->List[string]
        Renvoie le chemin à suivre pour atteindre la sortie fourni par l'algorithme de Djikstra"""
    sommet = str(largeur-1)
    L = pile()
    L.ajouter(sommet)
    chemin = []
    while sommet !="0":
        sommet = T[sommet][1]
        L.ajouter(sommet)
    while not (L.est_vide()):
        chemin.append(L.enlever())
    return chemin
    

def suis_chemin(chemin):
    """ List[string]->None
        Affiche le chemin suivi"""
    for s in chemin :
        case = int(s)
        x = case % largeur
        y = case // largeur
        bonhomme(x,y, "purple")


def resol_dijkstra():
    """Utilise l'algorithme de Djikstra pour trouver le plus cours chemin"""
    # les sommets sont nommés de 0 à longueur*largeur-1 du labyrinthe
    G = gen_graph()
    reponse_dijkstra = G.dijkstra("0")
    chemin = Trouve_chemin(reponse_dijkstra)
    suis_chemin(chemin)

def backtracker(x, y, cases):
    """ int*int*List[[String]]*List[[String]]
        Procédure récursive de création du labyrinthe par backtracker"""
    global Tab
    l_case = 800//largeur
    h_case = 600//hauteur
    cases[x][y] = "KO"
    while (x > 0 and cases[x-1][y] == "ok") or ((x < largeur -1) and cases[x+1][y] == "ok") or (y > 0 and cases[x][y-1] == "ok") or ((y < hauteur - 1) and cases[x][y+1] == "ok"):
        dir = randint(0, 3)
        if dir == 0 and y>0 and cases[x][y-1] == "ok":
            Tab[x][y] -= 0b0001
            Tab[x][y-1] -= 0b0100
            canvas.create_line((x*l_case, y*h_case),((x+1)*l_case,y*h_case), fill = "blue")
            canvas.update()
            backtracker(x, y-1, cases)
        elif dir == 1 and (x < largeur -1) and cases[x+1][y] == "ok":
            Tab[x][y] -= 0b0010
            Tab[x+1][y] -= 0b1000
            canvas.create_line(((x+1)*l_case, y*h_case),((x+1)*l_case,(y+1)*h_case), fill = "blue")
            canvas.update()
            backtracker(x+1, y, cases)
        elif dir == 2 and (y < hauteur - 1) and cases[x][y+1] == "ok":
            Tab[x][y] -= 0b0100
            Tab[x][y+1] -= 0b0001
            canvas.create_line((x*l_case, (y+1)*h_case),((x+1)*l_case,(y+1)*h_case), fill = "blue")
            canvas.update()
            backtracker(x, y+1, cases)
        elif dir == 3 and x > 0 and cases[x-1][y] == "ok":
            Tab[x][y] -= 0b1000
            Tab[x-1][y] -= 0b0010
            canvas.create_line((x*l_case, y*h_case),(x*l_case,(y+1)*h_case), fill = "blue")
            canvas.update()
            backtracker(x-1, y, cases)


def recursive():
    """ génération de labyrinthe par récusrsive bactracker"""
    global Tab, largeur, hauteur
    hauteur = nb_hauteur.get()
    largeur = nb_largeur.get()
    x = randint(0,largeur-1)
    y = randint(0,hauteur-1)
    cases = [["ok" for _ in range(hauteur)] for _ in range(largeur)]
    Tab = [[15 for _ in range(hauteur)] for _ in range(largeur)]
    trace_lab(Tab)
    backtracker(x,y,cases)
    print("fini")

def nb_zones(zones):
    cpt = 0
    liste = []
    for ligne in zones :
        for z in ligne :
            if z not in liste :
                cpt +=1
                liste.append(z)
    return cpt

def kruskal():
    """ génération de labyrinthe par kruskal"""
    global Tab, largeur, hauteur
    hauteur = nb_hauteur.get()
    largeur = nb_largeur.get()
    l_case = 800//largeur
    h_case = 600//hauteur
    zones = [[i+largeur*j for j in range(hauteur)] for i in range(largeur)]
    Tab = [[15 for _ in range(hauteur)] for _ in range(largeur)]
    trace_lab(Tab)
    #n = nb_zones(zones)
    n = largeur*hauteur
    while n > 1 :
        print(n)
        x = randint(0,largeur-1)
        y = randint(0,hauteur-1)
        dir = randint(0,3)
        if dir == 0 and y > 0 and zones[x][y] != zones[x][y-1] :
            Tab[x][y] -= 0b0001
            Tab[x][y-1] -= 0b0100
            canvas.create_line((x*l_case, y*h_case),((x+1)*l_case,y*h_case), fill = "blue")
            canvas.update()
            n -= 1
            old = zones[x][y-1]
            for i in range(largeur):
                for j in range(hauteur):
                    if zones[i][j] == old :
                        zones[i][j] = zones[x][y]
        elif dir == 1 and x < (largeur - 1) and zones[x][y] != zones[x+1][y] :
            Tab[x][y] -= 0b0010
            Tab[x+1][y] -= 0b1000
            canvas.create_line(((x+1)*l_case, y*h_case),((x+1)*l_case,(y+1)*h_case), fill = "blue")
            canvas.update()
            n -= 1
            old = zones[x+1][y]
            for i in range(largeur):
                for j in range(hauteur):
                    if zones[i][j] == old :
                        zones[i][j] = zones[x][y]
        elif dir == 2 and y < (hauteur - 1) and zones[x][y] != zones[x][y+1] :
            Tab[x][y] -= 0b0100
            Tab[x][y+1] -= 0b0001
            canvas.create_line((x*l_case, (y+1)*h_case),((x+1)*l_case,(y+1)*h_case), fill = "blue")
            canvas.update()
            n -= 1
            old = zones[x][y+1]
            for i in range(largeur):
                for j in range(hauteur):
                    if zones[i][j] == old :
                        zones[i][j] = zones[x][y]
        elif dir == 3 and x > 0 and zones[x][y] != zones[x-1][y] :
            Tab[x][y] -= 0b1000
            Tab[x-1][y] -= 0b0010
            canvas.create_line((x*l_case, y*h_case),(x*l_case,(y+1)*h_case), fill = "blue")
            canvas.update()
            n -= 1
            old = zones[x-1][y]
            for i in range(largeur):
                for j in range(hauteur):
                    if zones[i][j] == old :
                        zones[i][j] = zones[x][y]
        #n = nb_zones(zones)
    print("fini")

#######################
# Programme Principal #
####################### 

fenetre = Tk()
cadre = Frame(fenetre, width=800, height=700, borderwidth=1)
cadre.pack()
label_cadre = Label(cadre, text="Résolution de labyrinthe")
label_cadre.pack()
canvas = Canvas(cadre, background="blue", width=800, height=600)
canvas.pack()
cadre_btn = Frame(fenetre)
cadre_btn.pack()
nb_largeur = Scale(cadre_btn, orient="horizontal", from_=1, to_=100)
nb_largeur.grid(column=0, row=0)
nb_hauteur = Scale(cadre_btn, orient="horizontal", from_=1, to_=100)
nb_hauteur.grid(column=1, row=0)
btn_go = Button(cadre_btn, text="récursive", command=recursive)
btn_go.grid(column = 0, row = 1)
btn_go = Button(cadre_btn, text="kruskal", command=kruskal)
btn_go.grid(column = 1, row = 1)
btn_md = Button(cadre_btn, text="Main à droite", command=main_droite)
btn_md.grid(column = 0, row = 2)
btn_dj = Button(cadre_btn, text="Dijkstra", command=resol_dijkstra)
btn_dj.grid(column = 1, row = 2)
Tab = []
hauteur = nb_hauteur.get()
largeur = nb_largeur.get()

#fin du fichier
fenetre.mainloop()
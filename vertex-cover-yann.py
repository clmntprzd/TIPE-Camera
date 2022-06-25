#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:23:48 2022
metasploit
@author: clement
"""
import time
import numpy as np
from graph_tool.all import *
import graph_tool.generation
import graph_tool.topology
from random import choices
g = Graph(directed=False)
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
e = g.add_edge(v1, v2)
e2 = g.add_edge(v2, v3)
e3 = g.add_edge(v3, v4)
vlist=g.add_vertex(10)
C=[]

def deg_sample():
   n=np.random.poisson(3)
   if  n==0:
       return 1
   elif n>=5:
       return 5
   else: 
       return n
def num_graph(G):
    vprop = G.new_vertex_property("int")
    G.vp.num=vprop
    for v in G.iter_vertices():
        G.vp.num[v]=G.vertex_index[v]
    return G

def make_graph(N):
    G=graph_tool.generation.random_graph(N,deg_sample,directed=False)
    return G
def until_planar(N):
    G=make_graph(N)
    while not graph_tool.topology.is_planar(G):
        G=make_graph(N)
    return G
def vertex_cover(g):
    C=[]
    graph_tool.draw.graph_draw(g, vprops=g.vp.num)
    while len(g.get_edges())>0:
        V=choices(g.get_vertices(), k=2)
        C+=V
        graph_tool.draw.graph_draw(g,  vprops=g.vp.num)
        for v in reversed(sorted(V)):
            g.remove_vertex(g.vertex(v))
        V=[]
    return C      



graph_tool.draw.graph_draw(until_planar(20))





## Une partie vulga + Deux grandes parties de notre projet : MODÉLISATION PAR LES GRAPHES (d'une ville) et ANALYSE DU PROBLÈME ALGORITHMIQUEMENT


#VertexCover




#Coplanarité :
def ccw(A,B,C):
    return (C[1]-A[1])*(B[0]-A[0]) &gt; (B[1]-A[1])*(C[0]-A[0])

def intersect(A,B,C,D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


from random import shuffle

def List_of_Array(A):
    S = []
    for a in A : 
        S.append(a)
    return S


''' Contenu : Ici, le programme permet de tenter une solution brutale au problème suivant : disposant
de X caméras, quelle est la meilleure manière de placer ces caméras afin de couvrir le maximum
de sommets, considérées comme étant des intersections dans notre ville'''
''' Limites algorithmiques : pour un très grand nombre d'intersections (sommet), la solution aléatoire ne sera pas nécessairement
la meilleure solution (EXEMPLE : Pour 30 sommets et 4 caméras, on trouve rapidement la valeur optimale de recouvrement
qui est 46)'''
''' Limites de modélisation : un graphe aussi simple, ne comporte pas des paramètres intéressants
comme la densité de trafic etc.'''

def binomial(k,n):
    if n == 0 or k == 0 : 
        return 1 
    else :
        return n/k * binomial(k-1, n-1)

binomial(3,6)

def OptimisationAleatoire1(Nombre_Cameras, Graphe, T):
    print("Il y a ", Nombre_Cameras," parmi ", len(Graphe.get_vertices())," configurations de placements possibles, soit ", int(binomial(Nombre_Cameras, len(Graphe.get_vertices()))))
    Sommets = List_of_Array(Graphe.get_vertices())
    Placements = []
    for i in range(1,T+1):
        S = list(Sommets)
        shuffle(S)
        Cameras = S[0 : Nombre_Cameras-1]
        #print("Caméras choisies :", Cameras)
        Couverture = []
        for k in range(len(Cameras)):
            for w in List_of_Array(Graphe.get_out_neighbors(Cameras[k])):
                #print(w," est sommet couvert par le sommet", Cameras[k] )
                if w not in Couverture : 
                    Couverture.append(w)
        Placements.append((Cameras, len(Couverture)/len(Sommets)))
    return Placements 

def MO(L):
    S = []
    for k in range(len(L)):
        S.append(L[k][1])
    return max(S)

''' Le programme suivant propose d'attribuer à chaque sommet un "poids" qui sera totalement une boîte noire dans le sens où la gestion de données ne sera pas traitée
en profondeur ici.'''
''' Propriété du poids p : p_i est initialement pour chaque sommmet du graphe une boîte noire, dont la valeur est issue des divers paramètres qui importent dans la réalisation du placement.
Il sera conçu comme suit : il s'agit d'un score, plus haut est le score, plus intéressant il est de placer une caméra à cet endroit. La couverture en score /scoretotal remplaçera la notion de
couverture purement géographique. Dans le but de se libérer de toute modélisation, on se donnera p_i dans [0,1000]. On se donnera une distribution en sigmoïde '''

from numpy import exp
def sigmoide(x):
    return 1/(1+exp((1/1000)*x))

from random import randint
def AADPS(g):
    S = List_of_Array(g.get_vertices())
    IntersectionP = []
    for k in range(len(S)):
        IntersectionP.append((S[k],randint(0,1000)))
    return IntersectionP


#graphe_score = [(i-ème sommet, p_i, [ses voisins])]

def OptimisationAleatoire(Nombre_Cameras, graphe, T):
    def graphe_score(g):
        S = List_of_Array(g.get_vertices())
        for i in range(len(S)):
            ...
    Placements = []
    for i in range(1,T+1):
        S = [graphe_score[k][0]]
        shuffle(S)
        Cameras = S[0 : Nombre_Cameras-1]
        #print("Caméras choisies :", Cameras)
        Couverture = []
        for k in range(len(Cameras)):
            for w in List_of_Array(Graphe.get_out_neighbors(Cameras[k][0])):
                #print(w," est sommet couvert par le sommet", Cameras[k] )
                if w not in Couverture : 
                    Couverture.append(w)
        Placements.append((graphe_score[k][1]/sum(graphe_score)))
    return Placements 



''' Le programme suivant envisage une proposition d'addition de caméras optimale en plus de celles proposées précedemment. '''


''' Une autre idée de programme venant compléter le programme initial est de venir rajouter une condition pour savoir s'il existe une couverture par les sommets'''
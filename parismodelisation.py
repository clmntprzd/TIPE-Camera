#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 19:40:19 2022

@author: clement
"""

import matplotlib.pyplot as plt
from graph_tool.all import *
from tqdm import tqdm
g=load_graph("testparisflemme.gt")
import matplotlib.style as mplstyle
import json
mplstyle.use('fast')
def Montrer(G,LCam):
    fig=plt.figure()
    plt.rcParams['figure.facecolor'] = 'grey'
    
#    for v in G.iter_vertices():
#        plt.plot(G.vp.long[v],G.vp.lat[v],"bo")
    for e in tqdm(G.iter_edges()):
        (v1, v2)=e
        plt.plot([G.vp.long[v1],G.vp.long[v2]],[G.vp.lat[v1],G.vp.lat[v2]],"g-")
    for v in tqdm(LCam):
#        plt.plot(G.vp.long[G.vertex(v)],G.vp.lat[G.vertex(v)],"ro")
        for e in G.iter_all_edges(G.vertex(v)):
            (v1, v2)=e
            plt.plot([G.vp.long[v1],G.vp.long[v2]],[G.vp.lat[v1],G.vp.lat[v2]],"-",color='orange')
    plt.show()



c = open("camera.json", "r")
Cameras=json.loads(c.read())   
#Montrer(g,camera)
Couverture = []
L=g.get_total_degrees(g.get_vertices())
P=g.get_vertices()
Lsorted , Psorted =zip(*sorted(zip(L,P)))
#Cameras=Psorted[0:710]
S=0
for c in Cameras:
    if c in Psorted[0:710]:
        S+=1
for k in range(len(Cameras)):
        for w in g.get_out_neighbors(Cameras[k]):
            #print(w," est sommet couvert par le sommet", Cameras[k] )
            if w not in Couverture : 
                Couverture.append(w)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 17:20:18 2022

@author: clement
"""
from graph_tool.all import *
import json
from tqdm import tqdm
c = open("croisement2.json", "r")
Croisement=json.loads(c.read())


c = open("routes2.json", "r")
Routes=json.loads(c.read())


G=Graph(directed=False)
vprop = G.new_vertex_property("int")
G.vertex_properties["num"]=vprop
vlong= G.new_vertex_property("float")
G.vertex_properties["long"]=vlong
vlat= G.new_vertex_property("float")
G.vertex_properties["lat"]=vlat

def norm(A,B):
    (i,j)=(A[0],A[1]); (g,h)=(B[0],B[1])
    return ((i-g)**2+(j-h)**2)**0.5

def MeilleurChemin(Lind,Croisx):
    DeuxplusPr=[]
    if len(Lind)==2:
        return(Lind)
    for i in range(len(Lind)):
        L=[] ; P=[]
        for j in range(len(Lind)):
            if not i==j:
                L.append(norm(Croisx[Lind[i]],Croisx[Lind[j]]))
                P.append(Lind[j])
        Lsorted , Psorted =zip(*sorted(zip(L,P)))
        DeuxplusPr.append(Psorted[0:2])
    Chemins=[] ; CheminInd=[]
    
    for i in range(len(Lind)):
        
        vi=Lind[i]
        vj = DeuxplusPr[i][0]
        C=[vi,vj]
        S=norm(Croisx[vi],Croisx[vj])
        for j in range(len(Lind)):
            
            if DeuxplusPr[Lind.index(vj)][0]==vi:
 
                (vi , vj)=(vj, DeuxplusPr[Lind.index(vj)][1])
                
            else: 
                (vi , vj)=(vj, DeuxplusPr[Lind.index(vj)][0])
            C.append(vj)
            S+=norm(Croisx[vi],Croisx[vj])
        Chemins.append(S)
        CheminInd.append(C)
    Lsorted , Psorted =zip(*sorted(zip(Chemins,CheminInd)))
    return Psorted[0]

for i in range(0,len(Croisement["pos"])):
        v=G.add_vertex()
        G.vp.num[v]=i
        G.vp.long[v]=Croisement["pos"][i][0]
        G.vp.lat[v]=Croisement["pos"][i][1]
for route in tqdm(Routes):
    Crois=[]
    for i in range(len(Croisement["rues"])):
        if route in Croisement["rues"][i]:
            Crois.append(i)
    """
    Prend les croisements qui appartiennent à la même route, et les relie sur le graphe en prenant les plus proches
    
    """
    if len(Crois)==1 or len(Crois)==0 :
        continue
    Chemin=MeilleurChemin(Crois,Croisement["pos"])
    
    for i in range(len(Chemin)-1):
        j=i+1
        G.add_edge(G.vertex(Chemin[i]),G.vertex(Chemin[j])) 
    
G.save("testparis.gt")
    
    
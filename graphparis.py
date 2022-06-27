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

def Proche(A,B):
    dlon=A[0]-B[0]
    dlat= A[1]-B[1]
    dx=dlon*(111120)
    dy=dlat*(73339)
    l=dx**2 + dy**2
    return l<900**2

def norm(A,B):
    dlon=A[0]-B[0]
    dlat= A[1]-B[1]
    dx=dlon*(111120)
    dy=dlat*(73339)
    l=dx**2 + dy**2
    return (l)**0.5

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
        Vint=[vi]
        vj = DeuxplusPr[i][0]
        C=[vi,vj]
        S=norm(Croisx[vi],Croisx[vj])
        for j in range(len(Lind)-1):
            
            if DeuxplusPr[Lind.index(vj)][0] in Vint :
 
                (vi , vj)=(vj, DeuxplusPr[Lind.index(vj)][1])
                
            else: 
                (vi , vj)=(vj, DeuxplusPr[Lind.index(vj)][0])
            C.append(vj)
            Vint.append(vi)
            S+=norm(Croisx[vi],Croisx[vj])
        Chemins.append(S)
        CheminInd.append(C)
    Lsorted , Psorted =zip(*sorted(zip(Chemins,CheminInd)))
    return Psorted[0]
def MeilleurCheminFlemme(Lind,Croisx):
    DeuxplusPr=[] ; LArri=[]; LArrj=[]
    
    if len(Lind)==2:
        return(Lind)
    L=[]
    for i in range(len(Lind)):
        for j in range(len(Lind)):
            if not i==j:
                L.append(norm(Croisx[Lind[i]],Croisx[Lind[j]]))
    Lsorted=sorted(L, reverse=True)
    lim=Lsorted[2]
    for i in range(len(Lind)):
        L=[] ; P=[]
        for j in range(len(Lind)):
            if not i==j:
                L.append(norm(Croisx[Lind[i]],Croisx[Lind[j]]))
                P.append(Lind[j])
        Lsorted , Psorted =zip(*sorted(zip(L,P)))
        DeuxplusPr.append(Psorted[0:2])
    
    for vi in Lind:
        i=Lind.index(vi)
        for vj in DeuxplusPr[i]:
            if norm(Croisx[vi],Croisx[vj])<lim:
                    LArri.append(vi)
                    LArrj.append(vj)
    return LArri, LArrj
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
    Chemini , Cheminj=MeilleurCheminFlemme(Crois,Croisement["pos"])
    if isinstance(Chemini,int):
         G.add_edge(G.vertex(Chemini),G.vertex(Cheminj)) 
    else:
        for i in range(len(Chemini)):
            G.add_edge(G.vertex(Chemini[i]),G.vertex(Cheminj[i])) 

    
G.save("testparisflemme2.gt")
    
    
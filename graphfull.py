#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:13:09 2022

@author: clement
"""

import numpy as np
from graph_tool.all import *
import graph_tool.generation
import graph_tool.topology
from random import random, choice
import matplotlib.pyplot as plt
from random import choices


def Position(T):
    return ((random()-0.5)*T,(random()-0.5)*T)
    
def GenerationCroisement(n,T):
    C=[]
    for i in range(0,n):
        C.append(Position(T))
    return C

def num_graph(G):
    vprop = G.new_vertex_property("int")
    G.vertex_properties["num"]=vprop
    for v in G.iter_vertices():
        G.vp.num[v]=G.vertex_index[v]
    return G
def GraphAvecPosition(Lpos):
    G=Graph(directed=False)
    vprop = G.new_vertex_property("int")
    G.vertex_properties["num"]=vprop
    vlong= G.new_vertex_property("float")
    G.vertex_properties["long"]=vlong
    vlat= G.new_vertex_property("float")
    G.vertex_properties["lat"]=vlat
    for i in range(0,len(Lpos)):
        v=G.add_vertex()
        G.vp.num[v]=i
        G.vp.long[v]=Lpos[i][0]
        G.vp.lat[v]=Lpos[i][1]
    return G
def norm(A,B):
    (i,j)=A; (g,h)=B
    return np.sqrt((i-g)**2+(j-h)**2)
def ListeDistance(Lpos,i):
    L=[]; P=[j for j in range(len(Lpos))]
    for j in range(len(Lpos)):
        if not i==j:
            L.append(norm(Lpos[i],Lpos[j]))
    Lsorted , Psorted =zip(*sorted(zip(L,P)))
    return Psorted
def AppartientDroite(A,B,C):
    if A==B:
        return False
    if  not B[0]==A[0]:
        c=(C[0]-A[0])/(B[0]-A[0])
        if c>0 and c<1 :
            if B[1]==A[1]:
                return True
            return c==(C[1]-A[1])/(B[1]-A[1])
        return False
        
        
    else:
        c=(C[1]-A[1])/(B[1]-A[1])
        if c>0 and c<1 :
            return True

def Croisement(A,B,C,D):
    def ccw(A,B,C):
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
    def intersect(A,B,C,D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
    if AppartientDroite(A,B,C) or AppartientDroite(A,B,D):
        return True
    return intersect(A,B,C,D)
    
def Coupe(A,B,LAre):
    for Ar in LAre:
        if Croisement(A,B,Ar[0],Ar[1]):
            return True
    return False
    
def ConnectionGraph(Lpos):
    Num=5*[4]+8*[5]+6*[6]
    LAre=[] ; LAreInd=[]
    for vi in range(len(Lpos)):
        i=choice(Num)
        Candidats=ListeDistance(Lpos,i)
        for j in range(i+1):
            vj=Candidats[j]
            if (not [vi,vj] in LAreInd) and (not [vj,vi] in LAreInd):
                if not Coupe(Lpos[vi],Lpos[vj],LAre):
                    LAre.append([Lpos[vi],Lpos[vj]])
                    LAreInd.append([vi,vj])
    return LAreInd         
 
def FaireArr(G,LAreInd):
    for Arr in LAreInd:
        G.add_edge(G.vertex(Arr[0]),G.vertex(Arr[1]))        
    
def FaireGraph(N,T):
    C=GenerationCroisement(N,T)
    G=GraphAvecPosition(C)
    Arretes=ConnectionGraph(C)
    FaireArr(G,Arretes)
    return G

def FaireGraphMieux(N,T):
    C=GenerationCroisement(N,T)
    G=GraphAvecPosition(C)
    Arr=2*N
    while Arr>0:
        V=choices(G.get_vertices(), k=2)
        vs=G.vertex(V[0]); vt=G.vertex(V[1])
        if not vt in G.get_all_neighbors(vs):
            e = G.add_edge(vs, vt)
            if graph_tool.topology.is_planar(G):
                Arr-=1
            else:
                G.remove_edge(e)
        
    return G
def Montrer(G,LCam):
    fig=plt.figure()
    plt.rcParams['figure.facecolor'] = 'grey'
#    for v in G.iter_vertices():
#        plt.plot(G.vp.long[v],G.vp.lat[v],"bo")
    for e in G.iter_edges():
        (v1, v2)=e
        plt.plot([G.vp.long[v1],G.vp.long[v2]],[G.vp.lat[v1],G.vp.lat[v2]],"b-")
    for v in LCam:
#        plt.plot(G.vp.long[G.vertex(v)],G.vp.lat[G.vertex(v)],"ro")
        for e in G.iter_all_edges(G.vertex(v)):
            (v1, v2)=e
            plt.plot([G.vp.long[v1],G.vp.long[v2]],[G.vp.lat[v1],G.vp.lat[v2]],"r-")
    plt.show()
    
        
    
    
    
#
#long=[x[0] for x in C]
#lat=[x[1] for x in C]
#fig=plt.figure()
#plt.plot(long,lat, "s")
#plt.show()



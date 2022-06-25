#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:00:41 2022

Centre Paris:
Lat    1 min === 1.852 m
Lon    1 min ===  1.852* 0.66
Lat   1° ==== 111120m
LON   1° ==== 73339m
 Proche a partir de 10m

@author: clement
"""
from graph_tool.all import *
import csv

def Proche(A,B):
    dlon=A[0]-B[0]
    dlat= A[1]-B[1]
    dx=dlon*(111120)
    dy=dlat*(73339)
    l=dx**2 + dy**2
    return l<100
def C2P(C):
    return [float(C[2]),float(C[3])]


G=Graph(directed=False)
vprop = G.new_vertex_property("int")
G.vertex_properties["num"]=vprop
vlong= G.new_vertex_property("float")
G.vertex_properties["long"]=vlong
vlat= G.new_vertex_property("float")
G.vertex_properties["lat"]=vlat

Croisement=[] 
with open('data/croisements_rues_paris.csv', newline='') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        Croisement.append(row)
s=0
CroisementDisctinct=



            
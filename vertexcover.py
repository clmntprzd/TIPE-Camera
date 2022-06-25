#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:23:48 2022

@author: clement
"""
from tqdm import tqdm
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
    G.vertex_properties["num"]=vprop
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
    graph_tool.draw.graph_draw(g, vertex_text=g.vp.num)
    while len(g.get_edges())>0:
        V=choices(g.get_vertices(), k=2)
        
        graph_tool.draw.graph_draw(g ,vertex_text=g.vp.num)
        for v in V:
            #print(g.vp.num[g.vertex(v)])
            C.append(g.vp.num[g.vertex(v)])
            g.remove_vertex(g.vertex(v))
            
        V=[]
    graph_tool.draw.graph_draw(g ,vertex_text=g.vp.num)
    return C      




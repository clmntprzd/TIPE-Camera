#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:40:59 2022

@author: clement
"""
from graph_tool.all import *
def norm(A,B):
    dlon=A[0]-B[0]
    dlat= A[1]-B[1]
    dx=dlon*(111120)
    dy=dlat*(73339)
    l=dx**2 + dy**2
    return (l)**0.5

g=load_graph("testparisflemme.gt")

centre=[2.341648,48.848912]
    
for v in reversed(sorted(g.get_vertices())):
    
    if norm(centre,[g.vp.long[v], g.vp.lat[v]])>1500:
        
        g.remove_vertex(v)

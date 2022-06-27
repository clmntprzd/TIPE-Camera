#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:57:23 2022

@author: clement
"""
import csv
import json
from graph_tool.all import *
g=load_graph("testparisflemme.gt")
Camera=[]
def Proche(A,B):
    dlon=A[0]-B[0]
    dlat= A[1]-B[1]
    dx=dlon*(111120)
    dy=dlat*(73339)
    l=dx**2 + dy**2
    return l<100
with open('data/camera.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
    next(reader)
    for row in reader:
        coord=[float(row[5]),float(row[6])]
        for v in g.get_vertices():
            if Proche(coord,[g.vp.long[v],g.vp.lat[v]]):
                Camera.append(g.vp.num[v])

                
f = open("camera.json", "w")
f.write(json.dumps(Camera))
f.close()
print("Camera Saved")
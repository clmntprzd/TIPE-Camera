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
from tqdm import tqdm

import csv
import json
def Proche(A,B):
    dlon=A[0]-B[0]
    dlat= A[1]-B[1]
    dx=dlon*(111120)
    dy=dlat*(73339)
    l=dx**2 + dy**2
    return l<100
def C2P(C):
    return [float(C[2]),float(C[3])]



Routes=[]
Croisement={"pos":[], "rues":[]} 
with open('data/croisements_rues_paris.csv', newline='') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    next(reader)
    for row in tqdm(reader):
        if len(Croisement)==0:
            Croisement["pos"].append(C2P(row))
            Croisement["rues"].append([row[0], row[1]])
        else :
            crois=0 ; Doublon=False
            for i in range(len(Croisement["pos"])):
                if Proche(Croisement["pos"][i],C2P(row)):
                    crois=i ; Doublon=True
                    break
            if Doublon:
                if row[0] not in Croisement["rues"][i]:
                    Croisement["rues"][i].append(row[0])
                if row[1] not in Croisement["rues"][i]:
                    Croisement["rues"][i].append(row[1])
            else:
                Croisement["pos"].append(C2P(row))
                Croisement["rues"].append([row[0], row[1]])
        for i in range(2):
            if row[i] not in Routes:
                Routes.append(row[i])

f = open("routes2.json", "w")
f.write(json.dumps(Routes))
f.close()
print("Routes Saved")
f = open("croisement2.json", "w")
f.write(json.dumps(Croisement))
f.close()
print("Croisement Saved")
                    
        




            
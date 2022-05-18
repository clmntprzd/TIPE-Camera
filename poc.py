from graph_tool.all import *
from random import choice
g = Graph(directed=False)
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
e = g.add_edge(v1, v2)
e2 = g.add_edge(v2, v3)
e3 = g.add_edge(v3, v4)
vlist=g.add_vertex(10)

def listvertex(gr):
    l=[]
    for v in gr.vertices():
        l.append(v)
    return l
l=listvertex(g)
for v in  g.vertices():
    v2=choice(l)
    if v!=v2:
        g.add_edge(v,v2)

#### Connexité




def genlist(gen):
    L=[]
    for i in gen:
        L.append(i)
    return L
def connexite:
    
from graph_tool.all import *
g = load_graph("test.gt")

def viewg(G):
    graph_draw(G, vertex_text=G.vertex_index)

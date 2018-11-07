import snap
from AnaheimRead import load_from_binary_stram
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def visualize(graph_name,weight_type="Congestion"):
    G = load_from_binary_stram(graph_name + ".graph")
    GN = nx.Graph()
    
    for edge in G.Edges():
        fro = edge.GetSrcNId()
        to = edge.GetDstNId()
        wei = G.GetFltAttrDatE(edge.GetId(), weight_type)
        
        if not GN.has_node(fro):
            GN.add_node(fro)
        if not GN.has_node(to):
            GN.add_node(to)
        
        if not GN.has_edge(fro,to):
            GN.add_edge(fro,to,weight = wei)
    
    edges,weights = zip(*nx.get_edge_attributes(GN,'weight').items())
    
    weights = map(lambda x: -0.2 if x==0 else x, weights) #TODO, damo edge v buckete
    
    pos = nx.spring_layout(GN)
    nx.draw(GN,pos,node_size = 10,edgelist=edges,edge_color = weights,edge_cmap=plt.cm.Blues)

if __name__ == '__main__':
    visualize("ChicagoSketch")
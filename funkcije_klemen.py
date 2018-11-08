import snap
from AnaheimRead import load_from_binary_stram
import networkx as nx

def pagerank_list_po_id(graph_name):
    G = load_from_binary_stram(graph_name + ".graph")
    PRankH = snap.TIntFltH()
    snap.GetPageRank(G, PRankH)

    out = []

    for i in PRankH:
        out.append(PRankH[i])
    return out

def pagerank_list_po_id_nx(graph_name):
    G = load_from_binary_stram(graph_name + ".graph")
    
    GN = nx.Graph()

    for edge in G.Edges():
        fro = edge.GetSrcNId()
        to = edge.GetDstNId()

        if not GN.has_node(fro):
            GN.add_node(fro)
        if not GN.has_node(to):
            GN.add_node(to)

        if not GN.has_edge(fro,to):
            GN.add_edge(fro,to)
    
    pageR = nx.pagerank(GN)
    
    out = []
    for node in GN:
         out.append(pageR[node])
    return out

def degree_list_po_id(graph_name):
     G = load_from_binary_stram(graph_name + ".graph")
     GN = nx.Graph()

     for edge in G.Edges():
        fro = edge.GetSrcNId()
        to = edge.GetDstNId()

        if not GN.has_node(fro):
            GN.add_node(fro)
        if not GN.has_node(to):
            GN.add_node(to)

        if not GN.has_edge(fro,to):
            GN.add_edge(fro,to)
     
     out = []
     for node in GN:
         out.append(nx.degree(GN,node))

     return out



if __name__ == '__main__':
    pagerank_list_po_id_nx("Anaheim")
    #degree_list_po_id("Anaheim")
import snap
from AnaheimRead import load_from_binary_stram

def pagerank_list_po_id(graph_name):
    G = load_from_binary_stram(graph_name + ".graph")
    PRankH = snap.TIntFltH()
    snap.GetPageRank(G, PRankH)
    
    out = []
    
    for i in PRankH:
        out.append(PRankH[i])
    return out
        
if __name__ == '__main__':
    pagerank_list_po_id("Anaheim")
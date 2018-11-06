from __future__ import division
#to have normal division where 1/3 = 0.333333 and not 0

import AnaheimRead as AR
import matplotlib.pyplot as plt
import snap
import pandas as pd


def generateGraphs(G, la):
##    print 'haha'
    graphs=[]
    for l in la:
##        print 'lambda ', l;
        G1=snap.TNEANet.New()
        
        for edge in G.Edges():
            
            cap=G.GetFltAttrDatE(edge.GetId(), "Congestion")
            Nout=edge.GetSrcNId()
            Nin=edge.GetDstNId()
            if cap<l:
                if not G1.IsNode(Nout):
                    G1.AddNode(Nout)
                if not G1.IsNode(Nin):
                    G1.AddNode(Nin)
##                print cap;   
                G1.AddEdge(Nout, Nin, -1)
        graphs.append(G1);

    return graphs


dataframe=AR.read()
G = AR.to_graph(dataframe)
##print G.GetEdges();
la=[0.1,0.2,0.3,0.4,0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
graphs=generateGraphs(G, la)
#number of edges in each graph
edges=[]
for g in graphs:
    edges.append(g.GetEdges())
plt.plot(la, edges)
plt.xlabel('lambda')
plt.ylabel('number of edges')
plt.show()

#number of conected components in each graph
sizeOfCom=[];
for g in graphs:
    com= snap.TCnComV()
    snap.GetWccs(g, com)
    sizeOfCom.append(len(com))
plt.plot(la, sizeOfCom)
plt.xlabel('lambda')
plt.ylabel('number of components')
plt.show()


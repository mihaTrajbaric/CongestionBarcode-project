from __future__ import division
#to have normal division where 1/3 = 0.333333 and not 0

import AnaheimRead as AR
import ChicagoRead as CR
import matplotlib.pyplot as plt
import snap
import pandas as pd

#generates graphs for each lambda
def generateGraphs(G, la):
##    print 'haha'
    graphs=[]
    for l in la:
##        print 'lambda ', l;
        G1=snap.TNEANet.New()
        G1.AddFltAttrN("Flow")
        G1.AddFltAttrN("Capacity")
        G1.AddFltAttrN("Congestion")
        
        for edge in G.Edges():
            
            cap=G.GetFltAttrDatE(edge.GetId(), "Congestion")
            flow=G.GetFltAttrDatE(edge.GetId(), "Flow")
            capacity=G.GetFltAttrDatE(edge.GetId(), "Capacity")
            Nout=edge.GetSrcNId()
            Nin=edge.GetDstNId()
            if cap<l:
                if not G1.IsNode(Nout):
                    G1.AddNode(Nout)
                if not G1.IsNode(Nin):
                    G1.AddNode(Nin)
##                print cap;   
                edge_temp_id=G1.AddEdge(Nout, Nin, -1)
                G1.AddFltAttrDatE(edge_temp_id, cap, "Congestion")
                G1.AddFltAttrDatE(edge_temp_id, flow, "Flow")
                G1.AddFltAttrDatE(edge_temp_id, capacity, "Capacity")
                
        graphs.append(G1);

    return graphs


#gnerates list of --sets of nodes for each component in graph-- for each lambda
def getComponents(graphs):
    sets=[]
    for g in graphs:
        components=[]
        Com = snap.TCnComV()
        snap.GetWccs(g, Com)
        for CC in Com:
            mn=set()
            for n in CC:
                mn.add(n)
            components.append(mn.copy())
        sets.append(list(components))
    return sets


#generates two lists
#t is the starting point when each component starts,
#k is the ending point
def generateBarCode(sets):
    t=[]
    ta=[]
    k=[]
    for i in range(len(sets)-1):

        for a in sets[i]:
            exist=False
            b=[False]*len(ta)
            
            for j in range(len(ta)):
                s=ta[j]

                if s.issubset(a):
                    b[j]=True
                    exist=True
                    
            if not exist:
                t.append(i+1)
                ta.append(a)
                k.append(len(sets)+1)

            else:
                Tmin=i
                Imin=0
                for j in range(len(b)):
                    if b[j] :
                        k[j]=i
                        ta[j]={'none'}
                        if t[j]<Tmin:
                            Tmin=t[j]
                k[Imin]=len(sets)
                ta[j]=a
                               
    return [t,k]


#plots the bercode and returns two sets,
#ww1-starting lamdba(coresponding to t fromgenerateBarCode(sets))
#ww2-ending lambda(coresponding to k fromgenerateBarCode(sets))
def plotBarcode(w):
    z=[i+1 for i in range(len(w[0]))]
    ww1=[0]*len(w[0])
    ww2=[0]*len(w[0])

    for i in range(len(w[0])):
        ww1[i]=la[w[0][i]-1]
        ww2[i]=la[w[1][i]-1]

    for i in range(len(w[0])):
        plt.plot([ww1[i], ww2[i]], [i,i], 'b')
        plt.plot([ww1[i], ww2[i]], [i,i], 'b.', markersize=1)
    plt.xlabel('lambda')
    plt.ylabel('component index')
    plt.title('BARCODE')
    plt.show()
    return [ww1,ww2]

#probability of conectednes between two nodes from G in components
def probabilityOfConection(G, components):
    Rnd = snap.TRnd()
    Rnd.Randomize()
    numOfCon=0
    for i in range(100000):
        a=G.GetRndNId(Rnd)
        b=G.GetRndNId(Rnd)
        while a==b:
            a=G.GetRndNId(Rnd)
            b=G.GetRndNId(Rnd)
        conected=False
        for s in components:
            if (a in s) and (b in s):
                conected=True
                break
        if conected:
            numOfCon+=1
    return numOfCon/100000

#computing the probability for all lambda and ploting it
def plotProbability(G, sets, la):
    prob=[]
    for s in sets:
        prob.append(probabilityOfConection(G, s))
    plt.plot(la, prob)
    plt.xlabel('lambda')
    plt.ylabel('probability of conection')
    plt.show()

#############
#START!!!!!!#
#############



dataframe=AR.read()
G = AR.to_graph(dataframe)

##G=CR.read()


la=[0.1,0.2,0.3,0.4,0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]

#listof subgraphs for each lambda
graphs=generateGraphs(G, la)

##
#Computing Barcode
##


sets=getComponents(graphs)
w= generateBarCode(sets)


#plot number of edges in each graph
if __name__ == '__main__':
    edges=[]
    for g in graphs:
        edges.append(g.GetEdges())
    plt.plot(la, edges)
    plt.xlabel('lambda')
    plt.ylabel('number of edges')
    plt.show()

    #plot number of conected components in each graph
    sizeOfCom=[]
    for g in graphs:
        com= snap.TCnComV()
        snap.GetWccs(g, com)
        sizeOfCom.append(len(com))
    plt.plot(la, sizeOfCom)
    plt.xlabel('lambda')
    plt.ylabel('number of components')
    plt.show()

    #plot the size of the largest conected components in each graph
    larConComp=[]
    for g in graphs:
        larConComp.append((snap.GetMxScc(g)).GetNodes())
    plt.plot(la, larConComp)
    plt.xlabel('lambda')
    plt.ylabel('largest conected component')
    plt.show()



    
    #ploting the barcode
    ww=plotBarcode(w)


    #ploting the probability of conectednes
    plotProbability(G, sets, la)


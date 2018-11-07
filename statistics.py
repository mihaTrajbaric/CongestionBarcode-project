from __future__ import division
import AnaheimRead as AR
import matplotlib.pyplot as plt
import snap
import ChicagoRead as CR
from barcode import generateGraphs,generateBarCode,getComponents


def getDataPointsToPlot(Graph):
    """
    :param - Graph: snap.PUNGraph object representing an undirected graph

    return values:
    X: list of degrees
    Y: list of frequencies: Y[i] = fraction of nodes with degree X[i]
    """

    X, Y = [], []
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(Graph, DegToCntV)
    for p in DegToCntV:
        X.append(p.GetVal1())
        Y.append(p.GetVal2())
    return X, Y


def plot_degree_distribution(Graph,name=""):
    """
    Code for HW1 Q1.1
    """
    x, y = getDataPointsToPlot(Graph)
    plt.loglog(x, y)

    plt.xlabel('Node Degree (log)')
    plt.ylabel('Proportion of Nodes with a Given Degree (log)')
    plt.title('Degree Distribution of {}'.format(name))
    plt.legend()
    plt.show()

def read(name,la):
    if name == "Anaheim":
        G = AR.network()
    elif name == "Chicago":
        G = CR.read()
    else:
        raise IOError
    graphs = generateGraphs(G, la)
    sets = getComponents(graphs)
    w = generateBarCode(sets)
    return graphs,sets,w

def lamda_degree_distribution(graphs, la):
    for i in range (len(graphs)):
        plot_degree_distribution(graphs[i],"lambda = {}".format(la[i]))


if __name__ == '__main__':

    la = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
    graphs_ana, sets_ana, barcode_ana = read("Anaheim", la)
    lamda_degree_distribution(graphs_ana, la)


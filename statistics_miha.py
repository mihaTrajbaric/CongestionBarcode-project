from __future__ import division
import AnaheimRead as AR
import matplotlib.pyplot as plt
import snap
import ChicagoRead as CR
from barcode import generateGraphs, generateBarCode, getComponents


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


def plot_degree_distribution(Graph, name="", save_fig=False):
    """
    Code for HW1 Q1.1
    """
    x, y = getDataPointsToPlot(Graph)
    plt.loglog(x, y)

    plt.xlabel('Node Degree (log)')
    plt.ylabel('Proportion of Nodes with a Given Degree (log)')
    plt.title('Degree Distribution of {}'.format(name))
    plt.legend()

    if save_fig:
        plt.savefig("{}.png".format(name))
    plt.show()


def read(name, la):
    if name == "Anaheim":
        G = AR.network()
    elif name == "Chicago":
        G = CR.read()
    else:
        raise IOError
    graphs = generateGraphs(G, la)
    sets = getComponents(graphs)
    w = generateBarCode(sets)
    return graphs, sets, w


def lamda_degree_distribution(graphs, la, name="", save_fig=False):
    for i in range(len(graphs)):
        plot_degree_distribution(graphs[i], "{} (lambda {})".format(name, la[i]), save_fig=save_fig)
def k_clust_coef(G,node_id, k=5):
    """
    computes k clustering coef of node
    """

    nbr_set = set([node_id])
    for _ in range(k):
        nbr_set_new = set()
        for node_temp_id in nbr_set:
            nodeTemp = G.GetNI(node_temp_id)
            nodeTempDeg = nodeTemp.GetDeg()
            for i in range(nodeTempDeg):
                nbr_set_new.add(nodeTemp.GetNbrNId(i))
        nbr_set = nbr_set | nbr_set_new
    nbr_list = list(nbr_set)
    V = snap.TIntV()
    for i in nbr_list:
        V.Add(i)
    nbr_subgraph = snap.ConvertSubGraph(snap.PNEANet, G, V)
    nbr_subgraph.DelNode(node_id)
    n_edges = nbr_subgraph.GetEdges()


    n_nodes = nbr_subgraph.GetNodes()
    if n_nodes == 0:
        return 0

    coef = n_edges / (n_nodes * (n_nodes-1))
    return coef

def get_k_clust_coef(G,k=5):
    """
    computes cluster coef of all nodes in G
    funkcija za kobala

    """
    clustering_coefs = []
    for node in G.Nodes():
        clustering_coefs.append(k_clust_coef(G, node.GetId(), k))
    return clustering_coefs


if __name__ == '__main__':

    la = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
    graphs_ana, sets_ana, barcode_ana = read("Anaheim", la)
    graphs_chi, sets_chi, barcode_chi = read("Chicago", la)
    lamda_degree_distribution(graphs_ana, la, "Anaheim", save_fig=False)
    lamda_degree_distribution(graphs_chi, la, "Chicago", save_fig=False)

    k_clust_a = get_k_clust_coef(AR.network(), k=5)
    plt.hist(k_clust_a)
    plt.show()


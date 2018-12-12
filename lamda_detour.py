from __future__ import division
import AnaheimRead as AR
import matplotlib.pyplot as plt
import snap
import ChicagoRead as CR
from barcode import generateGraphs, getComponents
from shortest_path import find_shortest_path
import numpy as np


def read(name, la, lambda_subgraphs=True):
    if name == "Anaheim":
        G = AR.network()
    elif name == "Chicago":
        G = CR.read()
    else:
        raise IOError
    if lambda_subgraphs:
        graphs = generateGraphs(G, la)
        sets = getComponents(graphs)
        return G, graphs, sets
    return G


def make_detour(Graph, lambda_list, lambda_subgraphs, src_node_ID, dst_node_ID):
    """
    finds shortest detour on as low as possible lambda-subgraph
    :param Graph:
    :param lambda_list: list of lambdas
    :param lambda_subgraphs: list of subgraphs for each lamdba in lambda list
    :param src_node_ID, dst_node_ID: IDs of edge's endpoints of edge to be removed and its trafic detoured
    :return list of nodeIDs of detour
    """
    assert len(lambda_list) == len(lambda_subgraphs)
    try:
        edge = Graph.GetEI(src_node_ID, dst_node_ID)

    except:
        print("edge {}->{} does not exist".format(src_node_ID, dst_node_ID))
        return
    edge_id = edge.GetId()
    flow = Graph.GetFltAttrDatE(edge_id, "Flow")
    capacity = Graph.GetFltAttrDatE(edge_id, "Capacity")
    congestion = Graph.GetFltAttrDatE(edge_id, "Congestion")

    # delete the edge
    Graph.DelEdge(src_node_ID, dst_node_ID)
    # delete the edge from all subsets
    for subgraph in lambda_subgraphs:
        try:
            subgraph.DelEdge(src_node_ID, dst_node_ID)
        except RuntimeError:
            pass

    def return_edge():
        # return the edge to where it belongs
        min_lambda = next(x for x in lambda_list if x > congestion)
        index = lambda_list.index(min_lambda)
        for subgraph in lambda_subgraphs[index:]:
            # creates edge, then assign back the attributes
            id = subgraph.AddEdge(src_node_ID, dst_node_ID)
            subgraph.AddFltAttrDatE(id, flow, "Flow")
            subgraph.AddFltAttrDatE(id, capacity, "Capacity")
            subgraph.AddFltAttrDatE(id, congestion, "Congestion")

        # and to main graph
        id = Graph.AddEdge(src_node_ID, dst_node_ID)
        Graph.AddFltAttrDatE(id, flow, "Flow")
        Graph.AddFltAttrDatE(id, capacity, "Capacity")
        Graph.AddFltAttrDatE(id, congestion, "Congestion")

    for i, lambda_ in enumerate(lambda_list):
        subgraph = lambda_subgraphs[i]
        try:
            path_length, path = find_shortest_path(subgraph, src_node_ID, [dst_node_ID], weight_type="Congestion")
        except TypeError:
            # print "no path for lambda",lambda_
            continue
        if path_length != float("inf"):
            return_edge()
            return lambda_, path
        # else:
        #    print lambda_,path_length
    return_edge()
    return -1, []


def test_detouring(lambda_list, graph_name="Anaheim", n_of_tests=100):
    G, graphs, _ = read(graph_name, lambda_list)
    distrib = []
    for i in range(n_of_tests):
        # pick random edge
        edge_id = G.GetRndEId()
        edge = G.GetEI(edge_id)
        src_id = edge.GetSrcNId()
        dst_id = edge.GetDstNId()
        lambda_, path_length = make_detour(G, lambda_list, graphs, src_id, dst_id)
        distrib.append(lambda_)
    plt.hist(distrib, bins='auto')
    plt.title("lambda detour for {}".format(graph_name))
    plt.xlabel("lambda")
    plt.ylabel("n of random events")
    plt.savefig("results_{}.png".format(graph_name))
    plt.show()


def test():
    G = snap.TNEANet().New()
    G.AddFltAttrN("Flow")
    G.AddFltAttrN("Capacity")
    G.AddFltAttrN("Congestion")
    for i in range(10):
        G.AddNode(i)
    for i in range(9):
        id = G.AddEdge(i, i + 1)
        G.AddFltAttrDatE(id, 0, "Flow")
        G.AddFltAttrDatE(id, 0, "Capacity")
        G.AddFltAttrDatE(id, float(i), "Congestion")
        id = G.AddEdge(i + 1, i)
        G.AddFltAttrDatE(id, 0, "Flow")
        G.AddFltAttrDatE(id, 0, "Capacity")
        G.AddFltAttrDatE(id, float(i), "Congestion")
    id = G.AddEdge(0, 9)
    G.AddFltAttrDatE(id, 0, "Flow")
    G.AddFltAttrDatE(id, 0, "Capacity")
    G.AddFltAttrDatE(id, 1, "Congestion")
    id = G.AddEdge(9, 0)
    G.AddFltAttrDatE(id, 0, "Flow")
    G.AddFltAttrDatE(id, 0, "Capacity")
    G.AddFltAttrDatE(id, 1, "Congestion")
    # G.Dump()
    la = [x for x in range(10)]
    graphs = generateGraphs(G, la)
    sets = getComponents(graphs)
    for i, lambda_ in enumerate(la):
        print lambda_, sets[i]
    lambda_, path = make_detour(G, la, graphs, 5, 6)
    print "answer:", lambda_, path


def run(network_name="Anaheim"):
    congestion = max_congestion(network_name)

    la = np.arange(0.1, round(congestion, 1) + 0.2, 0.1).tolist()
    test_detouring(la, n_of_tests=1000, graph_name=network_name)


def max_congestion(network="Anaheim"):
    la = []
    G = read(network, la, lambda_subgraphs=False)
    max_congest = max([G.GetFltAttrDatE(edge, "Congestion") for edge in G.Edges()])
    return max_congest


if __name__ == '__main__':
    run(network_name="Chicago")
    run(network_name="Anaheim")

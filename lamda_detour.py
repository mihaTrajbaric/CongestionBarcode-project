from __future__ import division
import AnaheimRead as AR
import matplotlib.pyplot as plt
import snap
import ChicagoRead as CR
from barcode import generateGraphs, getComponents
from shortest_path import find_shortest_path
import numpy as np
import time


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
        try:
            min_lambda = next(x for x in lambda_list if x > congestion)
        except StopIteration:
            if len(lambda_list) == 1:
                # that is the case with specific lambda
                min_lambda = lambda_list[0]
            else:
                raise StopIteration
        index = lambda_list.index(min_lambda)
        for subgraph in lambda_subgraphs[index:]:
            # creates edge, then assign back the attributes
            try:
                id = subgraph.AddEdge(src_node_ID, dst_node_ID)
                subgraph.AddFltAttrDatE(id, flow, "Flow")
                subgraph.AddFltAttrDatE(id, capacity, "Capacity")
                subgraph.AddFltAttrDatE(id, congestion, "Congestion")
            except:
                pass

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
            return lambda_, path_length
        # else:
        #    print lambda_,path_length
    return_edge()
    return -1, 0
def detour_without_lambda(Graph, src_node_ID, dst_node_ID):
    """
    makes a detour just with path_finding algorithm, without lambda optimization
    :param Graph: snap.TNEANet graph
    :param src_node_ID: source node
    :param dst_node_ID: source node
    :return: path length
    """
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

    def return_edge():

        # and to main graph
        id = Graph.AddEdge(src_node_ID, dst_node_ID)
        Graph.AddFltAttrDatE(id, flow, "Flow")
        Graph.AddFltAttrDatE(id, capacity, "Capacity")
        Graph.AddFltAttrDatE(id, congestion, "Congestion")

    path_length, path = find_shortest_path(Graph, src_node_ID, [dst_node_ID], weight_type="Congestion")
    if path_length != float("inf"):
        return_edge()
        return path_length

    return_edge()
    return 0

def subgraph_statistics(graph_name="Anaheim"):
    congestion = max_congestion(graph_name)
    lambda_list = np.arange(0.1, round(congestion, 1) + 0.2, 0.1).tolist()
    G, graphs, _ = read(graph_name, lambda_list)
    assert len(graphs) == len(lambda_list)
    snap.PrintInfo(G, graph_name, "info-{}.txt".format(graph_name), False)
    EdgeV = snap.TIntPrV()
    snap.GetEdgeBridges(G, EdgeV)
    print len(EdgeV)
    for i in range(len(graphs)):
        snap.PrintInfo(graphs[i], "{} subgraph {}".format(graph_name, i), "info-{}{}.txt".format(graph_name, i), False)



def test_detouring(lambda_list, graph_name="Anaheim", n_of_tests=100,specific_lambda = 1.0):
    G, graphs, _ = read(graph_name, lambda_list)
    assert len(graphs) == len(lambda_list)
    # print lambda_list
    distrib = []
    no_path = 0
    path_length_without_lambda = 0.0
    path_length_with_lambda = 0.0
    path_length_specific_lambda = 0.0
    total_time_without_lambda = 0.0
    total_time_with_lambda = 0.0
    total_time_specific_lambda = 0.0
    path_list = []

    specifi_lambda_idx = lambda_list.index(specific_lambda)
    specific_subgraph = graphs[specifi_lambda_idx]

    for i in range(n_of_tests):
        # pick random edge
        edge_id = G.GetRndEId()
        edge = G.GetEI(edge_id)
        src_id = edge.GetSrcNId()
        dst_id = edge.GetDstNId()

        # src_id = 896
        # dst_id = 899
        start = time.time()
        _, path_l_temp_specific = make_detour(G, [specific_lambda], [specific_subgraph], src_id, dst_id)
        temp_time_specific_lambda = time.time() - start

        start = time.time()
        lambda_, path_length = make_detour(G, lambda_list, graphs, src_id, dst_id)
        temp_time_lambda = time.time() - start

        start = time.time()
        path_length_no_lambda_temp = detour_without_lambda(G, src_id, dst_id)
        temp_time_no_lambda = time.time() - start

        if path_length_no_lambda_temp != float("inf"):
            path_length_without_lambda += path_length_no_lambda_temp

        if path_l_temp_specific != float("inf"):
            path_length_specific_lambda += path_l_temp_specific

        total_time_without_lambda += temp_time_no_lambda
        total_time_with_lambda += temp_time_lambda
        total_time_specific_lambda += temp_time_specific_lambda

        if lambda_ == -1 | (float(path_length) == float("inf")) | (float(path_length) == -float("inf")):
            no_path += 1

        else:
            path_list.append(path_length)
            path_length_with_lambda += path_length
            distrib.append(lambda_)
    # path_length_with_lambda /= (n_of_tests - no_path)
    # print distrib
    # print "path list",path_list
    less_than_1 = sum([1 for x in distrib if x <= 1.0])/len(distrib)
    print "ration of smaller or equal 1: {}".format(less_than_1)
    plt.hist(distrib, bins=len(lambda_list))
    plt.title("Lambda detour for {} network".format(graph_name))
    plt.xlabel("lambda")
    plt.ylabel("# of detours")
    plt.savefig("results_{}.svg".format(graph_name))
    plt.show()
    print "Graph {}, no detour {}".format(graph_name, no_path)
    print "base         path {} time {}".format(path_length_without_lambda,total_time_without_lambda)
    print "all lambdas  path {} time {}".format(path_length_with_lambda,total_time_with_lambda)
    # print "lambda={}    path {} time {}".format(specific_lambda,path_length_specific_lambda,total_time_specific_lambda)
    print "ratio path: all_lambdas vs. base {}".format(path_length_with_lambda/path_length_without_lambda)
    # print "ratio path: lambda = {} vs. base {}".format(specific_lambda,path_length_specific_lambda/path_length_without_lambda)
    print "ratio time: all_lambdas vs. base {}".format(total_time_with_lambda/total_time_without_lambda)
    # print "ratio time: lambda = {} vs. base {}".format(specific_lambda,total_time_specific_lambda/total_time_without_lambda)
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

    la = [round(x, 1) for x in np.arange(0.1, round(congestion, 1) + 0.2, 0.1).tolist()]
    test_detouring(la, n_of_tests=1000, graph_name=network_name)


def max_congestion(network="Anaheim"):
    la = []
    G = read(network, la, lambda_subgraphs=False)
    max_congest = max([G.GetFltAttrDatE(edge, "Congestion") for edge in G.Edges()])
    return max_congest

def test2():
    congestion = max_congestion("Anaheim")

    la = [round(x,1) for x in np.arange(0.1, round(congestion, 1) + 0.2, 0.1).tolist()]
    print la

if __name__ == '__main__':

    # subgraph_statistics("Chicago")
    # subgraph_statistics("Anaheim")
    run(network_name="Chicago")
    run(network_name="Anaheim")
    # test2()

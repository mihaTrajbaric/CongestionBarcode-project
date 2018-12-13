import snap


def find_shortest_path(graph, start_node_id, end_nodes_ids, weight_type="Congestion"):
    """
    finds path with lowest sum

    """
    if not graph.IsNode(start_node_id):
        # print "start node is not in graph, node id:", start_node_id
        return float("inf"), []
    for end_node_id in end_nodes_ids:
        if not graph.IsNode(end_node_id):
            #print "end node is not in graph, node id:", end_node_id
            return float("inf"), []

    # nodes we already visited, spread out from
    visited = set()
    prev_nodes = {0: -1}
    # (path_length,currentNode)
    to_visit = [(0, start_node_id, -1)]
    distance = _iterate_shortest_path(graph, visited, to_visit, end_nodes_ids, weight_type, prev_nodes)
    if distance == float("inf"):
        return distance, []
    temp = next(x for x in end_nodes_ids if x in prev_nodes.keys())
    from collections import deque
    path = deque()
    while temp != -1:
        path.appendleft(temp)
        temp = prev_nodes[temp]

    return distance, list(path)


def _iterate_shortest_path(graph, visited, to_visit, end_nodes, weight_type, prev_nodes):
    while True:
        if len(to_visit) == 0:
            # infinite length, path not found
            return float("inf")

        path_length, current_node, prev_node = to_visit[0]

        if current_node in visited:
            to_visit = to_visit[1:]
            continue
            # return _iterate_shortest_path(graph, visited, to_visit, end_nodes, weight_type, prev_nodes)

        visited.add(current_node)
        prev_nodes[current_node] = prev_node

        # found path
        if current_node in end_nodes:
            return path_length

        to_visit = to_visit[1:]

        node = graph.GetNI(current_node)
        degree = node.GetOutDeg()

        for i in xrange(degree):
            neib_id = node.GetOutNId(i)

            if neib_id in visited:
                continue

            edge = graph.GetEI(current_node, neib_id)
            weight = graph.GetFltAttrDatE(edge, weight_type)
            if abs(weight) < 1e-8 or abs(weight) > 1e+8:
                weight = 0.0
            to_visit.append((path_length + weight, neib_id,current_node))

        # sort by weights
        to_visit = sorted(to_visit)

        # return _iterate_shortest_path(graph, visited, to_visit, end_nodes, weight_type,prev_nodes)


def test():
    print "1) test path finding algorithm"
    G = snap.TNEANet().New()
    G.AddFltAttrN("Congestion")
    for i in range(10):
        G.AddNode(i)
    for i in range(9):
        id = G.AddEdge(i, i + 1)
        G.AddFltAttrDatE(id, float(1), "Congestion")
    # G.Dump()
    # path test
    for i in range(10):
        for j in range(i, 10):
            path_length,_ = find_shortest_path(G, i, [j], weight_type="Congestion")
            if path_length != abs(i-j):
                raise ValueError
    print "path test OK"

    # full graph test
    size = 10
    G = snap.GenFull(snap.PNEANet, size)
    G.AddFltAttrN("Congestion")
    for edge in G.Edges():
        id = edge.GetId()
        G.AddFltAttrDatE(id, float(1), "Congestion")

    for i in range(size):
        for j in range(i,size):
            path_length,_ = find_shortest_path(G, i, [j], weight_type="Congestion")
            if not (path_length == 1 and i != j or path_length == 0 and i == j):
                raise ValueError
    print "Full graph test OK"

    # weights test
    G = snap.TNEANet().New()
    G.AddFltAttrN("Congestion")
    for i in range(10):
        G.AddNode(i)
    for i in range(9):
        id = G.AddEdge(i, i + 1)
        G.AddFltAttrDatE(id, float(1), "Congestion")
    id = G.AddEdge(9, 0)
    G.AddFltAttrDatE(id, float(12), "Congestion")
    # G.Dump()
    # path test
    path_length,_ = find_shortest_path(G, 0, [9], weight_type="Congestion")
    if path_length != 9:
        raise ValueError
    print "weight test OK"

    # unconnected graph
    G = snap.TNEANet().New()
    G.AddFltAttrN("Congestion")
    for i in range(10):
        G.AddNode(i)
    for i in range(9):
        if i != 5:
            id = G.AddEdge(i, i + 1)
            G.AddFltAttrDatE(id, float(1), "Congestion")
    # G.Dump()
    # path test
    path_length,_ = find_shortest_path(G, 0, [9], weight_type="Congestion")
    if path_length != float("inf"):
        raise ValueError
    print "Unconnected test OK"
def test2():
    print "2) test path"
    G = snap.TNEANet().New()
    G.AddFltAttrN("Congestion")
    for i in range(10):
        G.AddNode(i)
    for i in range(9):
        id = G.AddEdge(i, i + 1)
        G.AddFltAttrDatE(id, float(1), "Congestion")
    # G.Dump()
    # path test
    print "shortest path {}, {}".format(*find_shortest_path(G, 0, [9,8], weight_type="Congestion"))

if __name__ == '__main__':
    test()
    test2()
    """
    from AnaheimRead import load_from_binary_stream
    graph = load_from_binary_stream()
    """

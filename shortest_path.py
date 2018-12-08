
# finds path with lowest sum
def find_shortest_path(graph,start_node_id,end_nodes_ids,weight_type = "Congestion"):
    if not graph.IsNode(start_node_id):
        print "start node is not in graph, node id:",start_node_id
        return
    for end_node_id in end_nodes_ids:
        if not graph.IsNode(end_node_id):
            print "end node is not in graph, node id:",end_node_id
            return
    
    #nodes we already visited, spread out from
    visited = set()
    to_visit = [(0,start_node_id)]
    
    return _iterate_shortest_path(graph,visited,to_visit,end_nodes_ids,weight_type)

def _iterate_shortest_path(graph,visited,to_visit,end_nodes,weight_type):
    if len(to_visit) == 0:
        #infinite length, path not found
        return float("inf")
    
    path_length,current_node = to_visit[0]
    
    if current_node in visited:
        to_visit = to_visit[1:]
        return _iterate_shortest_path(graph,visited,to_visit,end_nodes,weight_type)
    
    visited.add(current_node)
    
    # found path
    if current_node in end_nodes:
        return path_length
    
    to_visit = to_visit[1:]
    
    node = graph.GetNI(current_node)
    degree = node.getOutDeg()
    
    for i in xrange(degree):
        neib_id = node.GetOutNId(i)
        
        if neib_id in visited:
            continue
        
        edge = graph.GetEI(current_node,neib_id)
        weight = graph.GetFltAttrDatE(edge, weight_type)
        
        to_visit.append((path_length + weight, neib_id))
        
    # sort by weights
    to_visit = sorted(to_visit)
    
    return _iterate_shortest_path(graph,visited,to_visit,end_nodes,weight_type)
        
    
if __name__ == '__main__':
    from AnaheimRead import load_from_binary_stram
    graph = load_from_binary_stram()

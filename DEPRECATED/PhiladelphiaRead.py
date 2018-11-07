import snap
import pandas as pd
from AnaheimRead import save_to_biary_stream,load_from_binary_stram

def getGraph():
    table = pd.read_csv("phil_net_no_dummy")
    
    graph = snap.TNEANet.New()
    
    graph.AddFltAttrN("Flow")
    graph.AddFltAttrN("Capacity")
    graph.AddFltAttrN("Congestion")
    
    
    for index,fro,to,capac,length,ftime,B,power,speed,toll,typ in table.itertuples():
        min_capac = capac*24*3600
        
        if not graph.IsNode(fro):
            graph.AddNode(fro)
        if not graph.IsNode(to):
            graph.AddNode(to)
        
        temp_edge = graph.AddEdge(fro,to)
        
        graph.AddFltAttrDatE(temp_edge,ftime,"Flow")
        graph.AddFltAttrDatE(temp_edge,min_capac,"Capacity")
        graph.AddFltAttrDatE(temp_edge,ftime*1.0/(min_capac*1.0),"Congestion")
        
    return graph

def save(graph):
    save_to_biary_stream(graph,"Philadelphia.graph")
    
def load():
    graph = load_from_binary_stram("Philadelphia.graph")
    return graph

if __name__ == '__main__':
    graph = getGraph()
    print "generated",graph.GetNodes(), graph.GetEdges()
    
    save(graph)
    graph = load()
    print "loaded",graph.GetNodes(), graph.GetEdges()
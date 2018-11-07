from __future__ import division
import snap
import pandas as pd
from AnaheimRead import save_to_biary_stream

def read():
    with open("TransportationNetworks/Chicago-Sketch/ChicagoSketch_net.tntp") as fil:
        table = pd.read_csv(fil,sep="\t",header = 5)
        table = table.iloc[:,1:11]
    
    povezave = table.loc[:,["head node","tail node","capacity (veh/h)"]]
    graph = snap.TNEANet.New()
    graph.AddFltAttrN("Flow")
    graph.AddFltAttrN("Capacity")
    graph.AddFltAttrN("Congestion")
    
    
    # adding edges
    for _,fro,to,capac in povezave.itertuples():
         
        if not graph.IsNode(fro):
            graph.AddNode(fro)
        if not graph.IsNode(to):
            graph.AddNode(to)
        
        
        temp_edge = graph.AddEdge(fro,to)

        temp_edge_reverse = graph.AddEdge(to,fro)

        graph.AddFltAttrDatE(temp_edge,capac,"Capacity")
        graph.AddFltAttrDatE(temp_edge_reverse,capac,"Capacity")

    # adding congestion
    flow = pd.read_csv("TransportationNetworks/Chicago-Sketch/ChicagoSketch_flow.tntp",sep="\t")
    
    flow_povez = flow.iloc[:,[0,1,2]]
    
    for _,fro,to,flow_vol in flow_povez.itertuples():
        edge = graph.GetEI(fro,to)
        edge_id = edge.GetId()

        capac = graph.GetFltAttrDatE(edge_id, "Capacity")
        graph.AddFltAttrDatE(edge_id,flow_vol,"Flow")
        graph.AddFltAttrDatE(edge_id,flow_vol*1.0/capac,"Congestion")

        # reverse edge

        edge_rev = graph.GetEI(to, fro)
        edge_rev_id = edge_rev.GetId()
        capac_rev = graph.GetFltAttrDatE(edge_rev_id, "Capacity")
        graph.AddFltAttrDatE(edge_rev_id, flow_vol, "Flow")
        graph.AddFltAttrDatE(edge_rev_id, flow_vol * 1.0 / capac_rev, "Congestion")
    
    return graph

save_to_biary_stream(read(),path="ChicagoSketch.graph")
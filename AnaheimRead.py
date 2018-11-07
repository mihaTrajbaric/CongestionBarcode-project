from __future__ import division
#to have normal division where 1/3 = 0.333333 and not 0
import snap
import pandas as pd


def read():
    """

    reads anheim data and returns pandas dataframe

    :return: pandas datafrane
    """

    file = open("TransportationNetworks/Anaheim/Anaheim_net.tntp")

    #skip 7 lines
    for _ in range(7):
        file.readline()

    legenda = file.readline().split()
    legenda = [legenda[1],legenda[2]," ".join(legenda[3:5])," ".join(legenda[5:7]),
                " ".join(legenda[7:11]),legenda[11],legenda[12]," ".join(legenda[13:15]),legenda[15],legenda[16]]

    data = []
    for line in file:
        a = line.split()
        a = [float(x) for x in a[:-1]]
        data.append(a)
    network = pd.DataFrame(data[:-1],columns=legenda)
    file2 = open("TransportationNetworks/Anaheim/Anaheim_flow.tntp")
    for _ in range(5):
        file2.readline()
    clNames2 = file2.readline().split()
    clNames2 = [clNames2[1],clNames2[2],clNames2[4],clNames2[5]]

    data2 = []
    for line in file2:
        a = line.split()
        temp = [a[0],a[1],a[3],a[4]]
        data2.append(temp)

    flow = pd.DataFrame(data2, columns=clNames2)
    #print flow
    #print network
    network['Flow (veh/h)'] = flow['Volume']
    network['Cost'] = flow['Cost']

    network['Congestion'] = network['Flow (veh/h)'].astype(float) / network['Capacity (veh/h)'].astype(float)

    return network
def to_graph(pd):
    G = snap.TNEANet.New()
    node_id_max = int(pd.iloc[-1]['Tail'])
    #add nodes
    for i in range(1,node_id_max+1):
        G.AddNode(i)
    #defines float edge atributes
    G.AddFltAttrN("Flow")
    G.AddFltAttrN("Capacity")
    G.AddFltAttrN("Congestion")
    #adds edges
    for row in pd.iterrows():
        podatki = row[1]

        edge_temp_id = G.AddEdge(int(podatki['Tail']), int(podatki['Head']))
        G.AddFltAttrDatE(edge_temp_id, float(podatki['Flow (veh/h)']), "Flow")
        G.AddFltAttrDatE(edge_temp_id, float(podatki['Capacity (veh/h)']), "Capacity")
        G.AddFltAttrDatE(edge_temp_id, float(podatki['Congestion']), "Congestion")

        edge_temp_id_reverse = G.AddEdge(int(podatki['Head']),int(podatki['Tail']))
        G.AddFltAttrDatE(edge_temp_id_reverse, float(podatki['Flow (veh/h)']), "Flow")
        G.AddFltAttrDatE(edge_temp_id_reverse, float(podatki['Capacity (veh/h)']), "Capacity")
        G.AddFltAttrDatE(edge_temp_id_reverse, float(podatki['Congestion']), "Congestion")

    return G

def save_to_biary_stream(G, path = "Anheim.graph"):
    """

    saves graph to binary stream

    :param G: graph of type snap.TNEANet
    :param path: path to file graph
    :return: none
    """
    FOut = snap.TFOut(path)
    G.Save(FOut)
    FOut.Flush()

def load_from_binary_stram(path = "Anheim.graph"):
    """

    loads graph from binary stram file

    :param path:
    :return: graph of type snap.TNEANet
    """
    FIn = snap.TFIn(path)
    G = snap.TNEANet.Load(FIn)
    return G
def network():
    return to_graph(read())

def demo():
    print
    print "Z ukazom read() preberemo podatke Anheim_flow in Anheim_net"
    dataframe = read()
    print
    print "rezultat je pandas dataframe s stolpci:"
    print list(dataframe)
    print
    # first row in dataframe
    print "takole zgleda vrstica"
    print "_____________________________________"
    print dataframe.iloc[0]
    print "_____________________________________"
    print
    # graph
    print "z ukazom G = to_graph(dataframe) dobimo iz dataframa graf (tipa snap.TNEANet)"
    G = to_graph(dataframe)
    print
    print "graf si najlazje izpises z G.Dump()"
    # G.Dump()
    print
    print "ukaza save_to_biary_stream(G) in G1 = load_from_binary_stram() sta za shranjevanje in branje iz .graph datotek"
    # save_to_biary_stream(G)
    # G1 = load_from_binary_stram()
    # G1.Dump()
    print
    print "trenutno so na povezavah (float) atributi 'Flow','Capacity','Congestion'"

    print "na povezave dodajamo kot G.AddFltAttrDatE(edge_id, value, name_of_attribute)"
    print "beremo pa kot kot G.GetFltAttrDatE(edge_id, name_of_attribute)"
    print
    print "primer na povezavi edge_id = 2"

    print "Flow",G.GetFltAttrDatE(2, "Flow")
    print "Capacity",G.GetFltAttrDatE(2, "Capacity")
    print "Congestion",G.GetFltAttrDatE(2, "Congestion")
    print
    print "srecno!"

if __name__ == '__main__':
    demo()

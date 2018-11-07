from __future__ import division
import snap
import pandas as pd

def read(graph_name,columns = [i for i in range(1, 11)],fro = 0, to = 1,capacity = 2):
    
    path = "TransportationNetworks/{0}/{0}_net.tntp".format(graph_name)
    with open(path) as fil:
        for i in range(5):
            fil.readline()
        
        table = pd.read_csv(fil,sep="\t")
    
    table = table.iloc[:,columns]
    
    #dodajanje povezav
    G = snap.TNEANet.New()
    
    povezave = table.iloc[:,[fro,to,capacity]]
    
    for _,fro,to,capacity in povezave.itertuples():
        if(capacity != 1):
            print 2
        
    
read("Winnipeg")
    
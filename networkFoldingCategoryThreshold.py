import pandas as pd
import snap
import matplotlib.pyplot as plt
import numpy as np
import itertools
import csv
import gc

import glob
path1 = "Category Bipartite Graphs/*.csv"
path2 = "Category Unipartite Graphs/*.csv"

for fname1 in glob.glob(path1):
    for fname2 in glob.glob(path2):
        if fname1.split('/')[1] == fname2.split('/')[1]:
            newfilename = fname1.split('/')[1]
            print fname1, fname2

            #bipartite
            G1 = snap.LoadEdgeList(snap.PUNGraph, fname1, 0, 1, ",")
            #unipartite
            G2 = snap.LoadEdgeList(snap.PUNGraph, fname2, 0, 1)

            #for every edge in G2, check if the intersection of their neighbors is over a certain number

            #open 3 files
            with open(newfilename.rsplit('.',1)[0]+'_1.csv', 'w') as f, open(newfilename.rsplit('.',1)[0]+'_2.csv', 'w') as g, open(newfilename.rsplit('.',1)[0]+'_3.csv', 'w') as h:
                writer1 = csv.writer(f)
                writer2 = csv.writer(g)
                writer3 = csv.writer(h)

                for NI in G2.Nodes():
                    node1 = NI.GetId()
                    #iterate over neighbors of node1
                    Neighbors = snap.TIntV()
                    snap.GetNodesAtHop(G2, node1, 1, Neighbors, False)
                    NodeVec1 = snap.TIntV()
                    snap.GetNodesAtHop(G1, node1, 1, NodeVec1, False)

                    for i in Neighbors:
                        if i > node1:
                            node2 = i
                            NodeVec2 = snap.TIntV()
                            snap.GetNodesAtHop(G1, node2, 1, NodeVec2, False)
                            intersect = len(set(NodeVec1).intersection(NodeVec2))
                            print intersect
                            if intersect > 1:
                                writer1.writerow((node1, node2))
                            if intersect > 2:
                                writer2.writerow((node1, node2))
                            if intersect > 3:
                                writer3.writerow((node1, node2))




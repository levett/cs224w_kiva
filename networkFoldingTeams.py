import pandas as pd
import snap
import matplotlib.pyplot as plt
import numpy as np
import itertools
import csv
import gc


def getDataPointsToPlot(Graph):
    """
    :param - Graph: snap.PUNGraph object representing an undirected graph

    return values:
    X: list of degrees
    Y: list of frequencies: Y[i] = fraction of nodes with degree X[i]
    """
    ############################################################################
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(Graph, DegToCntV)
    N = Graph.GetNodes()

    X, Y = [item.GetVal1() for item in DegToCntV], [np.true_divide(item.GetVal2(), N) for item in DegToCntV]

    ############################################################################
    return X, Y

G = snap.LoadEdgeList(snap.PNGraph, "team_data_bipartite.csv", 0, 1, ",")

# if the graph is loan id to user id, Out/In deg count, and set item.GetVal2() to zero

print "Loan nodes: %d" % (snap.CntInDegNodes(G, 0))
print "Lender nodes: %d" % (snap.CntOutDegNodes(G, 0))
print "Loan-Lender Edges: %d" % (G.GetEdges())

OutDegV = snap.TIntPrV()
snap.GetNodeOutDegV(G, OutDegV)

# Lender = [item.GetVal1() for item in OutDegV if item.GetVal2() == 0]
#
# NG = snap.TUNGraph.New()
# j = 0
# for i in Lender:
#     print j
#     if not NG.IsNode(i):
#         NG.AddNode(i)
#     NodeVec = snap.TIntV()
#     snap.GetNodesAtHop(G, i, 2, NodeVec, False)
#     for item in NodeVec:
#         if not NG.IsNode(item):
#             NG.AddNode(item)
#         if not NG.IsEdge(i, item):
#             NG.AddEdge(i, item)
#     j = j + 1


x_Graph1, y_Graph1 = getDataPointsToPlot(G)
plt.loglog(x_Graph1, y_Graph1, linestyle='dashed', color='r', label='Graph 1')

plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of Graph 1 and Graph 2')
plt.legend()
plt.savefig('DegreeDist.png')
plt.close()


#snap.SaveEdgeList(NG, 'team_unipartite_edgelist.txt')


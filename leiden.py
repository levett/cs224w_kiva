import snap
import igraph as ig
import leidenalg as la
import json as json
from matplotlib import pyplot as plt
from heapq import nlargest

def doLeidenAlg(fileName): 
    G = ig.Graph.Read_Edgelist("/Users/lilyinthesun/Documents/Code/data/" + fileName + ".csv", directed=False)
    partition = la.find_partition(G, la.ModularityVertexPartition, n_iterations=-1)

    with open("Leiden/leiden_result_" + fileName, "w") as leiden_result:
        leiden_result.write(str(partition))

    # Reformat the partition data into list of lists.
    clusters = []

    for x in range(len(partition)):
        if len(partition[x]) > 1:
            clusters.append(partition[x])
        else:
            break

    with open("Leiden/leiden_result_lists_" + fileName, "w") as leiden_result:
        leiden_result.write(str(clusters))

    plotClusterDist(clusters, fileName)


def plotClusterDist(clusters, fileName):
    # Plot the cluster distribution.
    X, Y = [], []

    # Construct a count dictionary.
    degCount = {}
    for cluster in clusters:
        size = len(cluster)
        # Update the dictionary depending on whether this particular size
        # has been counted before or not.
        if size in degCount:
            degCount[size] += 1
        else:
            degCount[size] = 1

    # Extract the dictionary information into arrays.
    for size, count in degCount.items():
        X.append(size)
        Y.append(count)

    plt.scatter(X, Y)
    plt.xlabel('Number of nodes in partition')
    plt.ylabel('Number of partitions')
    plt.title('Size distribution of Leiden partitions generated from ' + fileName)
    plt.savefig(fileName + '_Leiden_1.png')
    plt.close()
    plt.scatter(X, Y)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Number of nodes in partition')
    plt.ylabel('Number of partitions')
    plt.title('Log log size distribution of Leiden partitions generated from ' + fileName)
    plt.savefig(fileName + '_Leiden_log.png')
    plt.close()

def doAnalysis(fileName):
    doLeidenAlg(fileName)

def doAnalysisPostLeiden(fileName):
    with open("Leiden/leiden_result_lists_" + fileName) as json_data:
        myjson = json.load(json_data)
    print("read")
    # Reformat the partition data into list of lists.
    clusters = []

    for x in range(len(myjson)):
        clusters.append(myjson[x])
    print("clusters done")
    plotClusterDist(clusters, fileName)

# datasets = ['Arts', 'Clothing', 'Construction', 'Education', 'Entertainment', 'Health', 'Housing', 'Manufacturing', 'PersonalUse', 'Retail', 'Services', 'Transportation', 'Wholesale']
datasets = ['Housing', 'Manufacturing', 'Personal Use', 'Retail', 'Services', 'Transportation', 'Wholesale']

for dataset in datasets:
    myname = dataset
    doAnalysisPostLeiden(myname)

# doAnalysis("Food_2")
# doAnalysisPostLeiden("Food_1")

# topClusterSet = set([])

# for x in range(0, 10):
#     for myID in clusters[x]:
#         topClusterSet.add(myID)

# G1 = snap.LoadEdgeList(snap.PNGraph, "kiva_data/bipartite_edgelist_Q42017.csv", 0, 1, ",")
# G2 = snap.LoadEdgeList(snap.PUNGraph, "kiva_data/unipartite_edgelist_Q42017.txt", 0, 1, "\t")
# topClusterSets = []
# for x in range(0, 1):
#     topClusterSets.append(set(clusters[x]))

# NIdList = []

# for NI in G1.Nodes():
#     NIdList.append(NI.GetId())

# topLoans = nlargest(50, NIdList, key=lambda myID: G1.GetNI(myID).GetOutDeg())
# average = 0

# for loan in topLoans:
#     loanNI = G1.GetNI(loan)
#     myCount = 0

#      # for y in range(0, 11):
#     for x in range(loanNI.GetOutDeg()):
#         nbrNId = loanNI.GetNbrNId(x)
#         if nbrNId in topClusterSets[0]:
#             myCount += 1

#     # print("cluster percentage: %s" % (len(topClusterSets[y]) * 1.0 / 189720))
#     percentage = myCount * 1.0 / loanNI.GetOutDeg()
#     average += percentage
#     print(percentage)

# print("average: %s" % (average / 50.0))

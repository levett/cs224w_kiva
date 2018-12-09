import snap
import sys
from collections import defaultdict
import csv
import math
import copy
from apyori import apriori

FAN_THRESHOLD = 3
LOAN_CENTER_PRUNING_THRESHOLD = 125
MIN_CORE = 3
MAX_CORE = 9

donors = set()
potential_fans = set()

loans = set()

neighbor_num_to_fan = defaultdict(set) #{KEY: Node Degree, VALUE: Set of DONORS with degree = KEY}
fan_to_neighbors = defaultdict(set) #{KEY: Node ID of 'Fan' Node (defined by fan threshold for degree), VALUE: Neighbors of node with ID = KEY}

csv_file = sys.argv[1] #Bipartite Graph to Read

"""
LOAD DONOR/LOAN SETS
"""
with open(csv_file, "r") as network_f:
	next(network_f)
	if ".tsv" not in csv_file:
		with open(csv_file + ".tsv", "w") as new_tsv_file:
			for loan_pair in network_f:
				new = loan_pair.replace(",", "\t")
				new_tsv_file.write(new + "\n")
		file_to_read = csv_file + ".tsv"
	else:
		file_to_read = csv_file

with open(csv_file, "r") as network_f:
	next(network_f)
	for line in network_f:
		line = line.split(",")
		loans.add(int(line[0]))
		donors.add(int(line[1]))

"""
LOAD GRAPH
"""
GRAPH = snap.LoadEdgeList(snap.PUNGraph, file_to_read, 0, 1)

print "START NODE NUMBER: ", GRAPH.GetNodes()
print "START EDGE NUMBER: ", GRAPH.GetEdges()


"""
Duplicates/Shingling: NOT APPLICABLE TO OUR NETWORK (assuming no duplicate loans - or even if duplicate loans,
assuming people are not donating to duplicate loans)
"""

"""
Prune Centers (Loans) by In-Degree Distribution. NOTE. Not perfectly relevant, but would be interesting to compare with and without
, and it isn't that much more work to include it. It DOES help us get rid of super nodes.
"""

print "PRUNING CENTERS (LOANS) BY IN-DEGREE DISTRIBUTINO"
NIdV = snap.TIntV()
NodesToDel = snap.TIntV()
for nodeId in loans:
	num_neighbors = snap.GetNodesAtHop(GRAPH, nodeId, 1, NIdV, False)
	if num_neighbors >= LOAN_CENTER_PRUNING_THRESHOLD:
		NodesToDel.Add(nodeId)

for nid in NodesToDel:
	loans.remove(nid)
snap.DelNodes(GRAPH, NodesToDel)
print "PRUNED CENTERS"


print "POST IN-DEGREE PRUNE NODE NUMBER: ", GRAPH.GetNodes()
print "POST IN-DEGREE PRUNE EDGE NUMBER: ", GRAPH.GetEdges()


"""
ITERATIVE PRUNING - Iteratively remove nodes with degree less than (arbitrary) cutoff

Note: The authors of trawling paper include optimizations for this step which I've deemed irrelevant. 
It runs in 1-2 minutes (depending on cutoff size) for 3 months (ALL types of loans),
so for a full year of Kiva data, it still should be pretty fast, especially when SPLIT BY 
TYPES OF LOANS. 
"""
degree_map = {}
donor_to_loans = {}

def iterative_prune(i, j, Graph):
	while(True):
		print "PRUNING"
		print "CURRENT NODE NUMBER: ", Graph.GetNodes()
		print "CURRENT EDGE NUMBER: ", Graph.GetEdges()
		deleted = False
		NIdV = snap.TIntV()

		DonorsToDel = snap.TIntV()
		for d in donors2:
			num_neighbors = snap.GetNodesAtHop(Graph, d, 1, NIdV, False)
			if num_neighbors < j:
				deleted = True
				DonorsToDel.Add(d)
		for nid in DonorsToDel:
			donors2.remove(nid)
		snap.DelNodes(Graph,DonorsToDel)

		LoansToDel = snap.TIntV()
		for l in loans2:
			num_neighbors = snap.GetNodesAtHop(Graph, l, 1, NIdV, False)
			if num_neighbors < i:
				deleted = True
				LoansToDel.Add(l)
		for nid in LoansToDel:
			loans2.remove(nid)
		snap.DelNodes(Graph,LoansToDel)

		if not deleted:
			break


	print "POST-ITERATIVE PRUNING NODE NUMBER: ", Graph.GetNodes()
	print "POST-ITERATIVE PRUNING: ", Graph.GetEdges()

	print "POST-ITERATIVE PRUNING DONOR NUMBER: ", len(donors2)
	print "POST-ITERATIVE PRUNING LOAN NUMBER: ", len(loans2)

	print "Updating Donor Degree Map"

	for donor in donors2:
		NIdV = snap.TIntV()
		degree_map[donor] = snap.GetNodesAtHop(Graph, donor, 1, NIdV, False)
		donor_to_loans[donor] = set([nid for nid in NIdV])

	# for loan in loans2:
	# 	NIdV = snap.TIntV()
	# 	degree_map[donor] = snap.GetNodesAtHop(Graph, donor, 1, NIdV, False)
	# 	donor_to_loans[donor] = set([nid for nid in NIdV])



core_count = defaultdict(int)
cores = defaultdict(list)


def inc_ex_prune(i, j, Graph):
	donors_to_del = set()

	for d1 in donors2:
		if degree_map[d1] == j:
			l1 = donor_to_loans[d1]
			loan_neighbor_sets = []
			for loan in l1:
				n_set = set()
				NIdV = snap.TIntV()
				snap.GetNodesAtHop(Graph, loan, 1, NIdV, False)
				for n in NIdV:
					n_set.add(n)
				loan_neighbor_sets.append(n_set)
			shared_neighbors = set.intersection(*loan_neighbor_sets)
			num_shared_neighbors = len(shared_neighbors) #donors in core
			if num_shared_neighbors < i:
				#continue
				Graph.DelNode(d1)
				donors_to_del.add(d1)
			else: 
				core_count[(i,j)] += 1
				cores[(i,j)].append(list(shared_neighbors) + list(l1)) 
				donors_to_del.add(d1) #NOTE: try with and without a few times
	for d in donors_to_del:
		donors2.remove(d)



#print apriori_loan_list
# results = list(apriori(apriori_loan_list))
# print results
# for result in results:
# 	print result.support


# donors2 = copy.deepcopy(donors)
# loans2 = copy.deepcopy(loans)
# priori_graph = snap.LoadEdgeList(snap.PUNGraph, file_to_read, 0, 1)
# iterative_prune(3, 3, priori_graph)

# apriori_loan_list = []
# #TEST APRIORI
# with open('3-3-trawl-donors.tsv', "w") as pre_priori_file:
# 	for loan in loans2:
# 		NIdV = snap.TIntV()
# 		snap.GetNodesAtHop(priori_graph, loan, 1, NIdV, False)
# 		for donor in NIdV:
# 			pre_priori_file.write(str(donor)+",")
# 		pre_priori_file.write("\n")
	# #print n_list
	# if len(n_list) < 10:
	# 	apriori_loan_list.append(n_list)
		
	# if count == 20: 
	# 	print apriori_loan_list
	# 	break
		



#UNCOMMENT BELOW FOR OVERALL CODE
for i in range(3, 11):
	curr_graph = snap.LoadEdgeList(snap.PUNGraph, file_to_read, 0, 1)
	donors2 = copy.deepcopy(donors)
	loans2 = copy.deepcopy(loans)
	for j in range(3, 9):
		iterative_prune(i, j, curr_graph)
		inc_ex_prune(i, j, curr_graph)

		print core_count





#With pruning Inc/Exc: {(7, 3): 64, (5, 6): 1, (9, 4): 10, (8, 5): 1, (3, 3): 224, (10, 3): 42, (4, 4): 38, (6, 3): 82, (3, 6): 2, (5, 3): 96, (6, 4): 22, (5, 4): 29, (10, 4): 8, (4, 5): 9, (9, 3): 49, (3, 5): 16, (7, 5): 2, (6, 5): 4, (5, 5): 7, (8, 3): 53, (4, 6): 1, (7, 4): 19, (4, 3): 130, (3, 4): 51, (8, 4): 14})
#Without Prunin


#{(5, 4): 29, (3, 3): 224, (4, 5): 9, (4, 4): 38, (5, 5): 7, (4, 3): 130, (5, 3): 96, (3, 4): 51, (3, 5): 16})



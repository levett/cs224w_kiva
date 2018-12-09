import csv
import sys 
import json
from collections import defaultdict
import random

def jaccard_similarity(a, b):
	return float(len(a.intersection(b)))/len(a.union(b))

def common_neighbors(a,b):
	return len(a.intersection(b))

#PASS IN 100 TRUTH TEAMS
#Truth: {Team ID => Set of teams}
#Detected: {List of Set of Teams}
def compare_communities_truth(detected, truth):
	max_jaccard_score = defaultdict(float)
	common_neighbors_for_max_jaccard = defaultdict(int)
	max_jaccard_folks = defaultdict(set)

	for team in truth:
		team_set = truth[team]
		for det_set in detected:
			jacc = jaccard_similarity(team_set, det_set)
			cn = common_neighbors(team_set, det_set)
			if jacc > max_jaccard_score[team] and cn > 1:
				max_jaccard_score[team] = jacc
				common_neighbors_for_max_jaccard[team] = cn
				max_jaccard_folks[team] = det_set

	return max_jaccard_score, max_jaccard_folks, common_neighbors_for_max_jaccard

def get_rand_max_jaccard(randomized, truth):
	max_randomized_score, max_randomized_group, cn_rand = compare_communities_truth(randomized, truth)

	max_randomized_jaccard_overall = 0
	cn_rand_max_jaccard = 0

	len_team_best_sim_rand = {}

	len_folks_rand = set()

	for team in truth:
		if max_randomized_score[team] > max_randomized_jaccard_overall:# and cn_rand[team] > 1:
			cn_rand_max_jaccard = cn_rand[team]
			len_team_best_sim_rand[team] = len(max_randomized_group[team])
			max_randomized_jaccard_overall = max_randomized_score[team]

	for k2 in len_team_best_sim_rand:
		len_folks_rand.add(len_team_best_sim_rand[k2])

	return max_randomized_jaccard_overall

def get_det_max_jaccard(detected, truth):
	max_detected_score, max_detected_group, cn_detected = compare_communities_truth(detected, truth)

	max_deteced_jaccard_overall = 0
	cn_det_max_jaccard = 0

	len_team_best_sim_det = {}
	len_folks_det = set()

	for team in truth:
		if max_detected_score[team] > max_deteced_jaccard_overall:# and cn_detected[team] > 1:
			cn_det_max_jaccard = cn_detected[team]
			len_team_best_sim_det[team] = len(max_detected_group[team])
			max_deteced_jaccard_overall = max_detected_score[team]

	for k1 in len_team_best_sim_det:
		len_folks_det.add(len_team_best_sim_det[k1])

	return max_deteced_jaccard_overall


def shuffle_lists_maintain_sizes(list_of_lists):
	members = []
	sizes = []
	for lst in list_of_lists:
		sizes.append(len(lst))
		for item in lst:
			members.append(item)
	random.shuffle(members)


	new_lists = []
	for size in sizes:
		new_list = []
		for i in range(0, size):
			new_list.append(members.pop())
		new_lists.append(new_list)
	
	return new_lists

if __name__ == "__main__":
	det_file =open(sys.argv[1])
	det_json_array = json.load(det_file)

	shuffled_json_array = shuffle_lists_maintain_sizes(det_json_array)
	
	truth = (sys.argv[2])
	truth_map = defaultdict(set)

	with open(truth) as truth_file:
		truthreader = csv.reader(truth_file)
		for row in truthreader:
			#print row
			truth_map[int(row[0])].add(int(row[1]))

	#print truth_map
	num_iter = 100

	det_max_jaccard = get_det_max_jaccard(det_json_array, truth_map)

	for i in range(num_iter):
		det = 0
		rand = 0
		shuffled_json_array = shuffle_lists_maintain_sizes(det_json_array)
		rand_jaccard = get_rand_max_jaccard(shuffled_json_array, truth_map)
		if det_max_jaccard > rand_jaccard:
			print i, "DET", det_max_jaccard - rand_jaccard
			det += 1
		else:
			print i, "RAND", rand_jaccard - det_max_jaccard
			rand += 1
	p_val = float(rand)/num_iter
	print p_val




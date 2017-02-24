#!/usr/bin/env python
# coding=utf-8

###################################################

# each item to be packed is represented as a set of triples (size,value,name)
def itemSize(item): return item[0]
def itemValue(item): return item[1]
def itemName(item): return item[2]

# David Eppstein © ICS, UCI, 2/22/2002
def knapsack_0_1(items,sizeLimit):
	P = {}
	for nItems in range(len(items)+1):
		for lim in range(sizeLimit+1):
			if nItems == 0:
				P[nItems,lim] = 0
			elif itemSize(items[nItems-1]) > lim:
				P[nItems,lim] = P[nItems-1,lim]
			else:
				P[nItems,lim] = max(P[nItems-1,lim],
					P[nItems-1,lim-itemSize(items[nItems-1])] +
					itemValue(items[nItems-1]))

	L = []
	nItems = len(items)
	lim = sizeLimit
	while nItems > 0:
		if P[nItems,lim] == P[nItems-1,lim]:
			nItems -= 1
		else:
			nItems -= 1
			L.append(itemName(items[nItems]))
			lim -= itemSize(items[nItems])

	L.reverse()
	return L


###################################################


from itertools import groupby
from operator import itemgetter
import sys

def parse_file(file_name):

	f = open(file_name)

	### Parse numbers:

	numbers = f.readline().split()
	V = int(numbers[0])
	E = int(numbers[1])
	R = int(numbers[2])
	C = int(numbers[3])
	X = int(numbers[4])

	size_videos_ante = f.readline().split() # V numbers, one for each video (size in Mb)
	size_videos = [int(size) for size in size_videos_ante]

	### Parse endpoints:

	endpoints = []
	for i in range(E):
		LDK = f.readline().split()
		Ld = int(LDK[0]) # Latency of serving a video request from the data center to its endpoint
		K = int(LDK[1]) # Number of cache servers at this endpoint

		cache_servers_at_endpoint_i = []
		for j in range(K):
			CidLC = f.readline().split()
			cid = int(CidLC[0]) # Id (we don't care, it's just the position in the array)
			Lc = int(CidLC[1])
			cache_servers_at_endpoint_i.append((cid, Lc))

		endpoints.append( (Ld, K, cache_servers_at_endpoint_i) )

	### Parse requests:

	requests = []
	for i in range(R):
		RRR = f.readline().split()
		Rv = int(RRR[0])
		Re = int(RRR[1])
		Rn = int(RRR[2])
		requests.append((Rv, Re, Rn))

	return V, E, R, C, X, size_videos, endpoints, requests


def countRequest(file_name):

	V, E, R, C, X, size_videos, endpoints, requests = parse_file(file_name)

	#print(requests)
	#print(endpoints[requests[0][1]][2][0])

	caches = []

	for c in range(C):
		caches.append([])

	for r in requests:
		# r[0] is video #
		# r[1] is is endpoint
		# r[2] is # of request
		# endpoints[r[1]][2][0]  -- Latency to datacenter
		# endpoints[r[1]][2][1]  -- # of caches
		# endpoints[r[1]][2][2]  -- list of caches
		for c in endpoints[r[1]][2]:
			# c[0] is the cache,
			# c[1] is the latency
			#print(c[0])
			caches[c[0]].append((r[0], (endpoints[r[1]][0] - c[1]) * r[2]))

	#for c in range(C):
	 #   print(len(caches[c]))
	sortedCaches = []

	for c in range(C):
		first = itemgetter(0)
		sums = {(k, sum(item[1] for item in tups_to_sum)) for k, tups_to_sum in groupby(sorted(caches[c], key=first), key=first)}
		sortedCaches.append(sorted(sums, key=lambda x: x[1], reverse=True))

	toReturn = []

	for c in range(C):

		nbVideosInCache = len(sortedCaches[c])
		cumulatedSum = 0;

		# Solve kind of a 0/1 Knapsack problem,
		# Where the weight is the size of the movie,
		# And the value is the score of this movie in this cache.

		items = []
		for v in range(nbVideosInCache):
			videoScores = sortedCaches[c][v]
			videoId = videoScores[0]
			score = videoScores[1]
			weight = size_videos[videoId]
			items.append((weight, score, videoId))

		capacity = X

		knapsack_assignment = knapsack_0_1(items,capacity)

		# Caches are almost full, thx to Knapsack
		# S = 0
		# for video in knapsack_assignment:
			# S += size_videos[video]
		# print S

		toReturn.append(knapsack_assignment)

	return toReturn, C


if __name__ == '__main__':

	# Same value for each:
	# WEIGHT / VALUE / ITEM NAME
	# exampleItems = [(3,1,'A'),
	# 				(4,1,'B'),
	# 				(8,1,'C'),
	# 				(10,1,'D'),
	# 				(15,1,'E'),
	# 				(20,1,'F')]
	# exampleSizeLimit = 20
	# print knapsack_0_1(items,exampleSizeLimit)

	if len(sys.argv) < 2:
		print('Usage: python naive.py <file_name>')
		exit(1)

	file_name = sys.argv[1]

	topRequests, C = countRequest(file_name)


	output_file_name = file_name[:-3] + '.out'
	output_file = open(output_file_name, 'w')

	output_file.write(str(C) + '\n')

	for c in range(C):
		output_file.write(str(c) + ' ')
		for v in topRequests[c]:
			output_file.write(str(v) + ' ')
		output_file.write('\n')

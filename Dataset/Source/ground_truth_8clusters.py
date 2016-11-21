## Library needed : json ##
## inputfile : mappingfile, clustertagfile, raw tweet directory, input dataset ##
## Usage : This script creates the ground truth file for 8clusters from a given dataset ##

import os, json

mappingfilename = '/home/trishnendu/Graph_Lab/Term_project/Mapping/index_id_map.txt'
clustertagfilename = '/home/trishnendu/Graph_Lab/Term_project/Dataset/Raw_dataset/tweet-clustering-data.txt'
rawdatadirname = '/home/trishnendu/Graph_Lab/Term_project/Dataset/Raw_dataset/jsonl'
inputfilename = '/home/trishnendu/Graph_Lab/Term_project/Dataset/Test_dataset/withnohashstem(mapped)/randomsample_100_withnohashstem(mapped)_ground_truth.txt'
outputfilename = '/home/trishnendu/Graph_Lab/Term_project/Dataset/Test_dataset/withnohashstem(mapped)/randomsample_100_withnohashstem(mapped)_8cluster_ground_truth.txt'

mappingfile = open(mappingfilename)
inputfile = open(inputfilename)
outfile = open(outputfilename,"w")
clustertagfile = open(clustertagfilename)

indexidmap = {}
samplevertex = set()
hashcluster = []
ground_truth = {}

for line in mappingfile.read().split("\n"):
	line = line.split(" ")
	if len(line) == 2:
		indexidmap[int(line[0])] = line[1]

for line in inputfile.read().split("\n"):
	line = line.split(",")
	if len(line) > 0:
		line = set(line)
		samplevertex |= line

for line in clustertagfile.read().split("\n\n"):
	line = line.split(",")
	if len(line) > 0:
		hashset = set()
		for hashtag in line:
			hashtag = hashtag.replace("#","")
			hashset.add(hashtag.strip().lower())
		print(hashset)
		hashcluster.append(hashset)

print(len(hashcluster))

for filename in os.listdir(rawdatadirname):
	if ".json" in filename:
		data=open(rawdatadirname+"/"+filename).read().split("\n")
		filename = filename.replace("-tweets.jsonl","").lower()
		clusterid = -1
		for i in range(len(hashcluster)):
			for hashtag in hashcluster[i]:
				if hashtag in filename:
					clusterid = i
					break
		print((filename, clusterid))
		if clusterid not in ground_truth:
			ground_truth[clusterid] = set()
		for i in range(len(data)-1):
			jo=json.loads(data[i])
			if indexidmap[jo['id']] in samplevertex:
				ground_truth[clusterid].add(int(indexidmap[jo['id']]))

print(len(ground_truth))
for i in ground_truth:
	outfile.write(",".join(str(e) for e in ground_truth[i]))
	outfile.write("\n")
outfile.close()			





  

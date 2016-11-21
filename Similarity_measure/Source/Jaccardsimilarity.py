import os
from sklearn.cluster import KMeans
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def readdata(inputfile):
	tweets = {}
	infile = open(inputfile)
	
	inputdata = infile.read().split("\n\n")
	for data in inputdata:
		d = data.split("\n")
		if len(d) >= 2:	tweets[d[0]] = d[1]
	return tweets
		
def Jaccardsim(tweets,id1,id2):
	tweet1_terms = set(tweets[id1].split(" "))
	tweet2_terms = set(tweets[id2].split(" "))
	score = len(tweet1_terms & tweet2_terms) / (len(tweet1_terms | tweet2_terms))	
	return score

def Kmeansclustering(tweets, nclusters):
	X = []
	indexlist = list(tweets.keys())
	for i in range(len(indexlist)):
		vec = []
		for j in range(len(indexlist)):
			print((i,j,len(indexlist)))
			vec.append(Jaccardsim(tweets, indexlist[i], indexlist[j]))
		X.append(vec)
	X = np.array(X)
	cluster = KMeans(nclusters)
	pred = cluster.fit_predict(X)
	res = [[] for i in range(nclusters)]
	for i in range(len(pred)):
		res[pred[i]].append(indexlist[i])
	outfilename = "/home/trishnendu/Graph_Lab/Term_project/Clustering/Test_clusters/Jaccard_clusterKmean42_on_complete_withash(mapped).txt"
	outfile = open(outfilename,"w")
	for i in res:
		outfile.write(",".join(str(e) for e in i))
		outfile.write("\n")
	outfile.close()

if __name__ == '__main__':
	inputfile = "/home/trishnendu/Graph_Lab/Term_project/Dataset/Test_dataset/complete(mapped)/complete_withash(mapped).txt"
	tweets = readdata(inputfile)
	#Kmeansclustering(tweets, 8)
	outfile = open('/home/trishnendu/Graph_Lab/Term_project/Similarity_measure/Similarity_graphs/Jaccard_graph_on_randomsample_200_withonlyhash(mapped).txt','w')
	#outfile = open("similarity_score_jaccard_on_" + inputfile.replace('.txt',"").split("/")[-1] + "(mapped)",'w')
	ids = list(tweets.keys())
	for i in range(len(ids) - 1):
		for j in range(i + 1, len(ids)):
			print((i, j))
			similarity_score = Jaccardsim(tweets, ids[i], ids[j])
			if( similarity_score > 0):
				outfile.write(ids[i] + "," + ids[j] + "," + str(similarity_score) + "\n")
	outfile.close()

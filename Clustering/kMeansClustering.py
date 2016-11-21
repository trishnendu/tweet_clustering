## Library needed : sklearn, ldatest ##
## Files needed : stopwordfile, mappingfile ##
## Usage : This script takes the similarity graph and create clusters using kMeansCluster ## 


from sklearn.cluster import KMeans
from time import time
#from ldatest import *
import numpy as np

class kMeansCluster(object):
	
	def __init__(self, M, n_clusters):
		# M is a 2D MAtrix, each row represents the point/vector of a node
		self.cluster = KMeans(n_clusters)
		self.data = M
		
	def predictClusters(self):
		t0 = int(time())
		res = self.cluster.fit_predict(self.data)
		t1 = int(time())
		print "Completed in %d mins %d secs"%( (t1-t0)/60 , (t1-t0)%60)
		#res is a array containing the predicted cluster of each nodes
		return res
		
def create_adjmatrix(edglistfilename):
	edgelist = open(edgelistfilename).read()
	adj_matrix = {}
	vertex_set = set()
	edgelist = edgelist.split("\n")
	N = len(edgelist)
	cnt = 0 
	for line in edgelist:
		line = line.split(",")
		print((cnt, N))
		cnt += 1
		if len(line) == 3:
			vertex1 = int(line[0])
			vertex2 = int(line[1])
			vertex_set.add(vertex1)
			vertex_set.add(vertex2)
			edge_weight = float(line[2])
			if 	vertex1 in adj_matrix:
				adj_matrix[vertex1][vertex2] = edge_weight
			else:
				adj_matrix[vertex1] = {}
				adj_matrix[vertex1][vertex2] = edge_weight

			if 	vertex2 in adj_matrix:
				adj_matrix[vertex2][vertex1] = edge_weight
			else:
				adj_matrix[vertex2] = {}
				adj_matrix[vertex2][vertex1] = edge_weight

	return adj_matrix, list(vertex_set)
 
		 
#testing below
if __name__=='__main__':
	edgelistfilename = '/home/trishnendu/Graph_Lab/Term_project/Similarity_measure/Similarity_graphs/Jaccard_graph_on_randomsample_200_withonlyhash(mapped).txt'
	adj, vertex_list = create_adjmatrix(edgelistfilename)
	X = []
	for i in vertex_list:
		vec = []
		for j in vertex_list:
			if j in adj[i]:
				vec.append(adj[i][j])
			else:
				vec.append(0)
		X.append(vec)
	X = np.array(X)
	nclusters = 42
	KM = kMeansCluster(X, nclusters)
	pred = KM.predictClusters()
	res = [[] for i in range(nclusters)]
	for i in range(len(pred)):
		res[pred[i]].append(vertex_list[i])
	outfilename = "/home/trishnendu/Graph_Lab/Term_project/Clustering/Test_clusters/Jaccard_clusterKmean42_on_randomsample_200_withonlyhash(mapped).txt"
	outfile = open(outfilename,"w")
	for i in res:
		outfile.write(",".join(str(e) for e in i))
		outfile.write("\n")
	outfile.close()


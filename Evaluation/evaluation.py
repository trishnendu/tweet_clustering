## Library needed : sklearn, numpy ##
## Files needed : ground_truth, testClusters ##
## Usage : This script takes the two clusters (one test clusters and a ground truth and compares ) ## 


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time
import numpy as np
import math

class evaluate(object):
	def __init__(self,testFile, standardFile ):
		#data format: each line denotes a cluster, has tweet IDs 
		tp = open(testFile)
		sp = open(standardFile)
		
		self.testClusters = []
		self.standardClusters = []
		self.N = 0
		
		for line in tp.read().split("\n"):
			tmp = line.split(",")
			self.testClusters.append(tmp)
			self.N += len(tmp)
			
		cnt = 0
		
		for line in sp.read().split("\n"):
			tmp = line.split(",")
			self.standardClusters.append(tmp)
			cnt += len(tmp)
		
		'''	
		print((cnt, self.N))
		if cnt != self.N:
			print ("Different #nodes in the 2 clusters")
			raise Exception'''
		tp.close()
		sp.close()
	
	
	
	def getEntropies(self):	
		def _numberOfCommonIDs(C, K):
			cnt = 0
			for ID in C:
				if ID in K:
					cnt+=1
			return cnt
	
		def _entropy(cluster1, cluster2): 
			res = 0.0;
			
			for c in range(len(cluster1)):
				prob = 0.0
				for k in range(len(cluster2)):
					Ack = float(_numberOfCommonIDs(cluster1[c], cluster2[k]))
					prob += Ack
				prob /= self.N
				
				res += (prob * math.log((prob),2))
			return -res
		
		return [ _entropy(self.testClusters, self.standardClusters), _entropy(self.standardClusters, self.testClusters)] 
	
	
	
	
	
	def getConditionalEntropies(self):
		def _numberOfCommonIDs(C, K):
			cnt = 0
			for ID in C:
				if ID in K:
					cnt+=1
			return cnt 
	
		def _condEntropy(cluster1, cluster2): 
			res = 0.0;
			
			
			for k in range(len(cluster2)):
				sumAck = 0.0
				for c in range(len(cluster1)):
					sumAck += float(_numberOfCommonIDs(cluster1[c], cluster2[k]))
					
				for c in range(len(cluster1)):
					Ack = float(_numberOfCommonIDs(cluster1[c], cluster2[k]))
					if (Ack/sumAck) != 0:
						tmp = Ack/self.N * math.log((Ack/sumAck), 2)
						res += tmp
				
			return -res
		
		return [ _condEntropy(self.testClusters, self.standardClusters), _condEntropy(self.standardClusters, self.testClusters)] 
	
		
		
	
	def getVmeasure(self):
		cond1,cond2 = self.getConditionalEntropies()
		ent1, ent2 = self.getEntropies()
		h = 1 - cond1/ent1
		c = 1 - cond2/ent2
		return 2*h*c / (h + c)
		
	def getNVImeasure(self):
		cond1,cond2 = self.getConditionalEntropies()
		ent1, ent2 = self.getEntropies()
		
		if ent2 == 0:
			return ent1
		else:
			return (cond1 + cond2) / ent2

if __name__ ==	'__main__':
	e = evaluate('/home/trishnendu/Graph_Lab/Term_project/Clustering/Test_clusters/Lda_clusterKmean42_on_randomsample_100_withash(mapped).txt',"/home/trishnendu/Graph_Lab/Term_project/Dataset/Test_dataset/withash(mapped)/randomsample_100_withash(mapped)_ground_truth.txt")
	print(e.getVmeasure())
	print(e.getNVImeasure())


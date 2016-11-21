from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time
import numpy as np
import math

class LDAmodel(object):
	def __init__(self):
		self.n_features = 10000
		self.n_topics = 40
		self.n_top_words = 250
		self.tweetData = []
		self.IDs = []
		self.tf_vectorizer = CountVectorizer(max_df=0.85, min_df=2, max_features=self.n_features, stop_words = 'english')
		self.model = LatentDirichletAllocation(n_topics=self.n_topics, max_iter=35,
		                            learning_method='batch', learning_offset=50.,
		                            random_state=0)
		                     
	def print_top_words(self, n_words = 20):
		print("\nTopics in LDA model:")
		feature_names = self.tf_vectorizer.get_feature_names()
		
		for topic_idx, topic in enumerate(self.model.components_):
		    print("Topic #%d:" % topic_idx)
		    print(" ".join([feature_names[i] for i in topic.argsort()[:-n_words - 1:-1]]))
		    print("\n")

	def get_tweets(self):
		return (self.IDs, self.tweetData)
	
	def input(self, filePath = 'data.txt'):
		print ("Loading Data...")
		fdata = open(filePath).read()
		for lines in fdata.split('\n\n'):
			try:
				ID,dat = lines.split('\n')
				self.IDs.append(ID)
				self.tweetData.append(dat)
			except:
				pass
			
	
	def train(self):
		print("Extracting tf features for LDA...")		
		tf = self.tf_vectorizer.fit_transform(self.tweetData)
	
		print ("Fitting LDA models with tf features, n_features=%d..."% (self.n_features))
		t0 = int(time())
		self.model.fit(tf)
		t1 = int(time())
		print ("Completed in %d mins %d secs"%( (t1-t0)/60 , (t1-t0)%60))
	

	def label_tweets(self, data_samples = None):
		feature_names = self.tf_vectorizer.get_feature_names()
		topic_words = []
		
		if not data_samples	:
			data_samples = self.tweetData
		
		for topic in self.model.components_:
		   	topic_words.append([feature_names[i] for i in topic.argsort()[:-self.n_top_words - 1:-1]])
		   	
		print ("Classifying tweets...")
		   	
		##sum{(total features - i) * count} / sum(i)
		##then normalize
		probs = []
		zerocnt = 0
		denom = float(sum(range(1,len(topic_words[0]) + 1 )))
		
		t0 = int(time())
		for i,tweet in enumerate(data_samples):
			if not i % 1000:
				print (i)
			cnts = []
			for topic in topic_words:
				cnt = 0
				for rank,word in enumerate(topic):
					cnt += (len(topic) - rank) * tweet.count(word)
				cnts.append(cnt/denom)
				
			
			if sum(cnts) < 0.001:
				zerocnt +=1
				cnts = [1.0/len(topic_words)] * len(topic_words)
			else:
				cnts = [float(num)/(sum(cnts)) for num in cnts]
			probs.append(cnts)
			
		t1 = int(time())
		print ("Completed in %d mins %d secs"%( (t1-t0)/60 , (t1-t0)%60))
		print ("#undetermined tweets:", zerocnt)
		return probs
		
	def getCosineSimilarities(self, probList = None, outFile = "tweetCosineSimilarity.txt"):			
		def cosine_similarity(v1, v2):
			v1_u = v1 / np.linalg.norm(v1)
			v2_u = v2 / np.linalg.norm(v2)
			return np.dot(v1_u, v2_u)
		
		
		simDict = {}

		if not probList:
			probList = self.label_tweets()
		
		if outFile:
			of = open(outFile, "w")
		
		print ("Calculating Cosine Similarities...")
		t0 = int(time())
		for i in range(len(probList)):
			for j in range(i + 1, len(probList)):
				if not i % 1000 and j == i + 1:
					print (i)
					
				temp = simDict[(i,j)] = cosine_similarity(probList[i], probList[j])
				if outFile:
					of.write(self.IDs[i] + ", " + self.IDs[j] + ", " + str(temp) + "\n")
		if outFile:
			of.close()
		
		t1 = int(time())
		print ("Completed in %d mins %d secs"%( (t1-t0)/60 , (t1-t0)%60))

		return simDict
		
	

	def getSimilarityBetween(self, tweet1, tweet2):
		t1 = tweet1.split('\n')
		t2 = tweet2.split('\n')
		twList = [t1[1], t2[1]]
		
		out = self.label_tweets(twList)
		res = self.getCosineSimilarities(out, None)
		return res[(0,1)]


lda = LDAmodel()
#lda.input("New_dataset/all_data_with_hash.txt")
lda.input("/home/trishnendu/Graph_Lab/Term_project/Similarity Measure/similarity_score_jaccard_on_100_data_withash(mapped).txt(mapped)")
lda.train()
lda.print_top_words(15)
out = lda.getCosineSimilarities(outFile = "/home/trishnendu/Graph_Lab/Term_project/Similarity Measure/similarity_score_jaccard_on_lda_100_mapped.txt")


## Library needed : nltk, scipy, gensim, sklearn, json ##
## Files needed : stopwordfile, mappingfile ##
## Usage : This script takes the sample dataset and create similarity graph using word2vec_model ## 


import numpy as np
import scipy.spatial
from gensim.models import Word2Vec
np.seterr(divide='ignore', invalid='ignore')
from sklearn.cluster import KMeans

def avg_feature_vector(words, model, num_features, index2word_set):
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0

        for word in words:
            if word in index2word_set:
                nwords += 1
                featureVec = np.add(featureVec, model[word])
       	
       	if(nwords>0):
            featureVec = np.divide(featureVec, nwords)
        return featureVec

def create_vocab(sentences):
	vocab=[]
	for sentence in sentences:
		vocab.append(sentence.split())
	return vocab

def readdata(inputfile):
	tweets = {}
	infile = open(inputfile)
	
	inputdata = infile.read().split("\n\n")
	for data in inputdata:
		d = data.split("\n")
		if len(d) >= 2:	tweets[d[0]] = d[1]
	return tweets

def Word2vecsim(word2vec_model, index2word, nfeature, tweets, id1, id2):
	tweet1_terms = tweets[id1].split(" ")
	tweet2_terms = tweets[id2].split(" ")
	avg_vector1 = avg_feature_vector(tweet1_terms, model = word2vec_model, num_features = nfeature, index2word_set = index2word)
	avg_vector2 = avg_feature_vector(tweet2_terms, model = word2vec_model, num_features = nfeature, index2word_set = index2word)

	similarity = 1 - scipy.spatial.distance.cosine(avg_vector1, avg_vector2)

	return similarity

def Kmeansclustering(word2vec_model, index2word, nfeature, tweets, nclusters):
	X = []
	indexlist = list(tweets.keys())
	for index in indexlist:
		terms = tweets[index].split(" ")
		avg_vec = avg_feature_vector(terms, model = word2vec_model, num_features = nfeature, index2word_set = index2word)
		X.append(avg_vec)
	X = np.array(X)
	cluster = KMeans(nclusters)
	pred = cluster.fit_predict(X)
	res = [[] for i in range(nclusters)]
	for i in range(len(pred)):
		res[pred[i]].append(indexlist[i])
	outfilename = "/home/trishnendu/Graph_Lab/Term_project/Clustering/Test_clusters/Word2vec_clusterKmean8_1000feature_on_randomsample_100_withnohashstem(mapped).txt"
	outfile = open(outfilename,"w")
	for i in res:
		outfile.write(",".join(str(e) for e in i))
		outfile.write("\n")
	outfile.close()
	
if __name__ == '__main__':
	inputfile = "/home/trishnendu/Graph_Lab/Term_project/Dataset/Test_dataset/withnohash(mapped)/randomsample_100_withnohash(mapped).txt"
	tweets = readdata(inputfile)
	nfeature = 10000
	word2vec_model = Word2Vec(create_vocab(list(tweets.values())), size = nfeature, window = 5, min_count = 2, workers = 4)
	index2word = set(word2vec_model.index2word)
	Kmeansclustering(word2vec_model, index2word, nfeature, tweets, 8)
	'''ids = list(tweets.keys())
	for i in range(len(ids) - 1):
		for j in range(i + 1, len(ids)):
			print((i, j))
			similarity_score = Word2vecsim(word2vec_model, index2word, nfeature, tweets, ids[i], ids[j])
			if( similarity_score > 0):
				outfile.write(ids[i] + "," + ids[j] + "," + str(similarity_score) + "\n")
	outfile.close()
	'''

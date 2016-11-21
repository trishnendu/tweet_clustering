## Library needed : nltk, json ##
## Files needed : stopwordfile, mappingfile ##
## Usage : This script takes the raw tweet directory (tweets in json format) and cleans the tweet and generates sample dataset using random sampling ## 

import json, re, string, os, random
import nltk
from nltk.corpus import words
from nltk.stem.porter import *

def withhash(text):
	global stopwords
	urlremover=re.compile(r"(?:https?\://)\S+")
	puncremover = re.compile('[%s]' % re.escape(string.punctuation.replace('#','')))
	
	url_free_text=[]
	for term in init_text.split():
		url_free_text.append(urlremover.sub('',term))
	
	punctuation_free_text=puncremover.sub(''," ".join(str(e) for e in url_free_text))
	
	final_text=[]
	
	
	for term in punctuation_free_text.split(" "):
		term=term.lower()
		Flag=False
		if term not in stopwords:
			Flag=True
			for i in range(len(str(term))):
				if ord(term[i])>128:
					Flag=False
					break
		if Flag:	final_text.append(term)
	
	
	return " ".join(str(e) for e in final_text)

def withnohashstem(text):
	englishwords=set(words.words())
	stemmer = PorterStemmer()
	global stopwords
	urlremover=re.compile(r"(?:https?\://)\S+")
	puncremover = re.compile('[%s]' % re.escape(string.punctuation))
	
	url_free_text=[]
	for term in init_text.split():
		url_free_text.append(urlremover.sub('',term))
	
	punctuation_free_text=puncremover.sub(''," ".join(str(e) for e in url_free_text))
	
	final_text=[]
	
	
	for term in punctuation_free_text.split(" "):
		term=term.lower()
		Flag=False
		if term not in stopwords:
			Flag=True
			for i in range(len(str(term))):
				if ord(term[i])>128:
					Flag=False
					break
		if Flag:	
			if term in englishwords:	final_text.append(stemmer.stem(term))
			else:	final_text.append(term)
	
	return " ".join(str(e) for e in final_text)

def withnohash(text):			
	global stopwords
	urlremover=re.compile(r"(?:https?\://)\S+")
	puncremover = re.compile('[%s]' % re.escape(string.punctuation))

	url_free_text=[]
	for term in init_text.split():
		url_free_text.append(urlremover.sub('',term))
		
	punctuation_free_text=puncremover.sub(''," ".join(str(e) for e in url_free_text))
	
	final_text=[]
	
	for term in punctuation_free_text.split(" "):
		Flag=False
		term=term.lower()
		if term not in stopwords:
			Flag=True
			for i in range(len(str(term))):
				if ord(term[i])>128:
					Flag=False
					break
		if Flag:	final_text.append(term)
	
	return " ".join(str(e) for e in final_text)
	
	
def withonlyhash(text):
	global stopwords
	urlremover=re.compile(r"(?:https?\://)\S+")
	puncremover = re.compile('[%s]' % re.escape(string.punctuation.replace('#','')))
	
	url_free_text=[]
	for term in init_text.split():
		url_free_text.append(urlremover.sub('',term))
		
	punctuation_free_text=puncremover.sub(''," ".join(str(e) for e in url_free_text))
		
	final_text=[]
	for term in punctuation_free_text.split(" "):
		Flag=False
		term=term.lower()
		if term not in stopwords:
			Flag=True
			for i in range(len(str(term))):
				if ord(term[i])>128:
					Flag=False
					break
		if Flag and '#' in term:	final_text.append(term[term.index('#')+1:].lower())
	
	return " ".join(str(e) for e in final_text)
	
	
if __name__ == '__main__':
	outfile11 = open('/home/trishnendu/Graph_Lab/Term_project/Dataset/Test_dataset/complete(mapped)/complete_withash(mapped).txt','w')
	outfile12 = open('/home/trishnendu/Graph_Lab/Term_project/Dataset/Test_dataset/complete(mapped)/complete_withash(mapped)_ground_truth.txt','w')

	jsonldir = "/home/trishnendu/Graph_Lab/Term_project/Dataset/Raw_dataset/jsonl"
	mappingfile = open('/home/trishnendu/Graph_Lab/Term_project/Misc/index_id_map.txt').read() 
	stopwordfile=open('/home/trishnendu/Graph_Lab/Term_project/Misc/smart-stopwords').read()
	stopwords=set()
	indexidmap={}

	for stopword in stopwordfile.split("\n"):
		stopwords.add(stopword)

	for line in mappingfile.split("\n"):
		line = line.split(" ")
		if len(line) == 2:
			indexidmap[int(line[0])] = line[1]
					
	for filename in os.listdir(jsonldir):
		if ".json" in filename:
			data=open(jsonldir+"/"+filename).read().split("\n")
			samplesize = min(len(data)-1, 100)
			if (len(data)-1) >= samplesize:
				rsample = random.sample(range(len(data)-1), samplesize)		
				#rsample = [i for i in range(len(data)-1)]
				for i in range(len(data)-1):
					jo=json.loads(data[i])
					init_text=jo['text']
					if i in rsample:
						print(i)
						outfile11.write(str(indexidmap[jo['id']])+"\n"+withhash(init_text)+"\n\n")
						outfile12.write(str(indexidmap[jo['id']])+",")
				outfile12.write("\n")
					
	outfile11.close()
	outfile12.close()
	

import json,os

outfile = open("index_id_map.txt",'w')
jsonldir = "/home/trishnendu/Graph_Lab/Term_project/Dataset/Raw_dataset/jsonl"
cnt = 0
cwd = os.getcwd()
for filename in os.listdir(jsonldir):
	if ".json" in filename:
		data = open(filename).read().split("\n")
		for i in range(len(data) - 1):
			jo = json.loads(data[i])
			outfile.write(str(jo['id']) + " " + str(cnt) + "\n")
			cnt += 1	
outfile.close()

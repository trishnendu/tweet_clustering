def create_edge_list(edgelistfilename):
	edgelist = []
	for line in open(edgelistfilename).read().split("\n"):
		line = line.split(",")
		if (len(line) == 3):
			line[0] = int(line[0])
			line[1] = int(line[1])
			line[2] = float(line[2])
			edgelist.append(line)
	return edgelist

def create_adjmatrix(edglistfilename):
	edgelist = open(edgelistfilename).read()
	adj_matrix = {}
	vertex_set = set()
	for line in edgelist.split("\n"):
		line = line.split(",")
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

	return adj_matrix, vertex_set


def initial_partition(adj_matrix, vertex_set):				
	A = set()
	B = set()
	vertex_list = list(vertex_set)
	for i in range(len(vertex_set)):
		if i < 	len(vertex_set)/2:
			A.add(vertex_list[i])
		else:
			B.add(vertex_list[i])
	return A, B

def initial_partition1(adj_matrix, vertex_set, edgelistfilename):				
	A = set()
	B= set()
	N = len(vertex_set)
	vertex_list = list(vertex_set)
	edgelist = create_edge_list(edgelistfilename)
	edgelist = sorted(edgelist, key=lambda x:x[2])
	cnt = 0
	print("Preparing initial partition\n")
	for edge in edgelist:
		print((cnt,len(edgelist)))
		if len(A) >= N/2 or len(B) >= N/2:
			break
		else:
			if edge[0] not in A|B and edge[1] not in A|B:
				A.add(edge[0])	
				B.add(edge[1])
			if (edge[0] in A and edge[1] not in A):
				B.add(edge[1])
			if  (edge[1] in A and edge[0] not in A):
				B.add(edge[0])
			if (edge[0] in B and edge[1] not in B):
				A.add(edge[1])
			if (edge[1] in B and edge[0] not in B):
				A.add(edge[0])
		cnt +=1		
	#print(("test",A,B))
	A -= (A & B)
	
	if len(A) >= N/2:
		B = B | (vertex_set - A)
	elif len(B) >= N/2:
		A = A | (vertex_set - B)
		
	return A, B

		
def calculate_gain(adj_matrix, vertex_set, A, B):
	gain = {}
	for v in vertex_set:
		gain[v] = 0
		p_partition= set()
		o_partition= set()
		if v in A:	
			p_partition = A
			o_partition = B
		else:
			p_partition = B
			o_partition = A
		for u in adj_matrix[v]:
			if u in o_partition:
				gain[v] += adj_matrix[v][u]
			if u in p_partition:
				gain[v] -= adj_matrix[v][u]
	print((max(list(gain.values())),min(list(gain.values())))) 
	return gain 

def update_gain(gain, adj_matrix, A, B, a, b):
	for v in adj_matrix[a]:
		if v in A:
			gain[v] +=  adj_matrix[a][v]
		if v in B:
			gain[v] -=  adj_matrix[a][v]
	for v in adj_matrix[b]:
		if v in B:
			gain[v] +=  adj_matrix[b][v]
		if v in A:
			gain[v] -=  adj_matrix[b][v]
	#print((max(list(gain.values())),min(list(gain.values())))) 
	return gain 


#edgelistfilename = "/home/trishnendu/Graph_Lab/Term_project/Similarity Measure/similarity_score_jaccard_on_100_data_withash(mapped).txt(mapped)"
edgelistfilename = "/home/trishnendu/Graph_Lab/Term_project/Similarity Measure/test_edgelist"
#outfile = open("/home/trishnendu/Graph_Lab/Term_project/Similarity Measure/two_clusters",'w')
adj_matrix, vertex_set = create_adjmatrix(edgelistfilename)
#print(edgelistfile.split("\n")[0])
#print((len(A),len(B)))
A, B = initial_partition1(adj_matrix, vertex_set, edgelistfilename)
print((A, B))

itr = 0
while True:
	gain = calculate_gain(adj_matrix, vertex_set, A, B)
	print((max(list(gain.values())),min(list(gain.values())))) 

	gv = []
	av = []
	bv = []
	unmarkedA = A.copy()
	unmarkedB = B.copy()
	N = min(len(A), len(B))
	for i in range(N):
		print((itr,i,N))
		maxg = float("-inf")
		maxa = -1
		maxb = -1
		for a in unmarkedA:
			for b in unmarkedB:
				gab = gain[a] + gain[b]
				if b in adj_matrix[a]:
					gab -=  2 * adj_matrix[a][b]
				if gab > maxg:
					maxg = gab
					maxa = a
					maxb = b
		gv.append(maxg)
		av.append(maxa)
		bv.append(maxb)
		unmarkedA.remove(maxa)
		unmarkedB.remove(maxb)
		gain = update_gain(gain, adj_matrix, unmarkedA, unmarkedB, maxa, maxb)
	
	if(len(gv) <= 0):
		break	
	prefixgain = [gv[0]]
	for i in range(1, N):
		prefixgain.append(prefixgain[-1] + gv[i])
	g_max = max(prefixgain)
	if g_max < 0:	
		break
	#if itr > N:
	#	break
	k = prefixgain.index(g_max)
	for i in range(k+1):
		A.remove(av[i])
		B.remove(bv[i])
		A.add(bv[i])
		B.add(av[i])
	itr += 1

#print((len(A),len(B)))
print((A,B))	
#outfile.write(",".join(str(p) for p in A))
#outfile.write("\n")
#outfile.write(",".join(str(p) for p in B))
#outfile.close()

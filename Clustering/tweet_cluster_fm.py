def create_edge_list(edgelistfilename):
	edgelist = []
	cnt = 0
	data = open(edgelistfilename).read().split("\n")
	for line in data:
		line = line.split(",")
		line[0] = int(line[0])
		line[1] = int(line[1])
		line[2] = float(line[2])
		print((cnt,len(data)))
		edgelist.append(line)
		cnt += 1
	return edgelist

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
	#print("Preparing initial partition\n")
	for edge in edgelist:
		#print((cnt,len(edgelist)))
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

	A -= (A & B)

	if len(A) >= N/2:
		B = B | (vertex_set - A)
	elif len(B) >= N/2:
		A = A | (vertex_set - B)

	print(("init",len(A),len(B)))

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
	#print((max(list(gain.values())),min(list(gain.values()))))
	return gain


def update_gain(gain, adj_matrix, A, B, u, flag):
	if flag:
		for v in adj_matrix[u]:
			if v in A:
				gain[v] +=  adj_matrix[u][v]
			if v in B:
				gain[v] -=  adj_matrix[u][v]
	else:
		for v in adj_matrix[u]:
			if v in B:
				gain[v] +=  adj_matrix[u][v]
			if v in A:
				gain[v] -=  adj_matrix[u][v]
	#print((max(list(gain.values())),min(list(gain.values()))))
	return gain


def recursive_fm(adj_matrix, vertex_set, outfilename, curr_depth, max_depth):
	if curr_depth == max_depth:
		print(("Writing at depth ", curr_depth, len(vertex_set)))
		outfile = open(outfilename,'a')
		outfile.write(",".join(str(p) for p in vertex_set))
		outfile.write("\n")
		#outfile.write(",".join(str(p) for p in B))
		outfile.close()
		return

	A, B = initial_partition(adj_matrix, vertex_set)
	print(len(A),len(B))

	#print((max(list(gain.values())),min(list(gain.values()))))
	itr = 0
	while True:
		gain = calculate_gain(adj_matrix, vertex_set, A, B)
		print((max(list(gain.values())),min(list(gain.values()))))
		gva = []
		gvb = []
		av = []
		bv = []
		unmarkedA = A.copy()
		unmarkedB = B.copy()
		N = min(len(unmarkedA), len(unmarkedB))
		for i in range(N):
			#print((itr,i,N))
			maxg = float("-inf")
			maxa = -1

			for a in unmarkedA:
				if gain[a] > maxg:
					maxg = gain[a]
					maxa = a
			gva.append(maxg)
			av.append(maxa)
		#print((itr,i,"maxA",maxa,maxg))
			unmarkedA.remove(maxa)
			gain = update_gain(gain, adj_matrix, unmarkedA, unmarkedB, maxa, True)

			maxg = float("-inf")
			maxb = -1

			for b in unmarkedB:
				if gain[b] > maxg:
					maxg = gain[b]
					maxb = b
			gvb.append(maxg)
			bv.append(maxb)
			#print((itr,i,"maxB",maxb,maxg))
			unmarkedB.remove(maxb)
			gain = update_gain(gain, adj_matrix, unmarkedA, unmarkedB, maxb, False)

		#print(len(gvb))
		prefixgain = []
		if len(gva) > 0 and len(gvb) > 0:
			prefixgain = [gva[0] + gvb[0]] #- (2 * adj_matrix[av[0]][bv[0]])
			for i in range(1, min(len(gva),len(gvb))):
				if bv[i] in adj_matrix[av[i]]:
					prefixgain.append(prefixgain[-1] + gva[i] + gvb[i]) #- (2 * adj_matrix[av[i]][bv[i]])

		if prefixgain:
			g_max = max(prefixgain)
			if g_max <= 0:
				break
		else:
			break
		if itr > 100:
			break
		k = prefixgain.index(g_max)
		for i in range(k+1):
			A.remove(av[i])
			B.remove(bv[i])
			A.add(bv[i])
			B.add(av[i])
		print((curr_depth, itr, g_max))
		itr += 1

	recursive_fm(adj_matrix, A.copy(), outfilename, curr_depth + 1, max_depth)
	recursive_fm(adj_matrix, B.copy(), outfilename, curr_depth + 1, max_depth)


edgelistfilename = "/home/trishnendu/Graph_Lab/Term_project/Similarity_measure/Similarity_graphs/Lda_graph_on_randomsample_100_withnohashstem(mapped).txt"
#edgelistfilename = "/home/trishnendu/Graph_Lab/Term_project/Similarity Measure/test_edgelist"
outfilename = "/home/trishnendu/Graph_Lab/Term_project/Clustering/Test_clusters/Lda_clusterfm8_100itr_on_randomsample_100_withnohashstem(mapped).txt"
#edgelistfilename = '/mnt/data/Lucene_data/similarity_score_jaccard_on__complete_data_withash(mapped).txt'
#outfilename = "/home/trishnendu/Graph_Lab/Term_project/Similarity Measure/complete_data_clusters_100_jaccard"
adj_matrix, vertex_set = create_adjmatrix(edgelistfilename)
recursive_fm(adj_matrix, vertex_set, outfilename, 0, 3)
#print(edgelistfile.split("\n")[0])
#print((len(A),len(B)))


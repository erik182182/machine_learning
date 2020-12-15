import numpy as np
import networkx as nx

def connect(m, tree, rel):
    min = m[0][1]
    i_min, j_min = 0, 1
    for i in range(n):
        if rel[i] == 1:
            for j in range(n):
                if rel[j] == 0:
                    if min > m[i][j]:
                        min = m[i][j]
                        i_min, j_min = i, j
    tree[i_min][j_min] = m[i_min][j_min] = min
    tree[j_min][i_min] = m[j_min][i_min] = min
    rel[i_min] = rel[j_min] = 1

def draw_clusters(tree, n):
    G = nx.Graph(strict=False)
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if tree[i][j] != 0:
                G.add_edge(i,j, matrix=tree[i][j])
                G.add_edges_from([(i, j, {'matrix': tree[i][j]})])
                tree[i][j] = tree[j][i] = 0
    nx.draw_circular(G, with_labels=False)
    pos = nx.circular_layout(G)
    edge_labels = nx.get_edge_attributes(G,'matrix')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = edge_labels)

def cluster(k, tree, clust):
    clusters = []
    for i in range(n):
        for j in range(n):
            if tree[i][j] == 0:
                continue
            if len(clusters) == 0:
                clusters.append(i)
                clusters.append(j)
                tree[i][j] = tree[j][i] = 0
    m = clusters[0]
    old_m = -1
    while old_m != m:
        old_m = m
        for j in range(n):
            if tree[m][j] == 0:
                continue
            else:
                clusters.append(j)
                tree[m][j] = tree[j][m] = 0
                m = j
    m = clusters[1]
    old_m = -1
    while old_m != m:
        old_m = m
        for j in range(n):
            if tree[m][j] == 0:
                continue
            else:
                clusters.append(j)
                tree[m][j] = tree[j][m] = 0
                m = j
    for i in clusters:
        clust[i] = k



n, k = 7, 2
matrix = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j] = matrix[j][i] = np.random.randint(1, 100)

tree = [[0 for i in range(n)] for j in range(n)]

connection = np.zeros(n)
minim = matrix[0][1]
i_min, j_min = 0, 1
for i in range(n):
    for j in range(i + 1, n):
        if minim > matrix[i][j]:
            minim = matrix[i][j]
            i_min, j_min = i, j
tree[i_min][j_min] = matrix[i_min][j_min] = minim
tree[j_min][i_min] = matrix[j_min][i_min] = minim
connection[i_min] = connection[j_min] = 1


while 0 in connection:
    connect(matrix, tree, connection)

for i in range(k - 1):
    maxim = 0
    i_max, j_max = 0, 0
    for i in range(n):
        for j in range(i + 1, n):
            if tree[i][j] > maxim:
                maxim = tree[i][j]
                i_max, j_max = i, j
    tree[i_max][j_max] = tree[j_max][i_max] = 0

clust = np.zeros(n)
ot = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        ot[i][j] = tree[i][j]

for i in range(1, k):
    cluster(i, tree, clust)

draw_clusters(ot, n)

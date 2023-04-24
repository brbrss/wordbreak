import scipy.sparse.linalg
import filepickle
import numpy as np
import scipy.spatial
from helper.print_progress import print_progress
from helper.topheap import TopHeap

#dist_fp = 'spike/garbage/wdist.dump'


concentration = 5.0

neighbor_size = 5


def kernel(dotproduct):
    return np.exp(concentration*dotproduct)


def cluster(density: np.ndarray, nlist: dict[int, dict[int, float]]):
    '''
    Each cluster is represented by data point of highest density.


    density[i]: density at i
    dist[i][j]: cos dist between i,j, i.e. 1 - v_i dot v_j

    returns list where ret[i] is the index of highest density point in that cluster
    '''

    n = len(density)
    pre: list[int] = list(range(n))
    for i in range(n):
        a = density[i]
        best_j = i
        best_g = 0
        neighbor = nlist[i]

        for j in neighbor:
            b = density[j]
            if b > a:
                d = np.arccos(neighbor[j])
                g = (b-a)/d
                if g > best_g:
                    best_j = j
                    best_g = g
        pre[i] = best_j
    for i in range(n):
        parent = pre[i]
        while pre[parent] != parent:
            pre[i] = pre[parent]
            parent = pre[i]
    return pre


# def find_dist(word_embed_fp, dist_fp):
#     print('calculating distance')
#     c = filepickle.load(word_embed_fp)
#     nword = c.shape[0]
#     for i in range(nword):
#         c[i] /= np.linalg.norm(c[i])
#     dist = np.zeros(shape=(nword, nword))  # cos dist of words
#     for i in range(nword):
#         print_progress(i, nword)
#         for j in range(i+1, nword):
#             dist[i][j] = scipy.spatial.distance.cosine(c[i], c[j])
#             dist[j][i] = dist[i][j]
#     filepickle.dump(dist, dist_fp)


def kde(word_embed_fp, center_fp):
    c = filepickle.load(word_embed_fp)
    nword = c.shape[0]
    print('normalizing embedding')
    for i in range(nword):
        c[i] /= np.linalg.norm(c[i])
    print('calculating density')
    density = np.zeros(nword)
    neighbor: dict[int, dict[int, float]] = {}
    for i in range(nword):
        print_progress(i, nword)
        heap = TopHeap(neighbor_size)
        d = 0
        for j in range(nword):
            x = np.dot(c[i], c[j])
            if x == 0:
                print(i, j)
            heap.push(j, x)
            d += kernel(x)
        density[i] = d
        neighbor[i] = {heap.arr[t].k: heap.arr[t].v for t in range(len(heap))}

    print('performing clustering')
    center_list = cluster(density, neighbor)
    filepickle.dump(center_list, center_fp)

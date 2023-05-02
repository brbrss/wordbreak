from StatTool.sphere_em import SphereEm
import filepickle
import numpy as np
from helper import print_progress


ncluster = 256


def cluster(word_embed_fp, cluster_fp):
    print('clustering word')
    word = filepickle.load(word_embed_fp)

    nword, ndim = word.shape
    for i in range(nword):
        word[i] /= np.linalg.norm(word[i])

    em = SphereEm(word, ncluster)

    nrun = 20
    for i in range(nrun):
        print_progress.print_progress(i, nrun)
        em.update()
    zi = em.output()

    word_group = {}
    for i in range(nword):
        k = zi[i]
        if k not in word_group:
            word_group[k] = []
        word_group[k].append(i)

    filepickle.dump(word_group, cluster_fp)
    return

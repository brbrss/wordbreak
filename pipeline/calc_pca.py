import scipy.sparse.linalg
import filepickle
import numpy as np
import scipy.spatial


def calc_pca(reduced_matrix_fp,pca_dim, word_embed_fp):
    print('calculating svd')
    m = filepickle.load(reduced_matrix_fp)
    m = m.toarray()
    mean = m.mean(axis=1)
    m = m - mean[:, np.newaxis]
    u, s, v = scipy.sparse.linalg.svds(m, k=pca_dim)

    c = np.matmul(m, v.T)
    filepickle.dump(c, word_embed_fp)

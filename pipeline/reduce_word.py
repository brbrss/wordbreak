# calculate document frequency

import filepickle
import scipy.sparse
import numpy as np


def reduce_word(matrix_fp, word_fp, reduced_matrix_fp, reduced_word_fp):
    print('picking top n word for each doc')
    topn = 200
    m: scipy.sparse.spmatrix = filepickle.load(matrix_fp)
    nword, ndoc = m.shape
    mu = m > 0
    idf = -scipy.log(mu.sum(1)/ndoc)

    good_index = set()
    for i in range(ndoc):
        score = (m[:, i].toarray()*idf).transpose()[0]
        sorted = np.argsort(score)
        for wi in sorted[-topn:]:
            good_index.add(wi)
    print('filtering matrix')
    wlist = filepickle.load(word_fp)
    new_wlist = []
    new_nword = len(good_index)
    new_m = scipy.sparse.lil_matrix((new_nword, ndoc))
    for wi in range(new_nword):
        new_m[wi, :] = m[wi, :]
        new_wlist.append(wlist[wi])
    new_m = new_m.tocsc()
    filepickle.dump(new_wlist, reduced_word_fp)
    filepickle.dump(new_m, reduced_matrix_fp)

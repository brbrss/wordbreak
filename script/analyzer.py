import numpy as np
from StatTool.fast_seg import FastSeg
import filepickle
import scipy.sparse

np.seterr(all='raise')

def zscore(x0, n0, x1, n1):
    p = (x0+x1+0.01)/(n0+n1)
    m = p*n1
    return (x1-m)/np.sqrt(m)


class Analyzer:
    def __init__(self, cluster_fp, rword_fp) -> None:
        self.clu = filepickle.load(cluster_fp)
        self.wlist = filepickle.load(rword_fp)
        self.nword = len(self.wlist)
        self.nclu = len(self.clu)
        pass

    def iclu(self, i):
        for k in range(self.nclu):
            if i in self.clu[k]:
                return k
        return None

    def cludist(self, ar):
        res = np.zeros(self.nclu)
        for i in range(self.nword):
            clu_num = self.iclu(i)
            res[clu_num] += ar[i]
        return res

    def top_chi2(self, ar, base_weight):
        base_sum = sum(base_weight)
        n1 = sum(ar)
        if n1 == 0:
            return []
        lenv = len(base_weight)
        carr = [zscore(base_weight[k], base_sum, ar[k], n1) for k in range(lenv)]
        st = np.argsort(carr)
        return [t for t in reversed(st)]

    def top_cat(self, ar, base_clu):
        '''
        ar: array of word occurence shape==(nword)'''
        c = self.cludist(ar)
        return self.top_chi2(c, base_clu+100)

    def top_word(self, ar, base_word):
        st = self.top_chi2(ar, base_word+100)
        return [self.wlist[i] for i in st]

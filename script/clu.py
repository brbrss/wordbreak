'''for viewing clusters'''


import filepickle
import numpy as np
import scipy.sparse.linalg
import scipy.spatial

wlist = filepickle.load('output/rword.dump')
c = filepickle.load('output/embed.dump')
clu = filepickle.load('output/clu.dump')
m = filepickle.load('output/cludir.d')


wclu = [[wlist[i] for i in clu[k]] for k in range(max(clu.keys())+1)]
wlen = [len(t) for t in wclu]
nword = len(wlist)


def _get(v, n=100):
    d = np.zeros(nword)
    for j in range(nword):
        w2 = c[j]
        d[j] = scipy.spatial.distance.cosine(v, w2)
    sorted = np.argsort(d)
    return [wlist[j] for j in sorted][:n]

def getcen(k,n=100):
    v = m[k]
    d = []
    for j in clu[k]:
        w2 = c[j]
        item = j, scipy.spatial.distance.cosine(v, w2)
        d.append(item)
    d.sort(key=lambda t:t[1])
    return [wlist[j] for j,v in d][:n]

def get(word, n=100):
    '''top n words in cluster, returns words closest to center of cluster'''
    i = wlist.index(word)
    w1 = c[i]
    return _get(w1)

def inclu(w):
    k = wlist.index(w)
    for i in range(len(clu)):
        if k in clu[i]:
            return i
    return -1

#cen = [getcen(k, 10) for k in range(len(clu))]



def clurow(i):
    return str(i).ljust(5) +' '+ str(len(clu[i])).ljust(5) +'   ' +' '.join([repr(s)[1:-1] for s in getcen(i,10)])+'\n'

with open('output/show/clu.csv','w',encoding='utf-8') as f:
    flines = [clurow(i) for i in range(len(clu))]
    f.writelines(flines)

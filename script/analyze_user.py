from collections import Counter
import filepickle
import numpy as np
import json

fp = 'output/user_count.d'
data = filepickle.load(fp)
wlist = filepickle.load('output/rword.dump')
m = filepickle.load('output/rmatrix.dump')
clu = filepickle.load('output/clu.dump')

m = m.toarray()

wc = [m[i].sum() for i in range(m.shape[0])]
total = sum(wc)
arr = data.toarray()
nuser = arr.shape[0]
nword = len(wlist)
nclu = len(clu)
ulen = [sum(t) for t in arr]


def klist(k):
    return {wlist[i]: arr[k][i] for i in range(nword) if arr[k][i]}


def iclu(i):
    for k in range(len(clu)):
        if i in clu[k]:
            return k
    return None


def cludist(ar):
    res = Counter()
    for i in range(nword):
        clu_num = iclu(i)
        if ar[i]:
            res[clu_num] += ar[i]
    return res


base_weight = cludist(wc)
base_sum = base_weight.total()


def chi2(n, ntotal, p):
    return np.square(n-p*ntotal)/(p*ntotal)


def user_topw(k):
    s2 = sum(arr[k])
    if s2 == 0:
        return []
    x2 = np.zeros(nword)
    for i in range(nword):
        p = wc[i]/total
        x2[i] = s2*p - arr[k][i]/np.sqrt(s2*p)
    st = np.argsort(x2)
    return [wlist[i] for i in st]


def user_topc(i):
    u_clu = cludist(arr[i])
    utotal = u_clu.total()
    if utotal == 0:
        return []
    carr = [chi2(u_clu[k], utotal, base_weight[k]/base_sum)
            for k in range(nclu)]
    iar = np.argsort(carr)
    iar = [t for t in reversed(iar)]
    return iar


output = {}
for u in range(nuser):
    userlen = sum(arr[u])
    if userlen<1000:
        continue
    print('processing user', u)
    uclu = [int(_i) for _i in user_topc(u)]
    uw = user_topw(u)[:100]
    item = {'clu': uclu, 'word': uw, 'len': userlen}
    output[u] = item

with open('output/show/user.json', 'w', encoding='utf-8') as f:
    json.dump(output, f)

print('analyze_user end')

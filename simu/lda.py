from StatTool.ldavi import Ldavi
import numpy as np
import scipy.sparse

np.random.seed(123)

nword = 64
ndoc = 200
ncluster = 5

wt = np.random.dirichlet([0.1]*nword, ncluster)
data = np.zeros((nword, ndoc))

td = np.random.dirichlet([1]*ncluster, ndoc)
td[0] = [1, 0, 0, 0, 0]
td[1] = [0, 1, 0, 0, 0]
td[2] = [0, 0, 1, 0, 0]
td[3] = [0, 0, 0, 1, 0]
td[4] = [0, 0, 0, 0, 1]
for i in range(ndoc):
    lendoc = np.random.randint(low=400, high=5000)
    for k in range(ncluster):
        data[:, i] += np.random.multinomial(lendoc*td[i][k], wt[k])


nclu = 5
data = scipy.sparse.csr_matrix(data)

m = data.toarray()
mean = m.mean(axis=1)
m = m - mean[:, np.newaxis]
u, s, v = scipy.sparse.linalg.svds(m, k=ncluster)

c = np.matmul(m, v.T)

lda = Ldavi(data, nclu)
lda.nu=np.ones(shape=lda.nu.shape)*2000

itnum = 50
for i in range(40):
    itnum = lda.update_random(itnum)
    print(lda.nu[0])

# for i in range(50):
#     lda.update()
#     print(lda.nu[0])

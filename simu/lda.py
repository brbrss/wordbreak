from StatTool.ldavi import Ldavi
import numpy as np
import scipy.sparse

nword = 64
ndoc = 200
ncluster = 5

wt = np.random.dirichlet([0.1]*nword, ncluster)
data = np.zeros((nword, ndoc))

td = np.random.dirichlet([1]*ncluster,ndoc)
td[0]=[1,0,0,0,0]
td[1]=[0,1,0,0,0]
for i in range(ndoc):
    lendoc = np.random.randint(low=400,high=5000)
    for k in range(ncluster):
        data[:, i] += np.random.multinomial(lendoc*td[i][k], wt[k])


nclu = 5
data = scipy.sparse.csr_matrix(data)
lda = Ldavi(data,nclu)
for i in range(40):
    lda.update()
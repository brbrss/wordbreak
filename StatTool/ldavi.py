import numpy as np

import scipy.special
import scipy.sparse


class Ldavi:
    def __init__(self, data: scipy.sparse.spmatrix, ncluster: int):
        nword, ndoc = data.shape  # ?
        self.x: scipy.sparse.spmatrix = data.transpose()
        self.ncluster = ncluster
        self.nword: int = nword
        self.ndoc: int = ndoc

        self.nu_prior = 1.0
        self.beta_prior = 1.0
        # n[i][k] = dirichlet param of P(topic k|doc i)
        self.nu = np.random.uniform(low=1, high=10, size=(self.ndoc, ncluster))
        # beta[n][k] = dirichlet param of P(word n|cluster k)
        self.beta = np.random.dirichlet([1]*nword, size=ncluster)*nword
        self.beta_copy = self._create_beta_array()

        # auxilliary
        self.nu_di = np.zeros(ndoc)
        self.beta_di = np.zeros(nword)
        return

    def _init_auxiliary(self):
        self.beta_copy = self._create_beta_array()
        self.nu_di = self._create_nu_di()
        self.beta_di = self._create_beta_di()

    def _create_nu_di(self):
        return scipy.special.digamma(np.sum(self.nu, axis=1))

    def _create_beta_di(self):
        return scipy.special.digamma(np.sum(self.beta, axis=1))

    def _create_beta_array(self):
        return np.full(
            shape=self.beta.shape, fill_value=self.beta_prior)

    def _doc(self, i):
        return self.x[i].toarray()[0]

    def update(self):
        self._init_auxiliary()
        for i in range(self.ndoc):
            self.update_doc(i)
        self.beta = self.beta_copy
        pass

    def update_doc(self, i):
        '''doc i'''
        # doc[n] = count of word n in doc i
        doc = self._doc(i)
        z = self.update_z(i, doc)
        self.update_nu(i, z, doc)
        self.update_beta(i, z, doc)

    def update_z(self, i, doc):
        # z[n][k] = P(z=k|count word_n at doc)
        def get_logz(n, k):
            elogp_pi = scipy.special.digamma(self.nu[i][k])-self.nu_di[i]
            elogp_b = scipy.special.digamma(self.beta[k][n])-self.beta_di[k]
            return elogp_pi+elogp_b

        # q(cluster|word)
        shape = (self.nword, self.ncluster)
        z = np.zeros(shape=shape)
        #z = np.fromfunction(get_z, shape, dtype=int)
        logz = np.zeros(self.ncluster)
        for n in range(self.nword):
            if doc[n] > 0:
                for k in range(self.ncluster):
                    logz[k] = get_logz(n, k)
                m = max(logz)
                z[n] = np.exp(logz-m)
                z[n] /= sum(z[n])

        return z

    def update_nu(self, i, z, doc):
        # doc[n] = count word n
        for k in range(self.ncluster):
            self.nu[i][k] = self.nu_prior+sum(doc*z[:, k])

    def update_beta(self, i, z, doc):
        t = doc[:, None]*z  # t[n][k]
        self.beta_copy += t.T

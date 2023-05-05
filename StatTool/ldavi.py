import numpy as np

import scipy.special
import scipy.sparse
from helper.print_progress import print_progress


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
        self.elogp_nu = np.zeros(self.nu.shape)
        self.elogp_beta = np.zeros(self.beta.shape)
        return

    def _init_auxiliary(self):
        self.beta_copy = self._create_beta_array()
        # self._create_nu_di()
        self._create_beta_di()

    def _create_nu_di(self, i):
        di_total = scipy.special.digamma(np.sum(self.nu[i]))
        elogp_nu = scipy.special.digamma(self.nu[i])-di_total
        return elogp_nu

    def _create_beta_di(self):
        di_total = scipy.special.digamma(np.sum(self.beta, axis=1))
        self.elogp_beta = scipy.special.digamma(self.beta)-di_total[:, None]

    def _create_beta_array(self):
        return np.full(
            shape=self.beta.shape, fill_value=0.0)

    def _doc(self, i):
        return self.x[i].toarray()[0]

    def update(self):
        self._init_auxiliary()
        for i in range(self.ndoc):
            #print_progress(i, self.ndoc)
            self.update_doc(i)
        self.beta = self.beta_copy
        pass

    def update_random(self, itnum):
        doc_list = np.random.permutation(self.ndoc)
        BATCH_SIZE = 100
        counter = 0
        total_word = self.x.sum()
        word_count = 0
        self._init_auxiliary()
        total_counter = 0
        for i in doc_list:
            print_progress(total_counter, self.ndoc)
            total_counter += 1
            self.update_doc(i)
            doc = self._doc(i)
            word_count += sum(doc)
            counter += 1
            if counter >= BATCH_SIZE:
                counter = 0
                s = total_word/word_count
                alpha = 1/itnum
                self.beta = (1-alpha)*self.beta + alpha * s * \
                    (self.beta_copy+self.beta_prior)
                itnum += 1
                self._init_auxiliary()
        s = total_word/word_count
        alpha = 1/itnum
        self.beta = (1-alpha)*self.beta + alpha * s*self.beta_copy
        itnum += 1
        self._init_auxiliary()
        return itnum

    def update_doc(self, i):
        '''doc i'''
        # doc[n] = count of word n in doc i
        doc = self._doc(i)
        z = self.update_z(i, doc)
        self.update_nu(i, z, doc)
        self.update_beta(i, z, doc)

    def update_z(self, i, doc):
        # z[n][k] = P(z=k|count word_n at doc)
        elogp_nu = self._create_nu_di(i)

        def get_logz(n, k):
            return elogp_nu[k]+self.elogp_beta[k, n]

        # q(cluster|word)
        shape = (self.nword, self.ncluster)
        z = np.zeros(shape=shape)

        logz = np.fromfunction(
            get_logz, [self.nword, self.ncluster], dtype=int)
        for n in range(self.nword):
            if doc[n] > 0:
                m = max(logz[n])
                z[n] = np.exp(logz[n]-m)
                z[n] /= sum(z[n])

        return z

    def update_nu(self, i, z, doc):
        # doc[n] = count word n
        self.nu[i] = self.nu_prior+sum(doc[:, None]*z)

    def update_beta(self, i, z, doc):
        t = doc[:, None]*z  # t[n][k]
        self.beta_copy += t.T

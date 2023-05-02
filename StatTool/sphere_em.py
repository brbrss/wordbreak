import numpy as np

import scipy.special



def rand_uv(nsize, ndim):
    shape = [nsize, ndim]
    v = np.random.normal(0, 1, shape)
    n = np.linalg.norm(v, axis=1)[:, np.newaxis]
    v /= n
    return v


def a(ndim, kappa):
    '''normalizer coefficient for von mises fisher'''
    v = ndim/2
    _a = np.power(kappa, v-1)
    _b = np.power(2*np.pi, v)
    # modified Bessel function of the first kind at order
    _c = scipy.special.iv(v-1, kappa)
    return _a/(_b*_c)





class SphereEm:
    def __init__(self, data, k):
        ndata, ndim = data.shape
        self.ndim = ndim
        self.data = data
        self.n = ndata  # num data
        self.k = k  # num cluster
        self.prior = np.ones(k)*0.01  # prior of dirichlet
        self.pa = np.ones(k)*0.01  # param of dirichlet
        self.z = np.zeros(shape=(self.n, k))
        for i in range(self.n):
            t = np.random.choice(k)
            self.z[i][t] = 1

        # cluster parameter
        self.m = rand_uv(k, ndim)  # direction
        self.kappa = np.ones(k)
        pass

    def logpdf(self, x, k):
        normalizer = a(self.ndim, self.kappa[k])
        d = np.dot(x, self.m[k])
        return self.kappa[k] * d + np.log(normalizer)

    def update_z(self):
        a0 = sum(self.pa)
        di0 = scipy.special.digamma(a0)
        for i in range(self.k):
            E_log_p = scipy.special.digamma(self.pa[i])-di0
            normalizer = a(self.ndim, self.kappa[i])
            logp = self.logpdf(self.data, i)
            self.z[:, i] = np.exp(logp+E_log_p)
        ns = np.sum(self.z, axis=1)
        for i in range(self.n):
            self.z[i] /= ns[i]

    def update_p(self):
        self.pa = self.prior + np.sum(self.z, axis=0)

    def update_eta(self):
        for i in range(self.k):
            clu_n = sum(self.z[:, i])
            x_sum = sum(self.data * self.z[:, i][:, np.newaxis])
            if clu_n == 0:
                continue
            mu = x_sum/clu_n
            r = np.linalg.norm(mu, axis=0)
            v = mu/r
            self.m[i] = v
            a = 10
            estk = r*(self.ndim-r*r)/(1.001-r*r)
            # limit range of kappa so normalizer is numerically stable
            self.kappa[i] = min((estk*clu_n+1*a)/(a+clu_n), 150)
            #self.kappa[i] = 1/(0.01+r)

    def update(self):
        self.update_eta()
        self.update_p()
        self.update_z()

    def output(self):
        zi = np.argmax(self.z, axis=1)
        return zi


import itertools


class LayerDict(object):
    def __init__(self):
        self.L = [{}]

    def __getitem__(self, k):
        try:
            return self.L[k]
        except IndexError:
            return None
        return None

    def __len__(self):
        return len(self.L)

    def __iter__(self):
        return self.L.__iter__()

    def get(self, k, s):
        try:
            return self.L[k][s]
        except KeyError:
            return 0
        except IndexError:
            return 0
        return None

    def append(self, d):
        self.L.append(d)

    def words(self):
        return itertools.chain.from_iterable(self.L)

    def search_has(self, c):
        result = {}
        for d in self.L:
            for k in d.keys():
                if k.find(c)+1:
                    result[k] = d[k]

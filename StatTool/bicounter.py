from collections import Counter


class Bicounter():
    def __init__(self):
        self._d = {}

    def inc(self, w1, w2, n=1):
        if w1 not in self._d:
            self._d[w1] = Counter()
        self._d[w1][w2] += n

    def dec(self, w1, w2, n=1):
        self._d[w1][w2] -= n

    def clear(self):
        self._d.clear()

    def get(self, w1, w2):
        if w1 not in self._d:
            return 0
        return self._d[w1][w2]

    def __len__(self):
        return len(self._d)

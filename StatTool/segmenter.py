import numpy as np
from StatTool.trie import Trie, match_offset
from collections import Counter


class Segmenter:
    def __init__(self, data):
        self.data: list[str] = data
        # word break vector
        self.b = [np.ones(shape=len(s), dtype=np.bool_) for s in self.data]
        self.temperature = 2
        self.word_count = Counter()
        self.nword = 0

    def from_trie(self, trie: Trie):
        for i in range(len(self.data)):
            s = self.data[i]
            tlist = match_offset(s, trie)
            for a, b in tlist:
                for k in range(a+1, b):
                    self.b[i][k] = 0
        return

    def repr(self, i):
        b = self.b[i]
        s = self.data[i]
        res = []
        start = 0
        end = len(s)
        for k in range(1, len(b)):
            if b[k]:
                end = k
                res.append(s[start:end])
                start = k
        res.append(s[start:])
        return res

    def init_count(self):
        for i in range(len(self.data)):
            start = 0
            s = self.data[i]
            b = self.b[i]
            for k in range(1, len(b)):
                if b[k]:
                    word = s[start:k]
                    self.word_count[word] += 1
                    self.nword += 1
                    start = k
            if start != len(b):
                word = s[start:]
                self.word_count[word] += 1
                self.nword += 1
        return

    def anneal(self):
        pass

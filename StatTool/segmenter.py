import math
import numpy as np
from StatTool.trie import Trie, match_offset
from collections import Counter
import random


def next_on(b, k):
    for kk in range(k+1, len(b)):
        if b[kk]:
            return kk
    return len(b)


def count_char(data):
    s = set()
    for line in data:
        for c in line:
            s.add(c)
    return len(s)


class Segmenter:
    def __init__(self, data: list[str]):
        self.data: list[str] = data
        # word break vector
        self.b = [np.ones(shape=len(s), dtype=np.bool_) for s in self.data]
        self.temperature = 1
        self.word_count = Counter()
        self.nword = 0
        self.TAU = 0.3
        self.ALPHA = 5000
        self.nchar = count_char(data)
        self.nchanged = 0

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
        self.nchanged = 0
        self.word_count.clear()
        self.nword = 0
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

    def intrinsic_prob(self, w):
        n = len(w)
        return math.pow(1-self.TAU, n-1)*self.TAU*math.pow(1/self.nchar, n)

    def prob(self, w):
        nw = self.word_count[w]
        pw = self.intrinsic_prob(w)
        return (nw+self.ALPHA*pw)/(self.nword+self.ALPHA)

    def turn_on(self, w1, w2, w):
        self.word_count[w] -= 1
        self.word_count[w1] += 1
        self.word_count[w2] += 1
        self.nword += 1

    def turn_off(self, w1, w2, w):
        self.word_count[w] += 1
        self.word_count[w1] -= 1
        self.word_count[w2] -= 1
        self.nword -= 1

    def sample(self, p0, p1):
        if self.temperature == 0:
            return p1 > p0
        t = 1/self.temperature
        p0 = math.pow(p0, t)
        p1 = math.pow(p1, t)
        total = p0+p1
        d = random.random()
        return d*total > p0

    def gibbs(self):
        self.init_count()
        for i in range(len(self.data)):
            self._anneal(i)
        return

    def _anneal(self, i: int):
        '''optimize word breaking for text entry at i'''
        s = self.data[i]
        b = self.b[i]
        front = 0
        start = 0
        back = 0
        w = s[front:back]
        for k in range(1, len(b)):
            if k >= back:
                back = next_on(b, k)
                w = s[front:back]
            w1 = s[front:k]
            w2 = s[k:back]
            p1 = self.prob(w1)*self.prob(w2)
            p0 = self.prob(w)
            on = self.sample(p0, p1)
            self.nchanged += int(b[k] == on)
            b[k] = on
            if b[k]:
                front = k
                w = s[front:back]
        if start != len(b):
            word = s[start:]
            self.word_count[word] += 1
            self.nword += 1
        return

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

    def num_unique(self):
        return len(self.word_count)

    def num_word(self):
        return self.nword

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

    def prob(self, w, w_sub, n_sub):
        ''' 
        unigram probability P(w|text)

        w_sub: correction of word count
        n_sub: correction of total count
        '''
        nw = self.word_count[w]
        pw = self.intrinsic_prob(w)
        nw = nw - w_sub
        nt = self.nword - n_sub
        return (nw+self.ALPHA*pw)/(nt+self.ALPHA)

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



    def _anneal(self, i: int):
        '''optimize word breaking for text entry at i'''
        s = self.data[i]
        b = self.b[i]
        front = 0

        back = 0
        w = s[front:back]
        for k in range(1, len(b)):
            if k >= back:
                back = next_on(b, k)
                w = s[front:back]
            w1 = s[front:k]
            w2 = s[k:back]
            cur_on = b[k]
            n_sub = cur_on+1
            p1 = self.prob(w1, cur_on, n_sub) * \
                self.prob(w2, cur_on-int(w1 == w2), n_sub)
            p0 = self.prob(w, 1-cur_on, n_sub)
            on = self.sample(p0, p1)
            self.nchanged += int(b[k] == on)
            if b[k] and not on:
                self.turn_off(w1, w2, w)
            elif not b[k] and on:
                self.turn_on(w1, w2, w)
            b[k] = on
            if b[k]:
                front = k
                w = s[front:back]
        return

    def show_info(self):
        n = len(self.word_count)
        print('words: ', self.nword)
        print('unique: ', n)
        print('nchanged: ',self.nchanged)
        
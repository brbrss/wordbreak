from collections import Counter
from StatTool.bicounter import Bicounter
from StatTool.segmenter import Segmenter, count_char, next_on
import numpy as np


class Biseg(Segmenter):
    '''bigram segmenter'''

    def __init__(self, data: list[str]):
        self.data = data
        # word break vector
        self.b = [np.ones(shape=len(s), dtype=np.bool_) for s in self.data]

        self.temperature = 1
        self.TAU = 0.3
        self.ALPHA = 5000
        self.ALPHA_1 = 100

        self.word_count = Counter()
        self.bigram = Bicounter()
        self.nchar = count_char(data)+1  # plus empty str
        self.nword = 0

        self.npre = Counter()
        self.nchanged = 0
        pass

    def num_unique(self):
        return len(self.bigram)

    def num_word(self):
        return self.nword

    def init_count(self):
        self.nchanged = 0
        self.nword = 0
        self.bigram.clear()

        for i in range(len(self.data)):
            start = 0
            s = self.data[i]
            #n = self.data[i][1]
            b = self.b[i]
            pre = ''
            for k in range(1, len(b)):
                if b[k]:
                    word = s[start:k]
                    self.bigram.inc(pre, word, 1)
                    self.npre[pre] += 1
                    self.word_count[word] += 1
                    self.nword += 1
                    pre = word
                    start = k
            if start != len(b):
                word = s[start:]
                self.bigram.inc(pre, word, 1)
                self.npre[pre] += 1
                self.word_count[word] += 1
                self.nword += 1

            self.bigram.inc(pre, '', 1)
        return

    def con_prob(self, w1, w2):
        '''
        P(w2|w1,text)
        '''
        nw = self.bigram.get(w1, w2)
        pw = self.prob(w2)
        nw = max(0, nw-1)
        nt = max(0, self.npre[w1]-1)
        return (nw+self.ALPHA_1*pw)/(nt+self.ALPHA_1)

    def intrinsic_prob(self, w):
        n = len(w)
        return pow(1-self.TAU, n)*self.TAU*pow(1/self.nchar, n)

    def _anneal(self, i: int):
        '''optimize word breaking for text entry at i'''
        s = self.data[i]
        b = self.b[i]
        front = 0
        back = 0
        back2 = next_on(b, 0)
        pre = ''
        post = s[back:back2]
        w = s[front:back]
        for k in range(1, len(b)):
            if k >= back:
                back = back2
                back2 = next_on(b, back2)
                post = s[back:back2]
                w = s[front:back]
            w1 = s[front:k]
            w2 = s[k:back]
            p1 = self.con_prob(pre, w1)*self.con_prob(w1,
                                                      w2)*self.con_prob(w2, post)
            p0 = self.con_prob(pre, w)*self.con_prob(w, post)
            on = self.sample(p0, p1)
            self.nchanged += int(b[k] == on)
            b[k] = on
            if b[k]:
                front = k
                w = s[front:back]
        return

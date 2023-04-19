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

        #self.npre = Counter()
        self.nchanged = 0
        pass

    def num_unique(self):
        return len([w for w in self.word_count if self.word_count[w]])

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
            word = ''
            for k in range(1, len(b)):
                if b[k]:
                    word = s[start:k]
                    self.bigram.inc(pre, word, 1)
                    self.word_count[word] += 1
                    self.nword += 1
                    pre = word
                    start = k
            if start != len(b):
                word = s[start:]
                self.bigram.inc(pre, word, 1)
                self.word_count[word] += 1
                self.nword += 1

            self.bigram.inc(word, '', 1)
        return

    def con_prob(self, w1, w2, w_sub, n_sub):
        '''
        P(w2|w1,text)
        '''
        nw = self.bigram.get(w1, w2)
        pw = self.prob(w2, w_sub, n_sub+1)
        nw = nw - w_sub
        nt = self.word_count[w1]-n_sub
        result = (nw+self.ALPHA_1*pw)/(nt+self.ALPHA_1)
        # if result<0:
        #     raise ValueError('<0')
        return result

    def intrinsic_prob(self, w):
        n = len(w)
        return pow(1-self.TAU, n)*self.TAU*pow(1/self.nchar, n)

    def turn_on(self, w1, w2, w, pre, post):
        self.word_count[w] -= 1
        self.word_count[w1] += 1
        self.word_count[w2] += 1
        self.bigram.dec(pre, w)
        self.bigram.dec(w, post)
        self.bigram.inc(pre, w1)
        self.bigram.inc(w1, w2)
        self.bigram.inc(w2, post)
        self.nword += 1

    def turn_off(self, w1, w2, w, pre, post):
        self.word_count[w] += 1
        self.word_count[w1] -= 1
        self.word_count[w2] -= 1
        self.bigram.inc(pre, w)
        self.bigram.inc(w, post)
        self.bigram.dec(pre, w1)
        self.bigram.dec(w1, w2)
        self.bigram.dec(w2, post)
        self.nword -= 1

    def _anneal(self, i: int):
        '''optimize word breaking for text entry at i'''
        s = self.data[i]
        b = self.b[i]
        front = 0
        back = next_on(b, 0)
        back2 = next_on(b, back)
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

            cur_on = b[k]
            # remove current segment in counting for prob calc
            # if a-x-y-b remove a-x,x-y,y-b
            # if a-xy-b remove a-xy,xy-b
            # for a-x n_sub=1, w_sub =cur_on
            # for x-y n_sub=cur_on, w_sub=cur_on
            # for y-b n_sub = cur_on, w_sub = cur_on
            # for a-xy n_sub=1, w_sub=1-cur_on
            # for xy-b n_sub=1-cur_on, w_sub = 1-cur_on
            p1_pre = self.con_prob(pre, w1, cur_on, 1)
            p1_mid = self.con_prob(w1, w2, cur_on, cur_on)
            p1_post = self.con_prob(w2, post, cur_on, cur_on)
            p0_pre = self.con_prob(pre, w, 1-cur_on, 1)
            p0_post = self.con_prob(w, post, 1-cur_on, 1-cur_on)

            p1 = p1_pre*p1_mid*p1_post
            p0 = p0_pre*p0_post
            on = self.sample(p0, p1)
            self.nchanged += int(b[k] == on)
            if b[k] and not on:
                self.turn_off(w1, w2, w, pre, post)
            elif not b[k] and on:
                self.turn_on(w1, w2, w, pre, post)
            b[k] = on
            b[k] = on
            if b[k]:
                pre = s[front:k]
                front = k
                w = s[front:back]
        return

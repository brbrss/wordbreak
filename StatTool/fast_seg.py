from StatTool.segmenter import Segmenter, next_on


class FastSeg(Segmenter):
    def __init__(self, data):
        super().__init__(data)

    def prob(self, w):
        ''' 
        unigram probability P(w|text)
        '''
        nw = self.word_count[w]
        pw = self.intrinsic_prob(w)
        nt = self.nword
        return (nw+self.ALPHA*pw)/(nt+self.ALPHA)

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
            p1 = self.prob(w1) * self.prob(w2)
            p0 = self.prob(w)
            on = self.sample(p0, p1)
            self.nchanged += int(b[k] == on)

            b[k] = on
            if b[k]:
                front = k
                w = s[front:back]
        return

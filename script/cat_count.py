import numpy as np
from StatTool.fast_seg import FastSeg
import filepickle




class CatCount:
    def __init__(self, data_fp, reduced_word_fp, break_fp):
        self.data = filepickle.load(data_fp)
        self.wlist = filepickle.load(reduced_word_fp)
        self.b = filepickle.load(break_fp)
        self.nword = len(self.wlist)

        self.ncat = 0
        pass

    def category_id(t, p):
        pass

    def category_count(self):
        word_index = {self.wlist[i]: i for i in range(self.nword)}
        shape = (self.ncat, self.nword)
        result = np.zeros(shape)
        p_pos = 0  # running count of post
        data = self.data
        for tid in data:
            t = data[tid]
            for p in t.post_list:
                aid = self.category_id(t, p)
                if aid is not None:
                    seg = FastSeg([p.content])
                    seg.b = [self.b[p_pos]]
                    seg.init_count()
                    for w in seg.word_count:
                        try:
                            w_pos = word_index[w]
                            result[aid, w_pos] += seg.word_count[w]
                        except KeyError:
                            pass
                p_pos += 1
        return result

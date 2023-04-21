
import filepickle
from StatTool.fast_seg import FastSeg
import numpy as np
from ParseTool import model




def seg_matrix(data_fp, break_fp, word_fp, matrix_fp):
    data: dict[int, model.ThreadModel] = filepickle.load(data_fp)
    wlist = filepickle.load(word_fp)
    nword = len(wlist)
    len_data = len(data)
    word_matrix = np.zeros(shape=(nword, len_data))  # word, doc shape
    word_index = {wlist[i]: i for i in range(nword)}
    b = filepickle.load(break_fp)
    p_pos = 0
    t_pos = 0
    for tid in range(len(data)):
        t = data[tid]
        d = []
        plist = []
        for p in t.post_list:
            d.append(p.content)
            plist.append(p_pos)
            p_pos += 1
        seg = FastSeg(d)
        seg.b = [b[p] for p in plist]
        seg.init_count()
        for w in seg.word_count:
            if w in word_index:
                w_pos = word_index[w]
                word_matrix[w_pos][t_pos]
        t_pos += 1
    filepickle.dump(word_matrix, matrix_fp)
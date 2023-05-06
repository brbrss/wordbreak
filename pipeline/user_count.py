import numpy as np
from StatTool.fast_seg import FastSeg
import filepickle
import scipy.sparse


def get_user():
    arr = []
    with open('data/user.txt', 'r', encoding='utf-8') as f:
        arr = f.readlines()
    arr = [s.strip() for s in arr]
    return arr


def create_seg(data):
    d = []
    for tid in data:
        t = data[tid]
        for p in t.post_list:
            content = p.content
            d.append(content)
    seg = FastSeg(d)
    return seg


def user_count(data_fp, break_fp, reduced_word_fp, user_count_fp):
    data = filepickle.load(data_fp)
    wlist = filepickle.load(reduced_word_fp)

    b = filepickle.load(break_fp)

    nword = len(wlist)
    user_list = get_user()
    nuser = len(user_list)
    shape = (nuser, nword)
    word_index = {wlist[i]: i for i in range(nword)}
    result = scipy.sparse.lil_array(shape)

    i = 0
    p_pos = 0  # running count of post
    for tid in data:
        t = data[tid]
        for p in t.post_list:
            if p.author in user_list:
                seg = FastSeg([p.content])
                seg.b = [b[p_pos]]
                seg.init_count()
                for w in seg.word_count:
                    try:
                        w_pos = word_index[w]
                        aid = user_list.index(p.author)
                        result[aid, w_pos] += seg.word_count[w]
                    except KeyError:
                        pass
            p_pos += 1
    filepickle.dump(result, user_count_fp)

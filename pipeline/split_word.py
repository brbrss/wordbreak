from collections import Counter
from StatTool.biseg import Biseg
import filepickle


def show_info(seg: Biseg):
    n = len(seg.bigram)
    print('words: ', seg.nword)
    print('unique: ', n)
    print('nchanged: ', seg.nchanged)


def split_word(word_fp, count_fp, net_count_fp):

    print('start splitting keywords')
    word_list = filepickle.load(word_fp)
    count_data = filepickle.load(count_fp)
    ls = [(word_list[i], count_data[i]) for i in range(len(count_data))]
    seg = Biseg(ls)

    seg.TAU = 0.5
    seg.ALPHA = 5
    max_t = 5
    nrun = 20
    for i in range(nrun):
        seg.temperature = max_t - i/nrun*(max_t-1)
        print('annealing t=', seg.temperature)
        seg.gibbs()
        show_info(seg)
    ndata = len(seg.data)
    res = Counter()
    for i in range(ndata):
        for s in seg.repr(i):
            res[s] += seg.data[i][1]
    filepickle.dump(res, net_count_fp)

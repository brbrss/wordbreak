# generate term doc matrix
import time
import filepickle
from StatTool.trie import Trie
from StatTool.fast_seg import FastSeg, Segmenter
import os.path
import random


def fname(folder, i):
    name = 'b'+str(i)+'.seg'
    return os.path.join(folder, name)


def show_info(seg: Segmenter):
    n = len(seg.word_count)
    print('words: ', seg.nword)
    print('unique: ', n)
    print('nchanged: ', seg.nchanged)


def gen_seg(data_fp, trie_fp,  break_fp, seg_nrun=50):
    print('generating word break')
    data = filepickle.load(data_fp)
    d = []
    for tid in data:
        t = data[tid]
        for p in t.post_list:
            content = p.content
            d.append(content)
    seg = FastSeg(d)
    del d

    trie: Trie = filepickle.load(trie_fp)
    trie.invalidate_layer(1)
    seg.from_trie(trie)
    del trie

    ndata = len(seg.data)
    nround = ndata


    seg.TAU = 0.5
    seg.ALPHA = 3000
    for i in range(seg_nrun):
        #seg.temperature = max_t - i/seg_nrun*(max_t-1)
        seg.temperature = 1
        print('annealing t=', seg.temperature, ' round:', i)
        seg.gibbs()
        show_info(seg)

    seg.temperature = 0
    print('annealing t=', seg.temperature, ' round:', i)
    seg.gibbs()
    show_info(seg)

    #fp = fname(output_folder, str(int(time.time())))
    print('saved to ', break_fp)
    filepickle.dump(seg.b, break_fp)

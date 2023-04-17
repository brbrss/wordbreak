# generate term doc matrix
import filepickle
from StatTool.trie import Trie
from StatTool.segmenter import Segmenter
import os.path
import random


def fname(folder, i):
    name = 'b'+str(i)+'.seg'
    return os.path.join(folder, name)


def gen_seg(data_fp, trie_fp, output_folder):
    print('generating word break')
    data = filepickle.load(data_fp)
    trie: Trie = filepickle.load(trie_fp)
    d = []
    for tid in data:
        t = data[tid]
        for p in t.post_list:
            content = p.content
            d.append(content)
    seg = Segmenter(d)
    trie.invalidate_layer(1)
    seg.from_trie(trie)
    del trie
    del d
    ndata = len(seg.data)
    nround = ndata
    n = 100
    max_t = 4  # >1
    seg.TAU = 0.5
    seg.ALPHA = 200
    for i in range(n):
        seg.temperature = max_t - i/n*(max_t-1)
        print('annealing t=', seg.temperature, ' rounds:', nround)
        seg.init_count()
        for idata in range(nround):
            seg.anneal(idata)
    seg.temperature = 0
    for idata in range(nround):
        seg.anneal(idata)
    fp = fname(output_folder, i)
    print('saved to ', fp)
    filepickle.dump(seg.b, fp)

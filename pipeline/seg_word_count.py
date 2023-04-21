
import filepickle
from StatTool.fast_seg import FastSeg





def seg_word_count(data_fp, break_fp, min_occ, word_fp):
    data = filepickle.load(data_fp)
    d = [p.content for tid in data for p in data[tid].post_list]
    del data

    seg = FastSeg(d)
    seg.b = filepickle.load(break_fp)
    seg.init_count()
    wlist = [word for word in seg.word_count if seg.word_count[word] > min_occ]
    filepickle.dump(wlist, word_fp)

    return

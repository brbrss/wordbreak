
import filepickle
from StatTool.fast_seg import FastSeg





def seg_word_count(data_fp, break_fp, min_occ, word_fp):
    print('seg word count')
    data = filepickle.load(data_fp)
    d = [p.content for tid in data for p in data[tid].post_list]
    del data

    seg = FastSeg(d)
    seg.b = filepickle.load(break_fp)
    print('counting words')
    seg.init_count()
    print('filtering low occurrence words')
    wlist = [word for word in seg.word_count if seg.word_count[word] > min_occ]
    filepickle.dump(wlist, word_fp)
    print('finished counting words')
    return

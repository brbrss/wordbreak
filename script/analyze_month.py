from script.analyzer import Analyzer
from script.cat_count import CatCount
import datetime
import filepickle


class C(CatCount):
    def __init__(self, data_fp, reduced_word_fp, break_fp):
        super().__init__(data_fp, reduced_word_fp, break_fp)
        self.ncat = 12
        pass

    def category_id(self, t, p):
        try:
            date = datetime.datetime.fromisoformat(p.date)
            mon = date.month
            year = date.year
            if year!=2022:
                return None
            return mon-1
        except Exception:
            return None


class ResWriter:
    def __init__(self, fp):
        self.f = open(fp, 'w', encoding='utf-8')

    def close(self):
        self.f.close()

    def write(self, i, wlen, tw, tc):
        self.f.write('='*80+'\n')

        self.f.write('category '+str(i))
        self.f.write(' len: '+str(wlen))
        self.f.write('\n')

        self.f.write('clusters: ')
        self.f.write(', '.join([str(k) for k in tc]))
        self.f.write('\n')

        self.f.write('words: \n')
        w = [repr(t)[1:-1] for t in tw]
        self.f.write(' '.join(w))
        self.f.write('\n')

dfp = 'output/bymon.dump'

# print('loading')
# co = C('data/post.pickle', 'output/rword.dump', 'output/break.dump')
# print('counting')
# data = co.category_count()
# filepickle.dump(data,dfp)

data = filepickle.load(dfp)
ana = Analyzer('output/clu.dump', 'output/rword.dump')
writer = ResWriter('output/show/month.txt')
base = data[0]

print('processing categories')
for i in range(1, 12):
    print('processing ', i)
    ar = data[i]
    clu_dist = ana.cludist(base)
    tw = ana.top_word(ar, base)[:100]
    tc = ana.top_cat(ar, clu_dist)
    wlen = sum(ar)
    writer.write(i, wlen, tw, tc)
    base += ar

writer.close()
print('finished')

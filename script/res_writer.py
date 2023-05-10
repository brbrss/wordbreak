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
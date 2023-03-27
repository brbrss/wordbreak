
from StatTool.LayerDict import LayerDict
import functools


class CorpusModel(object):
    '''Contains three tables
    s: actual text
    pivot: pointer to text, sorted alphabetically
    co: length of common str between nearby pointers

    Invariants:
    if x in pivot, y in pivot
    then s[x:] < s[y:] iff pivot.index(x) < pivot.index[y]
    if pivot[i] == x
    then co[i] == length of common head of s[x:] and x[x+1:]

    Usage:
    feed(path) feeds data to self.s
    proc() generates self.pivot and self.co
    freq_table(minocc) outputs word frequency
    '''

    def __init__(self):
        self.data: list[str] = []

    def feed(self, s):
        self.data.append(s)

    def proc(self):
        '''Prepare ngram table'''
        print('Preprocessing text...')

        self.pivot: list[tuple[int, int]] = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                k = (i, j)
                self.pivot.append(k)
        self.co = []

        print('Preprocessing finished. Text has length', len(self.pivot))
        print('Sorting ngram list...')
        self._sort()
        print('Filling distance table...')
        self._fill_dist()
        print('Processing finished.')

    def _len(self):
        return len(self.pivot)

    def _get(self, x):
        '''s[x]'''
        try:
            i = x[0]
            j = x[1]
            return self.data[i][j]
        except IndexError:
            return None

    def _sort(self):
        def f(x, y): return self._cmp(x, y)
        self.pivot.sort(key=functools.cmp_to_key(f))

    def find(self, n, k):
        ''' words of length n appearing more than k times.
        Result indexed by position.'''
        d: dict[tuple[int, int], int] = {}
        count = 1
        for i in range(self._len()-1):
            if self.co[i] >= n:
                count += 1
            else:
                if count >= k:
                    d[self.pivot[i]] = count
                count = 1
        # loop ended, examine last char
        if count >= k:
            d[self.pivot[-1]] = count
        return d

    def word_find(self, n, k):
        '''Words of length n appearing more than k times.
        Indexed by string'''
        d = self.find(n, k)
        dd = {}
        for x in d:
            i = x[0]
            j = x[1]
            word = self.data[i][j:j+n]
            count = d[x]
            dd[word] = count
        return dd

    def _fill_dist(self):
        '''Fill distance table.'''
        pivotlen = len(self.pivot)
        for i in range(pivotlen-1):
            x = self.pivot[i]
            y = self.pivot[i+1]
            d = self._dist(x, y)
            self.co.append(d)

    def _dist(self, x, y):
        '''
        Length of common substring.
        ab,ac -> returns 1
        abcd,abce -> returns 3
        abc, abcd -> returns 3
        '''
        if x == y:
            return 0
        n = 0

        while self._get(x) == self._get(y):
            if self._get(x) is None:
                return n
            # will terminate since x!= y
            n += 1
            x = (x[0], x[1]+1)
            y = (y[0], y[1]+1)
        return n

    def show(self, start, end):
        '''Show section of ngram table.'''
        for i in range(start, end+1):
            k = self.pivot[i]
            print(k, self.data[k[0]][k[1]:], self.co[i])

    def _cmp(self, x, y):
        ''' Negative if x < y
        x<y if s[x] < s[y] , dictionary order.'''
        a = x
        b = y
        while 1:
            # finite loop since s finite

            sa = self._get(a)
            sb = self._get(b)
            if sa and sb:
                if sa == sb:
                    a = (a[0], a[1]+1)
                    b = (b[0], b[1]+1)
                else:
                    return ord(sa) - ord(sb)
            else:
                if sa is None:
                    return -1
                else:
                    return 1
        return None

    def freq_table(self, minocc):
        '''Generate frequency table.

        minocc: minimum number of occurence for word to be indexed.'''
        table = LayerDict()
        #table.len = self.len
        i = 0
        while True:
            i += 1
            d = self.word_find(i, minocc)
            if not d:
                break
            table.append(d)
        return table

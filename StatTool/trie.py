

class Trie(object):
    def __init__(self, c='', count=0):
        self.c = c
        self.count = count
        self.children: dict[str, Trie] = {}
        self.valid = True  # is a valid word node

    def find_child(self, c):
        if c in self.children:
            return self.children[c]
        else:
            return None
        # for cc in self.children:
        #     node = self.children[cc]
        #     if c == cc:
        #         return node

    def find_node(self, s: str):
        cur = self
        for c in s:
            cur = cur.find_child(c)
            if cur is None:
                return None
        return cur

    def insert(self, s: str, count):
        last = s[-1]
        cur = self
        for c in s:
            child = cur.find_child(c)
            if child is None:
                child = Trie(c, count)
                cur.children[c] = child
            cur = child
        cur.count = count

    def net_count(self, root: 'Trie', min_occ: int, prefix: str):
        s = prefix + self.c
        for c in self.children:
            node = self.children[c]
            node.net_count(root, min_occ, s)
        if self.count < min_occ:
            self.valid = False
            return
        for i in range(0, len(s)+1):
            for j in range(i+1, len(s)+1):
                ss = s[i:j]
                node = root.find_node(ss)
                if ss != s and node:
                    node.count -= self.count
        return

    def layer(self, n: int):
        '''get dict of str:count with len(str)==n'''
        if n == 0:
            return {self.c: self.count}
        d = {}
        for c in self.children:
            node = self.children[c]
            sub = node.layer(n-1)
            dd = {(self.c+cc): sub[cc] for cc in sub}
            d.update(dd)
        return d

    def _to_dict(self):
        result = {}
        for c in self.children:
            node = self.children[c]
            d = node._to_dict()
            dd = {(self.c+cc): d[cc] for cc in d}
            result.update(dd)
        result[self.c] = self.count
        return result


def _substract(d, s, val):
    for i in range(0, len(s)+1):
        for j in range(i+1, len(s)+1):
            ss = s[i:j]
            d[ss] -= val


def to_dict(trie: Trie, min_count):
    '''convert to dict, nodes with net count less than
    specified are ignored'''
    d = trie._to_dict()
    ls = list(d.keys())
    ls.sort(key=lambda s: len(s), reverse=True)
    result = {}
    for s in ls:
        if d[s] >= min_count:
            result[s] = d[s]
            _substract(d, s, d[s])
    return result


def _match_to_trie(s: str, t: Trie, start: int):
    '''Helper of match_to_trie

    Finds longest matching substring with a set given index
    s: to be matched
    t: trie of word candidates
    start: starting index

    returns: int `end` such that s[start:end] is the longest
    matching substring starting at start 
    '''
    cur = t
    best_end = start
    for k in range(start, len(s)):
        c = s[k]
        node = cur.find_child(c)
        if not node:
            return best_end
        if node.valid:
            best_end = k+1
    return best_end


def match_to_trie(s: str, t: Trie):
    ''' match string to trie

    Returns list of valid words occuring in string. 
    A word is valid if the corresponding node in trie exists
    and is valid'''

    res = []
    cur_j = 0
    for i in range(len(s)):
        j = _match_to_trie(s, t, i)
        if j > cur_j and j > i:
            cur_j = j
            res.append(s[i:j])
    return res

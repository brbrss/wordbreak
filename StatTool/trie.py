

class Trie(object):
    def __init__(self, c='', count=0):
        self.c = c
        self.count = count
        self.children: dict[str, Trie] = {}

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

    def net_count(self, s: str):
        node = self.find_node(s)
        if node is None:
            return 0
        n = node.count
        for c in node.children:
            n -= node.children[c].count
        return n

    def layer(self, n: int):
        '''get dict of str:count with len(str)==n'''
        if n == 0:
            return {self.c: self.count}
        d = {}
        for c in self.children:
            node = self.children[c]
            sub = node.layer(n-1)
            dd = {(self.c+cc):sub[cc] for cc in sub}
            d.update(dd)
        return d

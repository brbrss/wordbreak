

class Trie(object):
    def __init__(self, c='', count=0):
        self.c = c
        self.count = count
        self.children: dict[str, Trie] = {}

    def find_child(self, c):
        for cc in self.children:
            node = self.children[cc]
            if c == cc:
                return node
        return None

    def find_node(self, s: str):
        cur = self
        for c in s:
            cur = cur.find_child(c)
            if cur is None:
                return None
        return cur

    def insert(self, s: str, count):
        last = s[-1]
        parent = self.find_node(s[:-1])
        if parent.children.get(last, None):
            pass
        node = Trie(last, count)
        parent.children[last] = node

    def net_count(self, s: str):
        node = self.find_node(s)
        n = node.count
        for c in node.children:
            n -= node.children[c].count
        return n

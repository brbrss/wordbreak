

class Node(object):
    def __init__(self, c, count):
        self.c = c
        self.count = count
        self.children: dict[str, Node] = {}

    def find_child(self, c):
        for cc in self.children:
            node = self.children[cc]
            if c == cc:
                return node
        return None


class Trie(object):
    def __init__(self):
        #self.data = {}
        self.root = Node('', 0)

    def find_node(self, s: str):
        cur = self.root
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
        node = Node(last, count)
        parent.children[last] = node

    def net_count(self, s: str):
        node = self.find_node(s)
        n = node.count
        for c in node.children:
            n -= node.children[c].count
        return n

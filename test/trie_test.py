from StatTool.trie import Trie
import unittest


class TestTrie(unittest.TestCase):

    def test_insert(self):
        trie = Trie()
        d = ['apple', 'about', 'boo', 'bot']
        i = 1
        for s in d:
            for k in range(len(s)):
                prefix = s[:k+1]
                trie.find_node(prefix)
                trie.insert(prefix, i)
                i += 1
        node = trie.find_node('abo')
        self.assertEqual(node.count, 8)

    def test_netcount(self):
        trie = Trie()
        d = {'x': 36, 'xy': 6, 'b': 2, 'xz': 5, 'xyy': 6, 'bb': 2, 'bbb': 2}
        i = 1
        for s in d:
            trie.insert(s, d[s])
        self.assertEqual(trie.net_count('x'), 36-6-5)
        self.assertEqual(trie.net_count('bb'), 0)


if __name__ == '__main__':
    unittest.main()

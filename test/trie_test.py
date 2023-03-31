from StatTool.trie import Trie
from StatTool.trie import to_dict
import unittest


class TestTrie(unittest.TestCase):

    def test_insert(self):
        trie = Trie('', 0)
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
        trie = Trie('', 0)
        d = {'x': 36, 'xy': 6, 'b': 2, 'xz': 5, 'xyy': 6, 'bb': 2, 'bbb': 2}
        i = 1
        for s in d:
            trie.insert(s, d[s])
        self.assertEqual(trie.find_node('x').net_count(), 36-6-5)
        self.assertEqual(trie.find_node('bb').net_count(), 0)

    def test_insert_reverse(self):
        trie = Trie('', 0)
        d = {'rfvv': 45, 're': 5, 'r': 99}
        for s in d:
            trie.insert(s, d[s])
        self.assertEqual(trie.find_node('rfvv').count, 45)

    def test_layer(self):
        trie = Trie('', 0)
        d = {'x': 36, 'xy': 6, 'b': 2, 'xz': 5, 'xyy': 6, 'bb': 2, 'bbe': 2}
        i = 1
        for s in d:
            trie.insert(s, d[s])
        target = {k: d[k] for k in d if len(k) == 1}
        self.assertDictEqual(trie.layer(1), target)
        target = {k: d[k] for k in d if len(k) == 2}
        self.assertDictEqual(trie.layer(2), target)
        target = {k: d[k] for k in d if len(k) == 3}
        self.assertDictEqual(trie.layer(3), target)

    def test_to_dict(self):
        trie = Trie('', 0)
        d = {'x': 40, 'y': 30, 'yy': 7, 'z': 30, 'xy': 30, 'xz': 6,
             'xyy': 6, 'b': 10, 'be': 2, 'e': 2,  'bb': 3, 'bbe': 2}
        for s in d:
            trie.insert(s, d[s])
        target = {'x': 4, 'xy': 30-6, 'xz': 6,
                  'xyy': 6, 'z': 30-6, 'b': 10-2-2, 'bbe': 2}
        # 'bbe' contains 2 'b', 2 'bbe' means 'b' gets to reduce by 4
        self.assertDictEqual(to_dict(trie, 2), target)

    def test_to_dict2(self):
        trie = Trie('', 0)
        s = 'abcdefg'
        for i in range(0, len(s)+1):
            for j in range(i+1, len(s)+1):
                trie.insert(s[i:j], 49)
        target = {s: 49}
        self.assertDictEqual(to_dict(trie, 2), target)


if __name__ == '__main__':
    unittest.main()

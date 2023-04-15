
from StatTool.segmenter import Segmenter
from StatTool.trie import Trie
import unittest


class TestSegmenter(unittest.TestCase):

    def test_repr(self):
        data = ['lloo', 'trees']
        seg = Segmenter(data)

        res = seg.repr(1)
        target = ['t', 'r', 'e', 'e', 's']
        self.assertListEqual(res, target)

    def test_one(self):
        trie = Trie()
        trie.insert('dog', 0)
        trie.insert('cat', 0)
        data = ['tdogacatuv']
        seg = Segmenter(data)
        seg.from_trie(trie)

        res = seg.repr(0)
        target = ['t', 'dog', 'a', 'cat', 'u', 'v']
        self.assertListEqual(res, target)

    def test_count(self):
        trie = Trie()
        trie.insert('dog', 0)
        trie.insert('cat', 0)
        trie.insert('bull', 0)
        data = ['tdogacatuv', 'bulldog', 'awha']
        seg = Segmenter(data)
        seg.from_trie(trie)

        seg.init_count()

        self.assertEqual(seg.nword, seg.word_count.total())
        target = {'dog': 2, 'cat': 1, 'bull': 1}
        self.assertDictContainsSubset(target, seg.word_count)


if __name__ == '__main__':
    unittest.main()

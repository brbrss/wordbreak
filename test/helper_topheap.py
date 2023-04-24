import helper.topheap

import unittest


class TestTopheap(unittest.TestCase):

    def test_insert_less(self):
        h = helper.topheap.TopHeap(5)
        d = {'t': 6, 'w': 5, 'a': 9}
        for k in d:
            h.push(k, d[k])
        target = set(d.keys())
        self.assertSetEqual(set(h.data()), target)

    def test_insert_equal(self):
        h = helper.topheap.TopHeap(3)
        d = {'t': 6, 'w': 5, 'a': 9}
        for k in d:
            h.push(k, d[k])
        target = set(d.keys())
        self.assertSetEqual(set(h.data()), target)

    def test_replace(self):
        h = helper.topheap.TopHeap(2)
        d = {'t': 6, 'w': 5, 'a': 9,'v':3}
        for k in d:
            h.push(k, d[k])
        target = set(['t','a'])
        self.assertSetEqual(set(h.data()), target)

    def test_insert_more(self):
        h = helper.topheap.TopHeap(2)
        d = {'t': 6, 'w': 5, 'a': 9,'v':3,'u':5,'m':10,'n':11}
        for k in d:
            h.push(k, d[k])
        target = set(['m','n'])
        self.assertSetEqual(set(h.data()), target)
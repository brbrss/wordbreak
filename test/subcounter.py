from StatTool.subcounter import SubCounter
import unittest


class TestSubCounter(unittest.TestCase):

    def test_insert(self):
        counter = SubCounter()
        for i in range(5):
            counter.inc(i)
            counter.inc(i)
        self.assertEqual(counter.get(4), 3)
        counter.clear(3)
        self.assertEqual(counter.get(3), 1)
        self.assertEqual(counter.get(2), 3)




if __name__ == '__main__':
    unittest.main()

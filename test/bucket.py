
from StatTool.bucket import BucketList
import unittest


class TestBucketList(unittest.TestCase):

    def test_one(self):
        buck = BucketList()
        buck.add('f', 'fff')
        buck.add('f', 'fef')
        buck.add('w', 'w')
        buck.add('a', 'a5')
        buck.add('w', 'w5')
        buck.sort()
        res = []
        for t in buck:
            res.append(t)
        target = ['a5', 'fff', 'fef', 'w', 'w5']
        self.assertListEqual(res, target)


if __name__ == '__main__':
    unittest.main()

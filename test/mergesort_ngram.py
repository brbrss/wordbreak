from StatTool.mergesort_ngram import MergeCorpusModel
import unittest




class TestMcm(unittest.TestCase):


    def test_encode(self):
        cm = MergeCorpusModel(10)
        cm.key_table = [0,15,235,1984,2358,6134]
        t = 5,4096
        data = cm.encode_pivot_entry(t)
        output = cm.decode_pivot_entry(data)
        self.assertEqual(output,t)
        t = 0,0
        data = cm.encode_pivot_entry(t)
        output = cm.decode_pivot_entry(data)
        self.assertEqual(output,t)



if __name__ == '__main__':
    unittest.main()


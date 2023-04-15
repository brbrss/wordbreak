
from pipeline.pipeline import Pipeline, Step
import unittest


def f1(a, b, c):
    return a+b+c


def f2(a, b):
    return b+a


def f3(a):
    return a+a


def f4(a, b):
    return a+b+'-'


d = {'a': 'cat', 'b': 'rat', 'c': 'horse', 'd': 'lion'}


class PipelinetList(unittest.TestCase):

    def test_one(self):
        pipe = Pipeline()
        pipe.set_config(d)
        pipe.add('one', f1, {'a': 'b', 'b': 'b', 'c': 'a'})
        pipe.run_one('one')
        target = d['b']+d['b']+d['a']
        self.assertEqual(pipe.config['one'], target)

    def test_from(self):
        pipe = Pipeline()
        pipe.set_config(d)
        pipe.add('one', f3, {'a': 'd'},'one_res')
        pipe.add('two', f3, {'a': 'one_res'})
        pipe.add('three', f2, {'a': 'a', 'b': 'two'})

        pipe.run_from('one')
        target = d['d']*2*2+d['a']
        self.assertEqual(pipe.config['three'], target)

    def test_from_middle(self):
        pipe = Pipeline()
        pipe.set_config(d)
        pipe.add('one', f3, {'a': 'd'})
        pipe.add('two', f3, {'a': 'one'})
        pipe.add('three', f2, {'a': 'a', 'b': 'two'})

        pipe.set_config({'one': 'w'})
        pipe.run_from('two')
        target = 'w'*2+d['a']
        self.assertEqual(pipe.config['three'], target)

    def test_config_update(self):
        pipe = Pipeline()
        pipe.set_config(d)
        pipe.add('one', f3, {'a': 'd'})
        pipe.run_from('one')
        self.assertEqual(pipe.config['one'], d['d']*2)

        pipe.set_config({'d': 'x'})
        pipe.run_from('one')
        self.assertEqual(pipe.config['one'], 'xx')


    def test_validate(self):
        pipe = Pipeline()
        pipe.set_config(d)
        pipe.add('one', f3, {'a': 'd'})
        pipe.validate()

if __name__ == '__main__':
    unittest.main()

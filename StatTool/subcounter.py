

class SubCounter(object):
    '''class for counting substr'''

    def __init__(self):
        self.data: list[int] = []

    def get(self, i: int):
        if i >= len(self.data):
            return 1
        else:
            return self.data[i]

    def inc(self, i: int):
        n = len(self.data)
        if type(i) is not int:
            raise IndexError('invalid type')
        if i < 0:
            raise IndexError('negative index not supported')
        if i > n:
            raise IndexError('should inc i-1 first')
        elif i == n:
            self.data.append(2)
        elif i < n:
            self.data[i] += 1

    def __len__(self):
        return len(self.data)

    def clear(self, k):
        '''clear index >= k'''
        self.data = self.data[:k]

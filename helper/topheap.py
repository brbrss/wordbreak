import heapq




class _Item:
    def __init__(self, k, v):
        self.k = k
        self.v = v

    def __lt__(self, other):
        return self.v < other.v


class TopHeap:
    '''data structure for storing top n elements'''
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.arr: list[_Item] = []

    def __len__(self):
        return len(self.arr)

    def push(self, k, v):
        x = _Item(k, v)
        if len(self) < self.max_size:
            heapq.heappush(self.arr, x)
        else:
            if v>self.arr[0].v:
                heapq.heapreplace(self.arr, x)
        return

    def data(self):
        return [t.k for t in self.arr]

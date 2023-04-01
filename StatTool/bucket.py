

class BucketIterator:
    def __init__(self, buck):
        self.buck = buck
        self.bucket_it = iter(buck.data)
        #self.cur_list = None
        self.list_it = iter([])

    def __iter__(self):
        return self

    def __next__(self):
        #found = False
        while True:
            try:
                return next(self.list_it)
            except StopIteration:
                bucket_key = next(self.bucket_it)
                self.list_it = iter(self.buck.data[bucket_key])
        pass


class BucketList(object):
    def __init__(self):
        self.data: dict[any, list] = {}
        pass

    def add(self, key, val):
        if key in self.data:
            self.data[key].append(val)
        else:
            self.data[key] = [val]

    def __iter__(self):
        return BucketIterator(self)

    def sort(self):
        self.data = dict(sorted(self.data.items()))

    def clear(self):
        self.data.clear()

    def __len__(self):
        return sum([len(self.data[k]) for k in self.data])
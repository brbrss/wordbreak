
import functools
from StatTool.ngram import CorpusModel
import pickle
import struct
from typing import BinaryIO
import bisect
import os.path
from StatTool.subcounter import SubCounter

from StatTool.trie import Trie
from StatTool.bucket import BucketList


class MergeCorpusModel(CorpusModel):
    '''
    LIke CorpusModel, but handles the case when 
    self.pivot is too large to fit into  memory.

    How it works: load all data into self.s, 
    prepare and sort pivot on one batch of data, 
    merge with existing pivot from previous batches,
    write merged pivot list to disk,.
    '''

    def __init__(self, batch_size, folder=''):
        '''
        batch_size: number of entries in one processing batch
        '''
        super().__init__()

        # number of entries in one batch
        self.folder = folder
        self.batch_size = batch_size
        self.pivot_fp = None  # file path of partial pivot table
        self.key_table: list[int] = []
        self.pivot: list[tuple[int, int]] = []

    def encode_pivot_entry(self, entry: tuple[int, int]):
        '''
        returns binary form of pivot entry
        '''
        x, y = entry  # x entry index, y char offset
        offset = self.key_table[x]
        return struct.pack('i', offset + y)

    def decode_pivot_entry(self, bdata):
        '''
        returns pivot entry from binary form
        '''
        val = struct.unpack('i', bdata)[0]
        index = bisect.bisect(self.key_table, val)-1
        offset = self.key_table[index]
        return index, val-offset

    def gen_dump_name(self, start, end):
        filename = str(start)+'to'+str(end)+'.pickle'
        return os.path.join(self.folder, filename)

    def _partial_pivot(self, start, end):
        for i in range(start, end):
            for j in range(len(self.data[i])):
                k = (i, j)
                self.pivot.append(k)
        self._sort()

    def _bucket_sort(self):
        self.bucket_pivot.sort()
        def f(x, y): return self._cmp(x, y)
        for k in self.bucket_pivot.data:
            self.bucket_pivot.data[k].sort(key=functools.cmp_to_key(f))
        return

    def _partial_pivot_bucket(self, start, end):
        self.bucket_pivot = BucketList()
        for i in range(start, end):
            for j in range(len(self.data[i])):
                pivot_entry = (i, j)
                bucket_key = self._get(pivot_entry)
                self.bucket_pivot.add(bucket_key, pivot_entry)
        self._bucket_sort()
        print('num of buckets: ',len(self.bucket_pivot.data))

    def proc_part(self, start, size):
        '''
        Process pivot for data in [start:start+size]
        and merge with existing pivot data.

        start: starting data index
        size: number of entries to process'''

        self.pivot = []
        end = min(start+size, len(self.data))
        self._partial_pivot(start, end)
        fp = self.gen_dump_name(start, end)
        self.merge_pivot(fp)
        self.pivot.clear()
        return

    def _parse_pivot_dump(self, src_file: BinaryIO):
        '''Reads file and returns list of pivot.
        Only reads a limited chunk of file data.
        Call this function again to read more.
        Returns [] if eof is reached.'''

        buf = src_file.read(1024)
        if len(buf) % 4 != 0:
            raise RuntimeError('file size should be multiples of 8')
        num_entry = len(buf) // 4
        pivot_buf = [self.decode_pivot_entry(
            buf[i*4:i*4+4]) for i in range(num_entry)]
        return pivot_buf

    def _merge_pivot_file(self, src_file: BinaryIO, dst_file: BinaryIO):
        '''file version'''
        i = 0  # index to current pivot table
        cur_len = len(self.pivot)
        while True:
            old_pivot = self._parse_pivot_dump(src_file)
            if not old_pivot:
                break
            old_len = len(old_pivot)
            j = 0  # index to old pivot
            while i < cur_len and j < old_len:
                old = self.encode_pivot_entry(old_pivot[j])
                cur = self.encode_pivot_entry(self.pivot[i])
                cmp_res = self._cmp(old_pivot[j], self.pivot[i])
                if cmp_res <= 0:  # old smaller
                    dst_file.write(old)
                    j += 1
                else:
                    dst_file.write(cur)
                    i += 1
                pass
            while j < old_len:
                dst_file.write(self.encode_pivot_entry(old_pivot[j]))
                j += 1
        while i < cur_len:
            dst_file.write(self.encode_pivot_entry(self.pivot[i]))
            i += 1

    def merge_pivot(self, dst_fp):
        '''Merge pivot table. Contains two inputs: current batch pivot from
        self and previous pivot from disk file. Path to disk file is 
        in self.pivot_fp

        Result of merge is written to disk file. New file path is 
        written to self.pivot_fp
        '''
        src_fp = self.pivot_fp
        f2 = open(dst_fp, 'wb')
        if src_fp is None:
            for t in self.pivot:
                buf = self.encode_pivot_entry(t)
                f2.write(buf)
        else:
            f1 = open(src_fp, 'rb')
            self._merge_pivot_file(f1, f2)
            f1.close()
        f2.close()
        self.pivot_fp = dst_fp
        return

    def proc_pivot(self):
        '''Create and sort pivot'''

        start = 0
        data_len = len(self.data)
        while start < data_len:
            print('processing pivot batch at: ', start)
            self.proc_part(start, self.batch_size)
            start += self.batch_size
        return

    def proc(self):
        '''do not call this'''
        raise NotImplementedError('do not call this function')

    def gen_trie(self, minocc):
        trie = Trie()
        count = SubCounter()
        with open(self.pivot_fp, 'rb') as f:
            #i = 0
            pivot_1 = self.decode_pivot_entry(f.read(4))
            pivot_2 = self.decode_pivot_entry(f.read(4))

            while pivot_1 is not None:
                common = 0
                if pivot_2 is not None:
                    common = self._dist(pivot_1, pivot_2)
                for k in range(common+1):  # k in [0,common]
                    count.inc(k)
                for k in range(common+1, len(count)):
                    # longer str counts are finalized
                    occ = count.get(k)
                    if occ >= minocc:
                        #s = self.get_str(i, k)
                        data_id, offset = pivot_1
                        s = self.data[data_id][offset:offset+k]
                        trie.insert(s, occ)
                count.clear(common+1)
                buf = f.read(4)
                pivot_1 = pivot_2
                if len(buf) == 4:
                    pivot_2 = self.decode_pivot_entry(buf)
                else:
                    pivot_2 = None
                #i += 1
        return trie

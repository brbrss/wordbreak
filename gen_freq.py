import pickle
from StatTool.mergesort_ngram import MergeCorpusModel
from StatTool.trie import to_dict
import random

print('script start...')
print('loading data')

f = open('./data/post.pickle', 'rb')
data = pickle.load(f)
f.close()

BATCH_SIZE = 5 * 1000
cm = MergeCorpusModel(BATCH_SIZE, 'output')
# tid, index of post, size of data so far
text_key: list[tuple[int, int, int]] = []
count = 0
running_size = 0

print('feeding data')
# fix seed for consistent sampling
random.seed(123)
for tid in data:
    t = data[tid]
    for i in range(len(t.post_list)):
        # sample 3%
        if random.random() < 0.03:
            content = t.post_list[i].content
            cm.feed(content)
            entry_key = (tid, i, running_size)
            text_key.append(entry_key)
            running_size += len(content)
            count += 1
del data

print('loading finished')

# with open('output/key.dump', 'wb') as f:
#     pickle.dump(text_key, f)

print('key data dumped')

print('processing pivot')

#cm.proc_pivot(start=170000, pivot_fp='output/to170000.pickle', end=300000)
#cm.proc_pivot(start=0, pivot_fp=None, end=0)

print('generating trie')
cm.pivot_fp = 'output/to47246.pickle'
MIN_OCC = 50
trie = cm.gen_trie(MIN_OCC)
with open('output/trie.dump', 'wb') as f:
    pickle.dump(trie, f)
trie.net_count(MIN_OCC)
with open('output/net_trie.dump', 'wb') as f:
    pickle.dump(trie, f)

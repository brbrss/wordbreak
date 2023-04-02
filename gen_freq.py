import pickle
from StatTool.mergesort_ngram import MergeCorpusModel
from StatTool.trie import to_dict

print('script start...')
print('loading data')

f = open('./data/post.pickle', 'rb')
data = pickle.load(f)
f.close()

BATCH_SIZE = 20 * 1000
cm = MergeCorpusModel(BATCH_SIZE, 'output')
# tid, index of post, size of data so far
text_key: list[tuple[int, int, int]] = []
count = 0
running_size = 0

print('feeding data')

for tid in data:
    t = data[tid]
    for i in range(len(t.post_list)):
        content = t.post_list[i].content
        cm.feed(content)
        entry_key = (tid, i, running_size)
        text_key.append(entry_key)
        running_size += len(content)
        count += 1
del data

print('loading finished')

with open('output/key.dump', 'wb') as f:
    pickle.dump(text_key, f)

print('key data dumped')

print('processing pivot')
#cm.key_table = [t[2] for t in text_key]
cm.proc_pivot(start=130000, pivot_fp='output/to130000.pickle', end=0)

print('generating trie')

MIN_OCC = 50
trie = cm.gen_trie(MIN_OCC)
with open('output/trie.dump', 'wb') as f:
    pickle.dump(trie, f)
word_dict = to_dict(trie, MIN_OCC)
with open('output/words.dump', 'wb') as f:
    pickle.dump(word_dict, f)

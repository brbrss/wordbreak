import pickle
from StatTool.mergesort_ngram import MergeCorpusModel
from StatTool.trie import to_dict


f = open('./spike/title/data.pickle', 'rb')
data = pickle.load(f)
f.close()

cm = MergeCorpusModel(2000, 'output')
# tid, index of post, size of data so far
text_key: list[tuple[int, int, int]] = []
count = 0
running_size = 0
# for tid in data:
#     t = data[tid]
#     for i in range(len(t.post_list)):
#         pid = tid, i
#         content = t.post_list[i].content
#         cm.feed(content)
#         text_key[count] = tid, i, running_size
#         running_size += len(content)
#         count += 1
# del data

for t in data:
    cm.feed(t)
    text_key.append((0, 0, running_size))
    running_size += len(t)
    count += 1

with open('output/key.dump', 'wb') as f:
    pickle.dump(text_key, f)

cm.key_table = [t[2] for t in text_key]
cm.proc_pivot()
trie = cm.gen_trie(10)
with open('output/trie.dump', 'wb') as f:
    pickle.dump(trie, f)
word_dict = to_dict(trie, 10)
with open('output/words.dump', 'wb') as f:
    pickle.dump(word_dict, f)

# def dump_pivot(pivot):
#    for key in pivot:


# MAX_ENTRY = 100
# count = 0
# for i in range(len(cm.data)):
#     for j in range(len(cm.data[i])):
#         k = i, j
#         cm.pivot.append(k)
#         count += 1
#         if count >MAX_ENTRY:
#             do_batch()


# cm.proc()
# ftable = cm.freq_table(20)
# with open('test/ftt.dump', 'wb') as f:
#     pickle.dump(ftable, f)

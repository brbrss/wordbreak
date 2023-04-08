# generate term doc matrix
import filepickle
from StatTool.trie import Trie
from StatTool.trie import match_to_trie
import pandas
import numpy


def gen_index():
    df = filepickle.load('output/df.dump')
    s_index = {}
    i = 0
    for row in df.itertuples():
        s_index[row.s] = i
        i += 1
    return s_index


word_index = gen_index()

trie: Trie = filepickle.load('output/trie.dump')
#data = filepickle.load('./data/post.pickle')
data = filepickle.load('./output/small129.dump')


nword = len(word_index)
ndata = len(data)  # threads, not posts

len_data = len(data)
len_data = 128
passed = 0
cur_thread = 0
i = 0
word_matrix = numpy.zeros(shape=(nword, len_data))  # word, doc shape
print('start counting')
for tid in data:
    i += 1
    if i == len_data:
        break
    passed += 1
    if passed > 0.01*len_data:
        cur_thread += 1
        passed = 0
        print(cur_thread, '%')
    t = data[tid]
    for k in range(len(t.post_list)):
        content = t.post_list[k].content
        raw = match_to_trie(content, trie)
        for word in raw:
            wid = word_index[word]
            word_matrix[wid][cur_thread] += 1

# ii = 0
# word_matrix = numpy.zeros(shape=(nword, 40))
# for t in data:
#     if ii > 40:
#         break
#     ii += 1
#     raw = match_to_trie(t, trie)
#     for word in raw:
#         wid = word_index[word]
#         word_matrix[wid][cur_thread] += 1

#filepickle.dump(word_matrix, 'output/matrix.dump')
filepickle.dump(word_matrix, 'spike/garbage/matrix.dump')

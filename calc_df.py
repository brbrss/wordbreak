# calculate document frequency

import filepickle
from StatTool.trie import Trie
from StatTool.trie import match_to_trie
import pandas


def trie_dict(t: Trie, d=None, prefix=''):
    dd: dict[str, tuple[int, int]] = d
    if dd == None:
        dd = {}
    s = prefix + t.c
    if t.valid:
        dd[s] = 0, 0
    for c in t.children:
        node = t.children[c]
        trie_dict(node, dd, prefix=s)
    return dd


# trie
trie: Trie = filepickle.load('output/trie.dump')

# first int is total term freq, second int is document freq
tf_df: dict[str, tuple[int, int]] = trie_dict(trie)


data = filepickle.load('./data/post.pickle')
#data = filepickle.load('./spike/title/data.pickle')


def count_text(text):
    raw = match_to_trie(text, trie)
    unique = set(raw)
    for word in raw:
        old = tf_df[word]
        tf_df[word] = old[0]+1, old[1]
    for word in unique:
        old = tf_df[word]
        tf_df[word] = old[0], old[1]+1
    return


len_data = len(data)
passed = 0
i = 0
print('start counting')
for tid in data:
    passed += 1
    if passed > 0.01*len_data:
        i += 1
        passed = 0
        print(i, '%')
    t = data[tid]
    for k in range(len(t.post_list)):
        content = t.post_list[k].content
        count_text(content)

# for t in data:
#     count_text(t)


ls = [(t, tf_df[t][0], tf_df[t][1]) for t in tf_df]

df = pandas.DataFrame.from_records(ls, columns=['s', 'tf', 'df'])
df = df.sort_values(by='df')


filepickle.dump(df, 'output/df.dump')

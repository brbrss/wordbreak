# generate term doc matrix
import filepickle
from StatTool.trie import Trie
from StatTool.trie import match_to_trie

import numpy


def gen_index():
    df = filepickle.load('output/df.dump')
    s_index = {}
    i = 0
    for row in df.itertuples():
        s_index[row.s] = i
        i += 1
    return s_index


def gen_matrix(trie_fp, data_fp, matrix_fp):
    word_index = gen_index()

    trie: Trie = filepickle.load(trie_fp)
    data = filepickle.load(data_fp)

    nword = len(word_index)

    len_data = len(data)

    passed = 0
    cur_thread = 0
    word_matrix = numpy.zeros(shape=(nword, len_data))  # word, doc shape
    print('start counting')
    for tid in data:
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

    filepickle.dump(word_matrix, matrix_fp)

# generate term doc matrix
import filepickle
from StatTool.trie import Trie
from StatTool.trie import match_to_trie

import numpy


def gen_matrix(ntrie_fp, word_fp, data_fp, matrix_fp):

    print('generating word doc matrix')
    trie: Trie = filepickle.load(ntrie_fp)
    data = filepickle.load(data_fp)

    word_list = filepickle.load(word_fp)
    word_index = {word_list[i]: i for i in range(len(word_list))}
    nword = len(word_index)

    len_data = len(data)

    passed = 0
    cur_thread = 0
    cur_percent = 0
    word_matrix = numpy.zeros(shape=(nword, len_data))  # word, doc shape
    print('num of words: ', nword)
    print('num of doc: ', len_data)
    print('start counting')
    for tid in data:
        passed += 1
        if passed > 0.01*len_data:
            passed = 0
            cur_percent += 1
            print(cur_percent, '%')
        t = data[tid]
        for k in range(len(t.post_list)):
            content = t.post_list[k].content
            raw = match_to_trie(content, trie)
            for word in raw:
                wid = word_index[word]
                word_matrix[wid][cur_thread] += 1
        cur_thread += 1
        pass
    print('finished generating matrix')
    filepickle.dump(word_matrix, matrix_fp)

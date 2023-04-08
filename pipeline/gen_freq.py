import pickle
from StatTool.mergesort_ngram import MergeCorpusModel
from StatTool.trie import to_dict
import random


def gen_freq(data_fp, output_folder, trie_fp, min_occ, sample_percent=0.03, pivot_start=0, pivot_fp=None):
    print('script start...')
    print('loading data')

    f = open(data_fp, 'rb')
    data = pickle.load(f)
    f.close()

    BATCH_SIZE = 5 * 1000
    cm = MergeCorpusModel(BATCH_SIZE, output_folder)
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
            if random.random() < sample_percent:
                content = t.post_list[i].content
                cm.feed(content)
                entry_key = (tid, i, running_size)
                text_key.append(entry_key)
                running_size += len(content)
                count += 1
    del data

    print('loading finished')

    # with open('output/key.dump', 'wb') as f:
    #    pickle.dump(text_key, f)

    print('key data dumped')

    print('processing pivot')

    cm.proc_pivot(start=pivot_start, pivot_fp=pivot_fp, end=0)

    print('generating trie')

    #MIN_OCC = 50
    trie = cm.gen_trie(min_occ)
    with open(trie_fp, 'wb') as f:
        pickle.dump(trie, f)

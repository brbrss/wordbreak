import pipeline.pipeline as pipeline
from pipeline.gen_freq import gen_freq
from pipeline.gen_matrix import gen_matrix
from pipeline.gen_word_list import gen_word_list
from pipeline.gen_seg import gen_seg
from pipeline.word_count import word_count
from pipeline.split_word import split_word


pipe = pipeline.Pipeline()


d = pipeline.array_dict(['data_fp', 'output_folder',
                        'trie_fp', 'min_occ', 'sample_percent', 'pivot_start',  'pivot_fp'])
pipe.add('gen_freq', gen_freq, d)

# d = pipeline.array_dict(
#     ['data_fp', 'trie_fp', 'output_folder', 'break_fp', 'seg_nrun','max_temp'])
# pipe.add('gen_seg', gen_seg, d)


d = pipeline.array_dict(['trie_fp', 'ntrie_fp', 'word_fp'])
pipe.add('gen_word_list', gen_word_list, d)

d = pipeline.array_dict(['ntrie_fp', 'word_fp', 'data_fp', 'count_fp'])
pipe.add('word_count', word_count, d)

d = pipeline.array_dict(['word_fp', 'count_fp', 'net_count_fp'])
pipe.add('split_word', split_word, d)

# d = pipeline.array_dict(['ntrie_fp', 'word_fp', 'data_fp', 'matrix_fp'])
# pipe.add('gen_matrix', gen_matrix, d)


config = {
    'data_fp': 'data/post.pickle',
    'output_folder': 'out/',

    'sample_percent': 0.01,
    'min_occ': 20,
    'pivot_start': 0,

    'pivot_fp': None,
    'trie_fp': 'output/trie.dump',
    'ntrie_fp': 'output/ntrie.dump',

    'word_fp': 'output/words.dump',
    'matrix_fp': 'output/matrix.dump',
    'index_fp': 'output/windex.dump'

}


config_small = {
    'data_fp': 'output/small.pickle',
    'output_folder': 'spike/garbage/',

    'sample_percent': 0.2,
    'min_occ': 10,
    'pivot_start': 0,
    'pivot_fp': None,

    'trie_fp': 'spike/garbage/trie.dump',
    'ntrie_fp': 'spike/garbage/ntrie.dump',

    'seg_nrun': 10,
    'break_fp': None,
    'max_temp': 5,

    'word_fp': 'spike/garbage/word.dump',
    'count_fp': 'spike/garbage/count.dump',
    'net_count_fp': 'spike/garbage/net_count.dump',

    'matrix_fp': 'spike/garbage/matrix.dump',
    'index_fp': 'output/windex.dump'
}


# pipe.set_config(config)
# pipe.validate()
# pipe.run_all()


pipe.set_config(config_small)
pipe.validate()
pipe.run_from('split_word')

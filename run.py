import pipeline.pipeline as pipeline

from pipeline.gen_freq import gen_freq

from pipeline.gen_seg import gen_seg
from pipeline.seg_word_count import seg_word_count
from pipeline.seg_matrix import seg_matrix


pipe = pipeline.Pipeline()

######
d = pipeline.array_dict(['data_fp', 'output_folder',
                        'trie_fp', 'min_occ', 'sample_percent', 'pivot_start',  'pivot_fp'])
pipe.add('gen_freq', gen_freq, d)
######
d = pipeline.array_dict(
    ['data_fp', 'trie_fp', 'output_folder', 'partial_break', 'break_fp', 'max_temp','n_start', 'seg_nrun'])
pipe.add('gen_seg', gen_seg, d)
######
d = pipeline.array_dict(['data_fp', 'break_fp', 'min_occ', 'word_fp'])
pipe.add('seg_word_count', seg_word_count, d)
######
d = pipeline.array_dict(['data_fp', 'break_fp', 'word_fp', 'matrix_fp'])
pipe.add('seg_matrix', seg_matrix, d)

# d = pipeline.array_dict(['ntrie_fp', 'word_fp', 'data_fp', 'matrix_fp'])
# pipe.add('gen_matrix', gen_matrix, d)

# d = pipeline.array_dict(['matrix_fp','index_fp'])
# pipe.add('purge_word', purge_word, d)

config = {
    'data_fp': 'data/post.pickle',
    'output_folder': 'output/',

    'sample_percent': 0.03,
    'min_occ': 50,
    'pivot_start': 0,
    'pivot_fp': None,

    'trie_fp': 'output/trie.dump',
    # 'ntrie_fp': 'output/ntrie.dump',

    'partial_break': 'output/b9.seg',
    'n_start':20,
    'max_temp': 2,
    'seg_nrun': 20,
    'break_fp': 'output/break.dump',

    'word_fp': 'output/word.dump',
    'matrix_fp': 'output/matrix.dump',
}


config_small = {
    'data_fp': 'output/small.pickle',
    'output_folder': 'spike/garbage/',

    'sample_percent': 0.2,
    'min_occ': 10,
    'pivot_start': 0,
    'pivot_fp': None,

    'trie_fp': 'spike/garbage/trie.dump',
    # 'ntrie_fp': 'spike/garbage/ntrie.dump',

    'partial_break': None,
    'n_start':0,
    'max_temp': 2,
    'seg_nrun': 20,
    'break_fp': 'spike/garbage/break.dump',

    'word_fp': 'spike/garbage/word.dump',
    'matrix_fp': 'spike/garbage/matrix.dump',

}


pipe.set_config(config)
pipe.validate()
pipe.run_from('seg_matrix')


# pipe.set_config(config_small)
# pipe.validate()
# pipe.run_from('gen_seg')

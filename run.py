import pipeline.pipeline as pipeline
from pipeline.gen_freq import gen_freq
from pipeline.gen_matrix import gen_matrix

pipe = pipeline.Pipeline()


d = pipeline.array_dict(['data_fp', 'output_folder',
                        'trie_fp', 'min_occ', 'sample_percent', 'pivot_start',  'pivot_fp'])
pipe.add('gen_freq', gen_freq, d)

d = pipeline.array_dict(['trie_fp', 'data_fp', 'matrix_fp'])
pipe.add('gen_matrix', gen_matrix, d)


config = {
    'data_fp': 'data/post.pickle',
    'output_folder': 'out/',
    'sample_percent': 0.03,
    'min_occ': 50,
    'pivot_start': 0,
    'pivot_fp': None,
    'trie_fp': 'output/trie.dump',
    'matrix_fp': 'output/matrix.dump'
}


config_small = {
    'data_fp': 'output/small129.dump',
    'output_folder': 'spike/garbage/',
    'sample_percent': 0.1,
    'min_occ': 10,
    'pivot_start': 5489,
    'pivot_fp': 'spike/garbage/to5489.pickle',
    'trie_fp': 'spike/garbage/trie.dump',
    'matrix_fp': 'spike/garbage/matrix.dump'
}


# pipe.set_config(config)
# pipe.run_from('gen_matrix')


pipe.set_config(config_small)
pipe.run_all()

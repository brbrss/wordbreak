import pipeline.pipeline as pipeline

from pipeline.gen_freq import gen_freq

from pipeline.gen_seg import gen_seg
from pipeline.seg_word_count import seg_word_count
from pipeline.seg_matrix import seg_matrix
from pipeline.reduce_word import reduce_word
from pipeline.calc_pca import calc_pca

from pipeline.cluster import cluster
from pipeline.find_topic import find_topic


pipe = pipeline.Pipeline()

######
d = pipeline.array_dict(['data_fp', 'output_folder',
                        'trie_fp', 'min_occ', 'sample_percent', 'pivot_start',  'pivot_fp'])
pipe.add('gen_freq', gen_freq, d)
######
d = pipeline.array_dict(
    ['data_fp', 'trie_fp', 'output_folder', 'partial_break', 'break_fp', 'max_temp', 'n_start', 'seg_nrun'])
pipe.add('gen_seg', gen_seg, d)
######
d = pipeline.array_dict(['data_fp', 'break_fp', 'min_occ', 'word_fp'])
pipe.add('seg_word_count', seg_word_count, d)
######
d = pipeline.array_dict(['data_fp', 'break_fp', 'word_fp', 'matrix_fp'])
pipe.add('seg_matrix', seg_matrix, d)
######
d = pipeline.array_dict(
    ['matrix_fp', 'word_fp', 'reduced_matrix_fp', 'reduced_word_fp'])
pipe.add('reduce_word', reduce_word, d)
#####
d = pipeline.array_dict(
    ['reduced_matrix_fp', 'pca_dim', 'word_embed_fp'])
pipe.add('calc_pca', calc_pca, d)
#####
d = pipeline.array_dict(
    ['word_embed_fp', 'cluster_fp'])
pipe.add('cluster', cluster, d)
#####
d = pipeline.array_dict(
    ['reduced_matrix_fp', 'topic_fp','itnum','topic_con_fp'])
pipe.add('find_topic', find_topic, d)


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
    'n_start': 20,
    'max_temp': 2,
    'seg_nrun': 20,
    'break_fp': 'output/break.dump',

    'word_fp': 'output/word.dump',
    'matrix_fp': 'output/matrix.dump',
    'reduced_matrix_fp': 'output/rmatrix.dump',
    'reduced_word_fp': 'output/rword.dump',

    'pca_dim': 64,
    'word_embed_fp': 'output/embed.dump',
    'cluster_fp': 'output/cluster.dump',
    'topic_fp': 'output/topic.dump',
    'itnum':700,
    'topic_con_fp':'output/lda12.dump'
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
    'n_start': 0,
    'max_temp': 2,
    'seg_nrun': 20,
    'break_fp': 'spike/garbage/break.dump',

    'word_fp': 'spike/garbage/word.dump',
    'matrix_fp': 'spike/garbage/matrix.dump',
    'reduced_matrix_fp': 'spike/garbage/rmatrix.dump',
    'reduced_word_fp': 'spike/garbage/rword.dump',

    'pca_dim': 64,
    'word_embed_fp': 'spike/garbage/embed.dump',
    'dist_fp': 'spike/garbage/wdist.dump',
    'cluster_fp': 'spike/garbage/cluster.dump',
    'topic_fp':'spike/garbage/topic.dump',
    'itnum':50,
    'topic_con_fp':None

}


pipe.set_config(config)
pipe.validate()
pipe.run_from('find_topic')


# pipe.set_config(config_small)
# pipe.validate()
# pipe.run_one('find_topic')

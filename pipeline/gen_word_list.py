# generate term doc matrix
import filepickle
from StatTool.trie import Trie


def gen_word_list(trie_fp, ntrie_fp, word_fp):
    print('generating word list')
    trie: Trie = filepickle.load(trie_fp)
    trie.exact_net()
    filepickle.dump(trie, ntrie_fp)
    res = []

    def f(node, s):
        if node.valid:
            res.append(s)
        return
    trie.traverse('', f)
    filepickle.dump(res, word_fp)


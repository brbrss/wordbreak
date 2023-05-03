import filepickle
from StatTool.ldavi import Ldavi

ncluster = 128

def find_topic(reduced_matrix_fp, topic_fp):
    print('lda clustering')
    data = filepickle.load(reduced_matrix_fp)
    lda = Ldavi(data, ncluster)
    for i in range(40):
        print('round ',i)
        lda.update()
    obj = (lda.nu, lda.beta)
    filepickle.dump(obj, topic_fp)

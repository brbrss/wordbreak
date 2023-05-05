import filepickle
from StatTool.ldavi import Ldavi
import os.path

ncluster = 128


def find_topic(reduced_matrix_fp, topic_fp, topic_con_fp=None):
    print('lda clustering')
    data = filepickle.load(reduced_matrix_fp)
    lda = Ldavi(data, ncluster)
    start = 0
    if topic_con_fp:
        obj = filepickle.load(topic_con_fp)
        lda.nu, lda.beta = obj
        s = os.path.basename(topic_con_fp)
        try:
            start = int(s.split('.')[0][3:])+1
            print('starting from', start)
        except Exception:
            pass

    itnum = 300
    for i in range(start, 40):
        print('round ', i)
        itnum = lda.update_random(itnum)
        obj = (lda.nu, lda.beta)
        fp = os.path.join(os.path.dirname(topic_fp), 'lda'+str(i)+'.dump')
        filepickle.dump(obj, fp)
    obj = (lda.nu, lda.beta)
    filepickle.dump(obj, topic_fp)

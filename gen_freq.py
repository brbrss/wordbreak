import pickle
from StatTool.ngram import CorpusModel

from ParseTool.model import ThreadModel

f = open('post.pickle', 'rb')
data = pickle.load(f)
f.close()

cm = CorpusModel()
text_key = {}
count = 0
for tid in data:
    t = data[tid]
    cm.feed(t.title)
    for i in range(len(t.post_list)):
    #     pid = tid, i
    #     content = t.post_list[i].content
    #     cm.feed(content)
    #     text_key[count] = tid, i
        count += 1
del data

#with open('key.dump', 'wb') as f:
#    pickle.dump(text_key, f)

# cm.proc() # memory error

#def dump_pivot(pivot):
#    for key in pivot:

def do_batch():
    cm._sort()

# MAX_ENTRY = 100
# count = 0
# for i in range(len(cm.data)):
#     for j in range(len(cm.data[i])):
#         k = i, j
#         cm.pivot.append(k)
#         count += 1
#         if count >MAX_ENTRY:
#             do_batch()


print('no. of pots: ',count)
# cm.proc()
# ftable = cm.freq_table(20)
# with open('test/ftt.dump', 'wb') as f:
#     pickle.dump(ftable, f)
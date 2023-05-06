import json

f = open('output/show/user.json','r',encoding='utf-8')
data =json.load(f)
f.close()


f = open('output/show/user.txt','w',encoding='utf-8')
for i in data:
    item = data[i]
    f.write('='*80+'\n')
    
    f.write('user '+str(i))
    f.write(' len: '+str(item['len']))
    f.write('\n')

    f.write('clusters: ')
    f.write(', '.join([str(k) for k in item['clu'][:10]]))
    f.write('\n')

    f.write('words: \n')
    w =[repr(t)[1:-1] for t in item['word']]
    f.write(' '.join(w))
    f.write('\n')
f.close()

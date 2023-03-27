import pickle
import math
#from norm import gauss

def sub_str(s,i):
    ''' All substrings of s with length i'''
    if i==0:
        return []
    r = len(s)
    i = r - i
    L = [s[j:r-i+j] for j in range(i+1)]
    return L

def deduct(table,s,num):
    ln = len(s)
    table[ln][s] -= num
    if ln == 1:
        return None
    sub = sub_str(s,ln-1)
    for s in sub:
        deduct(table,s,num)
    return None
    
def proc_table(table):
    maxlen = len(table)
    L = range(maxlen)
    L.reverse()
    for i in L:
        d = table[i] 
        garbage = []        
        for k in d:
            if d[k] < 10:
                #to be removed
                garbage.append(k)
            else:
                # k is string
                sub = sub_str(k,i-1)
                for s in sub:
                    # s is substring of k                        
                    # remove double counting from substr
                    num = table[i-1][s]
                    if d[k] > num * 0.3:
                        deduct(table,s,d[k])
        for k in garbage:
            d.pop(k)     
    return table
    
def score(x,m,y,n):
    x = float(x)
    y = float(y)
    m = float(m)
    n = float(n)
    
    t1 = x/m
    t2 = y/n
    tt = (x+y)/(m+n)
    
    u = t1-t2
    i = tt*(1-tt)*(1/m+1/n)
    return u/math.sqrt(i)    
    
def word_score(d1,d2,m,n):
    table = {}
    #m = d1.len
    #n = d2.len
    i = 0
    for d in d1:
        for w in d:
            x = d1.get(i,w)
            y = d2.get(i,w)
            z = score(x,m,y,n)
            #p = gauss(z)
            table[w] = z
        i += 1
       
    i = 0 
    for d in d2:
        for w in d:
            if w not in table:
                x = d1.get(i,w)
                y = d2.get(i,w)           
                z = score(x,m,y,n)
                #p = gauss(z)
                table[w] = z
        i += 1
    return table


dic = {'B': [['C', 'C'], ['b']],
       'C': [['A', 'B'], ['a']],
       'A': [['B', 'A'], ['a']],
       'S': [['A', 'B'], ['B', 'C']]}

palabra = ['a','b']

T = {}
m = len(palabra)


def o(dic, t):
    res = []
    for key, l in dic.items():
        for value in l:
            if t in value:
                res.append(key)
    return res


for j in range(m):
    T[(j, j)] = o(dic, palabra[j])


def t(cel1, cel2, dic):
    sol = []
    combs = []
    #print(cel1,cel2)
    for i in range(len(cel1)):
        for j in range(len(cel2)):
            combs.append([cel1[i], cel2[j]])
    #print(combs)
    for key, values in dic.items():
        for comb in combs:
            if comb in values:
                sol.append(key)
                break
    return sol


def comb(i, j):
    res = []
    #print(i,j)
    for h in range(i, j):
        pos_sol = t(T[i, h], T[h + 1, j], dic)
        #print(pos_sol)
        for x in pos_sol:
            if x not in res:
                res.append(x)
        #print('pos',(i,j,((i,h),(h+1,j))),pos_sol)

    return res


for j in range(1, m + 1):
    for i in range(m):
        if i + j > m - 1:
            break
        else:
            T[(i, i + j)] = comb(i, i + j)


E=False
for x in T[(0,m-1)]:
    if x=='S':
        E=True
print(E)


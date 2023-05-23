from itertools import product
S,A,B,X,R = 0,1,2,3,4
rules = {'a':set([S,B,X]), 
         'b':set([S,B]), 
         (X,A): set([S]), 
         (A,X):set([S,B]), 
         (R,B): set([A]), 
         (X,B):set([R])}

#nt_rules = {0: ('S','XA','AX'),1:('A','RB'),2:('B','AX'),3:('X'),4:('R','XB')}
word = 'aaba' 

class Dynamic_CKY:
    
    def __init__(self, rules):
        self.rules = rules
        self.amount_rules = 5
    
    def test_word(self, word):
        self.word = word
        self.length = len(word)
        self.build_table()
        return 0 in self.table[0][0]

    def build_table(self):
        self.table = [[set() for p in range(self.length)]for i in range(self.length)]
        # We make sure the grammar can generate the terminals
        for terminal in range(self.length):
            self.table[self.length-1][terminal] = self.rules[word[terminal]]
        for i in range(self.length-2,-1, -1): # fila
            for j in range(0,i+1,1): # columna
                i1, j1 = self.length-1, j
                i2, j2 = i+1, j+1
                while i1 > i:
                    # Fer combinacions
                    for combi in self.combination((i1,j1),(i2,j2)):
                        if combi in rules:
                            if (rules[combi]) == 1: self.table[i][j].add(rules[combi]) 
                            else : self.table[i][j].update(rules[combi]) 
                    i1, i2, j2 = i1-1, i2+1, j2+1 
  
    def combination(self, cell1, cell2):
        return list(product(self.table[cell1[0]][cell1[1]], self.table[cell2[0]][cell2[1]]))

cky = Dynamic_CKY(rules)
cky.test_word(word = word)
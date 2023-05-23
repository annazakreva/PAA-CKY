from itertools import product
S,A,B,X,R = 0,1,2,3,4
t_rules = [['a','b'],[],['a','b'],['a'],[]]
non_t_rules = [[(X,A),(A,X)],[(R,B)],[(A,X)],[],[(X,B)]]
word = 'aaba'

class Rule:

    def __init__(self, head, body):
        
class Dynamic_Chomsky:
    
    def __init__(self, non_t_rules, t_rules):
        self.non_t_rules = non_t_rules
        self.t_rules = t_rules
        self.amount_rules = len(t_rules)
    
    def test_word(self, word):
        self.word = word
        self.length = len(word)
        self.build_table()
        return self.table[0][0][0]

    def build_table(self):
        self.table = [[[False for _ in range(self.amount_rules)] for p in range(self.length)]for i in range(self.length)]
        # We make sure the grammar can generate the terminals
        for terminal in range(self.length):
            for i_rule, rule in enumerate(self.t_rules):
                self.table[self.length-1][terminal][i_rule] = True if word[terminal] in rule else False
        for i in range(self.length-2,-1, -1): # fila
            for j in range(0,i+1,1): # columna
                for i_rule, rule in enumerate(self.non_t_rules):
                    for opt in rule:
                        i1, j1 = self.length-1, j
                        i2, j2 = i+1, j+1
                        while i1 > i and not self.table[i][j][i_rule]:
                            if self.table[i1][j1][opt[0]] and self.table[i2][j2][opt[1]]:
                                self.table[i][j][i_rule] = True
                            i1, i2, j2 = i1-1, i2+1, j2+1 
    
    def 
  

cky = Dynamic_Chomsky(non_t_rules=non_t_rules, t_rules=t_rules)
print(cky.test_word(word = word))
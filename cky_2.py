from itertools import product

class Dynamic_CKY:
    
    def __init__(self, rules, grammar):
        self.grammar = grammar
        self.rules = rules
        self.amount_rules = 5

    def read_file(self):
        '''
        This function is used to read a '.txt' file containing the rules of a certain grammar.
        '''
        # Open the file in read mode using the file name
        with open(self.grammar, 'r') as file:
            # Read the contents of the file and save them as a class variable
            contents = file.read()
            return contents

    def convert_grammar(self):
        ''' 
        Converts the grammar rules into the format the class works with.
        Args:
            self.contents('.txt' file): grammar rules 
        Generates:
            encoding_dict(dictionary): Encoding used for the rules, where the key is the head of the rule and the body is the numerical encoding used.
            self.t_rules(list): Grammar rules, considering only the ones that derive terminals. 
            self.nt_rules(list): Grammar rules, considering only the ones that derive non-terminals.
        '''
        grammar = self.read_file() #Reading the grammar file
        # Split the grammar string into separate lines
        grammar_lines = grammar.strip().split('\n')
        #encoding the rules: each rule name will be encoded with a number from 0 to the amount of rules-1
        self.encoding_dict, encoding = {}, 0 # Creating an empty dictionary to store the rules and initializing the encoding
        for line in range(len(grammar_lines)):
            self.encoding_dict[grammar_lines[line][0]] = encoding
            encoding += 1
        #Creating a list for each type of rule (terminal and non-terminal). The index states the head code and the content its body
        self.t_rules, self.nt_rules = [[] for _ in range(encoding)], [[] for _ in range(encoding)]
        for line in grammar_lines: # Process each line of the grammar
            head, elements = line.split(' → ') # Splitting the line into the head and elements of the rule
            values = elements.split(' | ') # Splitting the elements using "|" as the separator, for the cases of 'OR' statements
            for element in values: 
                if element.isupper(): #it's a non-terminal
                    #Creating a tuple so that 'AB' ~ ('A','B'), for future implementation use
                    tuple_form = (self.encoding_dict[element[0]],self.encoding_dict[element[1]]) 
                    self.nt_rules[self.encoding_dict[head]].append(tuple_form)
                else: #is a terminal
                    self.t_rules[self.encoding_dict[head]].append(element)
    
    def test_word(self, word):
        ''' 
        Tests a certain word for the processed grammar.
        Input:
            word(string): The word to check by the CKY.
        Returns:
            boolean: True or False according to belonging to the grammar.
        Example:
            >>> cky = Dynamic_CKY(grammar)
            >>> cky.test_word('aabab')
            True
        '''
        self.word = word
        self.length = len(word)
        self.build_table()
        
    def build_table(self):
        '''
        Builds the table for the dynamic programming version of the CKY.
        Input:
            self.contents('.txt' file): Grammar rules.
            self.word(string): The word to check by the CKY. 
        Returns:
            self.table(list): Table with the derivation rules of the given word for the corresponding grammar.
        '''
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
from itertools import product
import nltk
import time




GRAMMAR_FILE = 'grammarPLH.txt'
WORD = 'hwshmiht'


class Node:

    def __init__(self, parent, child1,prob = None, child2 = None):
        self.parent =  parent
        self.probability = prob
        self.child1 = child1
        self.child2 = child2

    def __repr__(self) -> str:
        return f"Pointer parent {self.parent}"
    
class Dynamic_CKY:
    
    def __init__(self, grammar_file, timing = False, prob=False):
        self.grammar = grammar_file
        self.timing = timing
        initial_time = time.time()
        self.convert_grammar(prob) # We convert grammar file to grammar
        if self.timing:
            print("Time taken to convert grammar:", '{:.10f}'.format(time.time()-initial_time))
        self.amount_rules = len(self.t_rules) # Save number of rules

    def read_file(self):
        '''
        This function is used to read a '.txt' file containing the rules of a certain grammar.
        '''
        # Open the file in read mode using the file name
        with open(self.grammar, 'r', encoding='utf-8') as file:
            # Read the contents of the file and save them as a class variable
            contents = file.read()
            return contents

    def convert_grammar(self, prob):
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
        print('input',grammar_lines)
        #encoding the rules: each rule name will be encoded with a number from 0 to the amount of rules-1
        self.encoding_dict, encoding = {}, 0 # Creating an empty dictionary to store the rules and initializing the encoding
        for line in range(len(grammar_lines)):
            self.encoding_dict[grammar_lines[line][0]] = encoding
            self.encoding_dict[encoding] = grammar_lines[line][0]
            encoding += 1
        #Creating a list for each type of rule (terminal and non-terminal). The index states the head code and the content its body
        self.t_rules, self.nt_rules = [[] for _ in range(encoding)], [[] for _ in range(encoding)]
        if prob: #Creating the same mirrored lists for their corresponding probabilities
            self.t_probs, self.non_t_probs =  [[] for _ in range(encoding)], [[] for _ in range(encoding)]
        for line in grammar_lines: # Process each line of the grammar
            head, elements = line.split(' → ') # Splitting the line into the head and elements of the rule
            values = elements.split(' | ') # Splitting the elements using "|" as the separator, for the cases of 'OR' statements
            for element in values: 
                if element.isupper(): #it's a non-terminal
                    #Creating a tuple so that 'AB' ~ ('A','B'), for future implementation use
                    tuple_form = (self.encoding_dict[element[0]],self.encoding_dict[element[1]]) 
                    self.nt_rules[self.encoding_dict[head]].append(tuple_form)
                    if prob:
                        #Appending the probability for each tuple in its corresponding place in the probability list
                        self.non_t_probs[self.encoding_dict[head]].append(float(element[3:7]))
                else: #is a terminal
                    self.t_rules[self.encoding_dict[head]].append(element[0])
                    #Appending the probability for the terminals
                    if prob: 
                        self.t_probs[self.encoding_dict[head]].append(float(element[2:6]))
    
   

    def test_word(self, word, visual = True, prob=False):
        ''' 
        Tests a certain word for the processed grammar.
        Input:
            word(string): The word to check by the CKY.
            visual: Boolean (True if output is visual parse tree)
            prob: Boolean (True if taking into consideration probability is wanted)
        Returns:
            boolean: True or False according to belonging to the grammar.
        Example:
            >>> cky = Dynamic_CKY(grammar)
            >>> cky.test_word('aabab')
            True
        '''
        initial_time = time.time()
        self.word = word
        self.length = len(word)
        if prob:
            self.build_table_prob()
        else:
            self.build_table()
        mid_time = time.time()
        if self.timing:
            print("Time taken to check word",'{:.10f}'.format(mid_time-initial_time))
        if visual and self.table[0][0][self.encoding_dict['S']]: 
            tree = self.visualize_tree()
            if self.timing:
                print("Time taken to draw tree",'{:.10f}'.format(time.time()-mid_time))
            tree.draw()
            print(self.pointers)
        
        
        if prob:
            print(self.probabilities)

        return self.table[0][0][self.encoding_dict['S']]

    def build_table(self):
        '''
        Function used to test current word. It creates 2 tables:
        - table: Built as a table of nxn, where each element is a boolean list of amount_rules length. 
            If cell is True in the i position, then the ith rule can be applied there
        - pointers: Built as the previous table, it saves the nodes that connect the rules to visualize Parse Tree
        '''
        # Creation of tables
        self.table = [[[False for _ in range(self.amount_rules)] for p in range(self.length)]for i in range(self.length)]
        self.pointers = [[[None for _ in range(self.amount_rules)] for p in range(self.length)]for i in range(self.length)] 


        # Iteration of last row (for terminals)
        for terminal in range(self.length):
            for i_rule, rule in enumerate(self.t_rules):
                # Turn the i_rule index of this cell True if the letter is found the body of the i_rule rule
                self.table[self.length-1][terminal][i_rule] = True if self.word[terminal] in rule else False 
                # We create a pointer with the parent being the index of the rule, and the (only) child the letter
                self.pointers[self.length-1][terminal][i_rule] = Node(parent = i_rule, child1 = self.word[terminal])
    
        for i in range(self.length-2,-1, -1): # Iterating through rows
            for j in range(0,i+1,1): # Iterating through columns
                for i_rule, rule in enumerate(self.nt_rules): # Iterating through rules
                    for body in rule: # Iterating through different bodies in rules
                        # First possible cell combination
                        i1, j1 = self.length-1, j 
                        i2, j2 = i+1, j+1
                        while i1 > i and not self.table[i][j][i_rule]: # While we haven't tried all cell combinations and rule is still not True
                            if self.table[i1][j1][body[0]] and self.table[i2][j2][body[1]]: # If the body is True in the current combination 
                                self.table[i][j][i_rule] = True 
                                # Create pointer: Parent is rule index, and childs are the pointers of the cells we have used to apply the rule
                                self.pointers[i][j][i_rule] = Node(parent = i_rule, child1 = self.pointers[i1][j1][body[0]],child2=self.pointers[i2][j2][body[1]])

                            i1, i2, j2 = i1-1, i2+1, j2+1 

    def build_table_prob(self):
        '''
        Function used to test current word with the probability extension added. It creates 3 tables:
        - table: Built as a table of nxn, where each element is a boolean list of amount_rules length. 
            If cell is True in the i position, then the ith rule can be applied there.
        - pointers: Built as the previous table, it saves the nodes that connect the rules to visualize Parse Tree.
        - probabilities: Built as the previous table but with only one contianer per cell, it keeps the maximum probability achieved per cell if there's a feasible combination.
        '''
        # Creation of tables
        self.table = [[[False for _ in range(self.amount_rules)] for _ in range(self.length)]for _ in range(self.length)]
        self.pointers = [[[None for _ in range(self.amount_rules)] for _ in range(self.length)]for _ in range(self.length)]
        self.probabilities = [[0.0 for _ in range(self.length)] for _ in range(self.length)] 
        # Iteration of last row (for terminals)
        for terminal in range(self.length):
            max_prob, best_rule = 0.0, -1  # Initialize maximum probability and best rule index
            for i_rule, rule in enumerate(self.t_rules):
                for ind, p in enumerate(self.t_probs[i_rule]):
                    #Calculating highest probability per terminal
                    if self.t_rules[i_rule][ind] == self.word[terminal] and p > max_prob:
                        max_prob = p
                        best_rule = i_rule
            self.probabilities[self.length-1][terminal] = max_prob
            # Turn the i_rule index of this cell True if the letter is found the body of the i_rule rule and has maximum probability
            self.table[self.length-1][terminal][best_rule]= True
            # We create a pointer with the parent being the index of the rule, and the (only) child the letter
            self.pointers[self.length-1][terminal][best_rule] = Node(parent = best_rule, prob = max_prob, child1 = self.word[terminal])
        for i in range(self.length-2,-1, -1): # Iterating through rows
            for j in range(0,i+1,1): # Iterating through columns
                max_prob = 0.0  # Initialize maximum probability
                best_rule = -1  # Initialize best rule index
                for i_rule, rule in enumerate(self.nt_rules): # Iterating through rules
                    for i_body, body in enumerate(rule): # Iterating through different bodies in rules
                        # First possible cell combination
                        i1, j1 = self.length-1, j 
                        i2, j2 = i+1, j+1
                        while i1 > i: # While we haven't tried all cell combinations 
                            if self.table[i1][j1][body[0]] and self.table[i2][j2][body[1]]: # If the body is True in the current combination 
                                #Calculate the probability of the combination
                                prob = self.non_t_probs[i_rule][i_body] * self.probabilities[i1][j1] * self.probabilities[i2][j2]
                                #Checking if the probability is higher to what has been previously saved, if so save it
                                if prob > max_prob:
                                    max_prob = prob
                                    # Create pointer: Parent is rule index, and childs are the pointers of the cells we have used to apply the rule
                                    self.pointers[i][j][best_rule] = None
                                    self.pointers[i][j][i_rule] = Node(parent = i_rule, prob = prob, child1 = self.pointers[i1][j1][body[0]],child2=self.pointers[i2][j2][body[1]])
                                    best_rule = i_rule
                            i1, i2, j2 = i1-1, i2+1, j2+1 
                if best_rule > -1:#if there's a feasible combination 
                    self.probabilities[i][j] = max_prob  # Set the maximum probability for the current cell
                    # Only turning true the best rule
                    self.table[i][j][best_rule]= True
        print(self.table)
    
    def visualize_tree(self):
        '''
        Builds tree then draws it
        '''
        return self.build_tree(node=self.pointers[0][0][self.encoding_dict['S']])

    def build_tree(self, node):
        '''
        Starting off at parent node, it returns the tree by building it recursively
        '''
        print(node)
        if node.child2 is None: 
            return nltk.Tree(self.encoding_dict[node.parent]+f'({node.probability})', [node.child1])
        return nltk.Tree(self.encoding_dict[node.parent]+f'{node.probability}', [self.build_tree(node.child1), self.build_tree(node.child2)])



if __name__ == '__main__':
    cky = Dynamic_CKY(GRAMMAR_FILE, prob=True)
    print(cky.test_word(WORD,prob=True))
    
    

    
    
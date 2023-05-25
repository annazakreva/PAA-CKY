import string

grammar = 'grammar1.txt'
with open(grammar, 'r') as file:
    # Read the contents of the file and save them as a class variable
    contents = file.read()

def replace_letter(bodies, letter_to_combine):
    result = []
    for body in bodies:
        body = [letter for letter in body]
        if all([letter!=letter_to_combine for letter in body]):
            permutations = [''.join(body)]
        elif body != [letter_to_combine,letter_to_combine]:           
            permutations = []
            for combination in [letter_to_combine,None]:
                new_values = []
                for value in body:
                    if value == letter_to_combine: # If value is A (needs to be replaced)
                        if combination != None: # If it is not empty string, subtitute A with body
                            new_values.append(combination)   
                    else: # If it is not A, add value
                        new_values.append(value)
                permutations.append(''.join(new_values))
            else:
                if combination != None:
                    permutations.append(''.join(body))
        else:
            permutations = [letter_to_combine+letter_to_combine, letter_to_combine]
        result += permutations
    return result

def convert_grammar(grammar, cnf = True, prob=False):
    
    # Split the grammar string into separate lines
    grammar_lines = grammar.strip().split('\n')
    heads, bodies = [], []
    for rule_idx in range(len(grammar_lines)): # Process each line of the grammar
        line = grammar_lines[rule_idx]
        head, elements = line.split(' → ') # Splitting the line into the head and elements of the rule
        values = elements.split(' | ') # Splitting the elements using "|" as the separator, for the cases of 'OR' statements
        heads.append(head)
        bodies.append(values)

    print(heads)
    print(bodies)
    
    if cnf:
        alphabet = [letter for letter in string.ascii_uppercase if letter not in heads]
        i = 0
        while i < len(bodies):
            for element in range(len(bodies[i])):
                current_var = bodies[i][element]
                #step 1:
                ''' 
                Eliminate terminals from right side if they exist with other terminals or non-terminals
                e.g: production rule X->xY can be decomposed as:
                X->ZY
                Z->x
                '''
                if any(char.islower() for char in current_var) and len(current_var) > 1:
                    new_var = ''
                    for letter in range(len(current_var)):
                        if current_var[letter].islower():
                            new_letter = alphabet.pop(0)
                            heads.append(new_letter)
                            bodies.append([current_var[letter]])
                            new_var += new_letter
                        else:
                            new_var += current_var[letter]
                    bodies[i][element] = new_var
                
                current_var = bodies[i][element] #in case something has changed
                
                #step 2:
                '''
                Eliminate RHS with more than two non-terminals.
                e.g,; production rule X->LYZ can be decomposed as:
                X->LP
                P->YZ
                '''
                if len(current_var) > 2:
                    new_letter = alphabet.pop(0)
                    new_var = current_var[0] + new_letter #Change to two terminals
                    bodies[i][element] = new_var #change the body of the rule to a two terminals rule
                    heads.append(new_letter) #add new created rule to heads
                    bodies.append([current_var[1:]]) #add new rule (the rest of the body of the original one) to bodies 
                
                current_var = bodies[i][element] #in case something has changed    
            i+=1


        #step 3:
        '''
        Eliminate ε-rules
        e.g: a production rule can derive is nullable in two scenarios:
            - ε appears explicitly: A → ε or  A → a | ε 
            - the rule is implicitly nullable: A → B where B doesn't exist
        For purely nullable rules: all istances of the head are deleted
        For partially nullable rules: consider that all appearances of the rule as possible empty string 
        '''
        #Dealing with implicitly nullable rules A → B
        for body in range(len(bodies)):
            current_body = bodies[body]
            if 'ε' in current_body or ((len(current_body) == 1) and (current_body[0].isupper() and (len(current_body[0])==1)) ): # Rule is nullable
                if len(current_body) == 1 and current_body != 'ε': 
                    current_body == 'ε'
                    bodies[body][element] = 'ε' #we delete A → B
        
        #dealing with explicitly pure nullable rule A → ε
        for body in range(len(bodies)): 
            current_body = bodies[body]
            if 'ε' in current_body and len(current_body)==1:
                to_delete = heads[body] #Rule that should be deleted from other rules
                for rule in range(len(bodies)):
                    if bodies[rule]:
                        updated_rule = [element.replace(to_delete, '') for element in bodies[rule]] #delete all the heads appearences in each rule
                        bodies[rule] = updated_rule
                heads[body] = False
                bodies[body] = False
        
        #updating lists to delete the null rules
        bodies = [element for element in bodies if element != False]
        heads = [element for element in heads if element != False]

        #dealing with explicitly impure nullable rule A → a | ε 
        for body in range(len(bodies)):
            current_body = bodies[body]
            if len(current_body) > 1 and 'ε' in current_body: 
                current_body.remove('ε') #elements for the permutation
                bodies[body] = current_body #we update the rule so it doesn't have ε 
                #modify the production rules:
                null_head = heads[body]
                nulled_bodies = [] #list of bodies that contain the nullable rule
                for body2 in range(len(bodies)): #we find the heads of the elements that contain the nullable rule
                    for element in range(len(bodies[body2])):
                        if null_head in bodies[body2][element]: #if the nullable rule appears in some other rule
                            nulled_bodies.append(heads[body2]) 
                for nulled in nulled_bodies: #3.1 i 3.2
                    nulled_index = heads.index(nulled)
                    new_bodies = replace_letter(bodies[nulled_index], null_head)
                    bodies[nulled_index] = new_bodies
                    changed_rule = heads[nulled_index]
                    for body3 in range(len(bodies)):
                        if any(changed_rule in el for el in bodies[body3]):
                            new_bodies = replace_letter(bodies[body3], changed_rule)
                            bodies[body3] = new_bodies

        #step 4:
        '''
        Eliminate unit rules
        e.g: considering production rule A → B:
            if B → CD exists, original rule should be converted to  A → CD
        '''
        for body in range(len(bodies)):
            current_body = bodies[body]
            if ((len(current_body) == 1) and (current_body[0].isupper() and (len(current_body[0])==1)) ): # Rule is unitary
                if heads.index(bodies[body]):
                    actual_rule = bodies[heads.index(bodies[body])] #he look for B → CD, specifically CD
                    bodies[body] = actual_rule
        
        #step 5:
        '''
        Filter unitary rules that are left
        '''
        bodies = [[item for item in sublist if not (len(item) == 1 and item.isupper())] for sublist in bodies]


                       
             
    #encoding the rules: each rule name will be encoded with a number from 0 to the amount of rules-1
    encoding_dict, encoding = {}, 0 # Creating an empty dictionary to store the rules and initializing the encoding
    for line in range(len(heads)):
        encoding_dict[heads[line]] = encoding
        encoding += 1
            
    #Creating a list for each type of rule (terminal and non-terminal). The index states the head code and the content its body
    ter_rules, nter_rules = [[] for _ in range(encoding)], [[] for _ in range(encoding)]
    if prob: #Creating the same mirrored lists for their corresponding probabilities
            t_probs, non_t_probs =  [[] for _ in range(encoding)], [[] for _ in range(encoding)]
    for head,body in zip(heads, bodies): # Process each line of the grammar
        for element in body: 
            if element.isupper(): #it's a non-terminal
                #Creating a tuple so that 'AB' ~ ('A','B'), for future implementation use
                tuple_form = (encoding_dict[element[0]],encoding_dict[element[1]]) 
                nter_rules[encoding_dict[head]].append(tuple_form)
                if prob:
                        #Appending the probability for each tuple in its corresponding place in the probability list
                        non_t_probs[encoding_dict[head]].append(float(element[3:7]))
            else: #is a terminal
                
                #Appending the probability for the terminals
                if prob: 
                    ter_rules[encoding_dict[head]].append(element[0])
                    t_probs[encoding_dict[head]].append(float(element[2:6]))
                else:
                    ter_rules[encoding_dict[head]].append(element)
    if prob:
        return ter_rules, nter_rules, t_probs, non_t_probs
    else:
        return ter_rules, nter_rules


t_rules, nt_rules = convert_grammar(contents)
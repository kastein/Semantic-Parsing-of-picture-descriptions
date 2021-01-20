import nltk
from nltk import CFG
from nltk.grammar import Production
from nltk import Tree

"""
NOTE: don't recompute your rhs2lhs map for every sentence, that's just takes unnecessary time
NOTE: you compute all possible rhs1,rhs2 before checking whether there is a rule for this in the grammar.
NOTE: detour using fromstring: first built string representations of parse trees and only in the end built Trees from that.
NOTE: you had a lot of try-except statements and sometimes I don't think you can even run into the exceptions you tried to catch. Also: with try-except without further specifying the kind of Exception (e.g. IndexError, KeyError) you're trying to catch you can easily introduce bugs that are hard to find because you just don't catch one specific exception, but ANY exception. even the ones you haven't thought about.
"""

def cky_parser(sentence, grammar):
    """
    parses the input sentence with respect to the input grammar by running the cky algorithm 
    and storing backpointers from which the parse trees can be build
    sentence: a string 
    grammar: a grammar object for a grammar in cnf form
    returns: a dictionary with the backpointers to reconstruct the parse tree for the input sentence; 
    key = (A, start, end), value = (B, C, split) if B covered input string from start to start+split and C covered input string
    from start+split to end and there is a rule in the grammar A -> B C
    """
    # tokenize sentence by white space
    words = sentence.split()
    
    n = len(words)
    
    # create a dictionary for the chart
    table = dict()
    # create a dictionary for the backpointers
    backpointers = dict()
    
    # create dictionary with an entry for each right hand side B C in the grammar as key and as value the list of all 
    # left hand sides A for which A -> B C is a rule in the grammar (the same for rules A -> wi)
    # this dictionary prevents the need to loop over all rules to find the possible left hand sides inside the inner loop 
    rules_by_rhs = dict()
    for rule in grammar.productions():
        right = rule.rhs()
        left = rule.lhs()
        try:
            rules_by_rhs[right].append(left)
        except:
            rules_by_rhs[right] = [left]
    
    
    # fill in the cells in the table for the terminals / words
    # for each wi in the sentence 
    for i in range(0, n):
        w_i = words[i]
        production_rules = grammar.productions(rhs=w_i)
        
        # if there is a unknown word in the sentence return an empty dict because no parse tree can be built for the sentence
        if production_rules == []:
            return dict()
        
        table[(i,i+1)] = set()
        # and for each rule A -> wi in the grammar
        for rule in production_rules:
            left = rule.lhs()
            # add A to the cell
            table[(i,i+1)].add(left)
            
            # store backpointers, e.g. that the non-terminal A covering the word from i to i+1 came from the word wi
            try:
                backpointers[(left,i,i+1)].append((w_i,))
            except:
                backpointers[(left,i,i+1)] = [(w_i,)]
    
    
    # fill the rest of the cells from left to right and bottom-up
    # for each substring of the sentence with length = width
    for width in range(2, n+1):
        
        # for each start index of this substring
        for start in range(0, n-width+1):
            table[(start, start+width)] = set() 
            
            # for each possible index split where the substring from start with length width can be splitted
            for split in range(start+1, start+width):  
                
                possible_rhs = [(rhs_1, rhs_2) for rhs_1 in table[(start,split)] for rhs_2 in table[(split, start+width)]]
                for (rhs_1, rhs_2) in possible_rhs:
                    
                     # and for all rules A -> B C in the grammar
                    try:
                        for lhs in rules_by_rhs[(rhs_1, rhs_2)]:
                            
                            # add A to the cell corresponding to the substring starting at start with length width
                            table[(start, start+width)].add(lhs)
                            
                            # store backpointers: backpointer for A from start with length width is the triple (B, C, split) 
                            # for each A -> B C that was used to fill A into the chart 
                            try:
                                backpointers[(lhs, start, start+width)].append((rhs_1, rhs_2, split))
                            except:
                                backpointers[(lhs, start, start+width)] =[(rhs_1, rhs_2, split)]
                            
                    # if there is no rule with right hand side B C nothing can be added 
                    except:
                        continue

    
        
    return backpointers




def compute_parse_trees(sentence_list, grammar):
    """
    parses the input sentences with respect to the input grammar using the cky parser and 
    returns all parse trees for each sentence which are computed using the build_tree_string function
    sentence_list: list containing the sentences that should be parsed as strings
    grammar: a grammar object in cnf format
    returns: dictionary with the parse trees (Tree objects) for each of the input sentences; 
    key = sentence, value = list of parse trees
    """
    
    parse_trees = dict()
    
    for sentence in sentence_list:
        
        # run the cky parser for each single sentence
        backpointers = cky_parser(sentence, grammar)
        
        # initialize the entry in the dictionary for the current sentence with an empty list
        parse_trees[sentence] = []
        
        # get the start point for following the backpointers top down which is the start symbol covering the whole sentence
        length = len(sentence.split())
        start = grammar.start()
        start_point = (start, 0, length)
        
        # call build_tree_string to get a list with all parse trees in string format 
        all_parses = build_tree_string(start_point, backpointers)
        
        # convert each string for the parse tree to an actual tree object and add it to the dictionary entry for the current sentence
        for tree_string in all_parses:
            parse_tree = Tree.fromstring(tree_string)
            parse_trees[sentence].append(parse_tree)

    
    
    return parse_trees




def build_tree_string(current, backpointers):
    """
    recursively builds the string representation for the tree 
    current: the triple consisting of (Nonterminal, start_index, end_index) for which the trees with the root Nonterminal that 
    covers the input from start_index to end_index should be build based on the information in the backpointers
    backpointers: the dictionary with the backpointers 
    returns: all possible trees with root Nonterminal covering start_index to end_index
    """
    
    current_label = current[0]
    current_start = current[1]
    current_end = current[2]
    
    sub_trees = []
    
    # if at leaves, e.g. current = (NP,0,1) and backpointer[(NP,0,1)] = [(elephant,)]
    # then the string representation looks like "(NP elephant)""
    if current_end - current_start == 1:
        leaf = backpointers[current]
        tree_string = "(" + str(current_label) + " " + leaf[0][0] + ")"
        sub_trees.append(tree_string)
    
    # for all other cases, e.g. current = (S,0,7) and backpointer[(S,0,7)] = [(NP,VP,1), ...]
    # then the string representation for the first element looks like 
    # "(S string_repr_NP_0_1 string_repr_VP_1_7)" -> "(S (NP elephant) (VP ...))"
    else:
        
        # if there is no backpointer indicating how current was derived the empty list is returned as no parse tree can be build
        # by the way in which backpointers are created this only happens if there is no backpointer for the start symbol (-> no parse tree at all)
        try:
            possible_children = backpointers[current]
            
        except:
            return[]
        
        # each possible pairing of 2 subtrees is build recursively 
        for pointer in possible_children:
            child_1 = pointer[0]
            child_2 = pointer[1]
            split = pointer[2]
            left_subtrees = build_tree_string((child_1, current_start, split), backpointers)
            right_subtrees = build_tree_string((child_2, split, current_end), backpointers)
            
            for left in left_subtrees:
                for right in right_subtrees:
                    
                    # and for each of the possible left and right subtrees pairings a tree string is added to the sub_trees list
                    tree_string = "(" + str(current_label) + " " + left + " " + right + ")"
                    sub_trees.append(tree_string)
                    
    return sub_trees




def compute_number_parses(sentence_list, grammar, output):
    """
    does the same as compute_parse_trees (parse the input sentences using cky and compute all possible parse trees) 
    and additionally outputs the number of parse trees for each of the input sentences 
    and writes each sentence and the number of its parse trees (separated by tab) in a file 
    sentence_list: list of sentences as strings
    grammar: a grammar object in cnf format
    output: the path to the output file
    returns: a dictionary with the number of parses for each input sentence; key = sentence, value = (number of parses, [all parse trees]
    """
    
    # compute all parse trees for each input sentence 
    parse_trees = compute_parse_trees(sentence_list, grammar)
    number_p = dict()
    
    with open(output, "w", encoding="utf-8") as o:
        for sentence in sentence_list:
            parses = parse_trees[sentence]
            # as parses is a list of all possible parse trees for the current sentence the number of parses is simply its length
            number_parses = len(parses)
            o.write(sentence + "\t" + str(number_parses) + "\n")
            number_p[sentence] = (number_parses, parses)
            
    return number_p

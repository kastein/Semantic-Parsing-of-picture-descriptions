#!/usr/bin/env python

"""

"""


"""
To see how the implementation works, it's probably easiest to study
gold_lexicon, rules, and functions below. Together, these implement
the example in table 1.

To create new grammars, you just need to define the following:

* A lexicon mapping strings to arrays of tuples, where the tuples
  are (category, logical form) pairs.

* A set of rules, each a list [X, Y, Z, (a,b)], where X is the left
  daughter category, Y is the right daughter category, Z is the 
  mother category, and (a,b) says which order of application to
  use in the semantics: (0,1) means apply X to Y, and (1,0)
  means apply Y to X.

* A set of Python functions that will interpret the logical forms
  (second members of all the nonterminal node labels).  If your
  logical forms can be intepreted in native Python this can be 
  empty.
"""

__author__ = "Christopher Potts and Percy Liang"
__credits__ = []
__license__ = "GNU general public license, version 2"
__version__ = "2.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the authors' websites"


import sys
from collections import defaultdict
from itertools import product

# variable to store all blocks of the current picture
allblocks = []
# variable to store the guessed blocks for an input utterance
guessed_blocks = set()
# only needed when running this script separately for demo or testing purpose
all_blocks_grid = []



def create_all_blocks(picture):
    """
    updates the allblocks by resetting and then adding all blocks of the Picture object
    :param picture: a Picture object as defined in BlockPictureGenerator.py
    :return: None
    """
    allblocks.clear()
    grid = picture.grid
    for row in grid:
        for b in row:
            if b:
                allblocks.append(b)            
    return None
    

def position_test(blocks,block_locations,position):
    """
    finds all pairs of blocks b1 form blocks and b2 from blocklocations that stand in relation position to eachother
    e.g. blocks is a list of all blue rectangles and block_locations a list of all red circles and position is 'u'
    then the function returns all blocks that are blue rectangles and are below red circles
    additionally updates guessed blocks by removing all blocks from guessed_blocks that do not match, e.g. removes all
    blue rectangles that are not below a red circle and removes all red circles that are not above a blue rectangle
    :param blocks: list of blocks
    :param block_locations: list of blocks
    :param position: string for the relative position
    :return: list of all blocks from blocks that stand in relation position to any block in block_locations
    """
    fulfill = []
    checked = set()
    passed_check = set()

    for b1 in blocks:
        for b2 in block_locations:
            checked.add(b1)
            checked.add(b2)
            
            if position == "u":
                if b1.y > b2.y:
                    fulfill.append(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

            elif position == "o":
                if b1.y < b2.y:
                    fulfill.append(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)
 
            elif position == "n":
                if b1.y == b2.y and (b1.x == b2.x+1 or b1.x == b2.x-1):
                    fulfill.append(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

            elif position == "l":
                if b1.x < b2.x:
                    fulfill.append(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)
 
            elif position == "r":
                if b1.x > b2.x:
                    fulfill.append(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

    for bl in checked:
        if bl not in passed_check:
            guessed_blocks.remove(bl)
        
    return fulfill
    

def block_filter(conditions,blocks):
    """
    returns a list of all blocks that match the specific conditions and updates guessed_blocks by adding those blocks
    :param conditions: list of conditions, e.g. shape == rectangle or color == green
    :return: a list of all blocks in blocks that fulfill the conditions
    """
    fulfill = []
    for b in blocks:
        test = True
        for c in conditions:
            test = test and c(b)
        if test:
            fulfill.append(b)
    guessed_blocks.update(fulfill)
    return fulfill




class Grammar:

    def __init__(self, lexicon, rules, functions):
        """For examples of these arguments, see below."""
        self.lexicon = lexicon
        self.rules = rules
        self.functions = functions
        self.backpointers = defaultdict(list)

    def recursive_treebuild(self,current):
        #print("current",current)
        current_label = current[0]
        current_start = current[1]
        current_end = current[2]
        sub_trees = []
        if current_end - current_start == 1:
            leaf = self.backpointers[current]
            tree = [current_label,leaf]
            sub_trees.append(tree)
        else:
            possible_children = self.backpointers[current]
            for pointer in possible_children:
                #print(pointer,len(pointer))
                child1 = pointer[0]
                child2 = pointer[1]
                k = pointer[2] # split in Katharinas Code
                left_subtrees = self.recursive_treebuild((child1,current_start,k))
                right_subtrees = self.recursive_treebuild((child2,k,current_end))
                
                for left in left_subtrees:
                    for right in right_subtrees:
                        tree = [current_label,[left,right]]
                        sub_trees.append(tree)

        return sub_trees
                

    def compute_parse_trees(self,n):
        #start_point = ('V',0,n)
        parse_trees = []
        #for i in backpointers:
            #print("key",i,backpointers[i])
        for l,x,y in self.backpointers:
            if l[0]=="V" and x == 0 and y==n:
                parse_trees += self.recursive_treebuild((l,x,y))
        return parse_trees
        

    def gen(self, s):
        """CYK parsing, but we just keep the full derivations. The input
        s should be a string that can be parsed with this grammar."""
        words = s.split()
        n = len(words)+1
        trace = defaultdict(set)
        self.backpointers = defaultdict(list)
        
        for i in range(1,n):
            word = words[i-1]
            for syntax,semantic in self.lexicon[word]:
                trace[(i-1,i)].add((syntax,semantic))
                self.backpointers[((syntax,semantic),i-1,i)].append(word)
        for j in range(2, n):
            for i in range(j-1, -1, -1):
                for k in range(i+1, j):
                    for c1, c2 in product(trace[(i,k)], trace[(k,j)]):
                        for lfnode in self.allcombos(c1,c2):
                            trace[(i,j)].add(lfnode)
                            #print(c1,c2)
                            self.backpointers[(lfnode,i,j)].append((c1,c2,k))
        # Return only full parses, from the upper right of the chart:
        #return buildtrees(trace[(0,n-1)])
        return self.compute_parse_trees(n-1)
    

    def allcombos(self, c1, c2):
        """Given any two nonterminal node labels, find all the ways
        they can be combined given self.rules."""
        results = []
        for left, right, mother, app_order in self.rules:
            if left == c1[0] and right == c2[0]:
                sem = [c1[1], c2[1]]
                results.append((mother, "{}({})".format(
                    sem[app_order[0]], sem[app_order[1]])))
        return results

    def sem(self, lf):
        """Interpret, as Python code, the root of a logical form
        generated by this grammar."""
        # Import all of the user's functions into the namespace to
        # help with the interpretation of the logical forms.
        grammar = sys.modules[__name__]
        for key, val in list(self.functions.items()):
            setattr(grammar, key, val)
        return eval(lf[0][1]) # Interpret just the root node's semantics. 


# The lexicon for our pictures
gold_lexicon = {
    'form':[('B','[]')],
    'forms':[('B','[]')],
    'square': [('B','[(lambda b: b.shape == "rectangle")]')],
    'squares': [('B','[(lambda b: b.shape == "rectangle")]')],
    'triangle': [('B','[(lambda b: b.shape == "triangle")]')],
    'triangles': [('B','[(lambda b: b.shape == "triangle")]')],
    'circle': [('B','[(lambda b: b.shape == "circle")]')],
    'circles': [('B','[(lambda b: b.shape == "circle")]')],
    'green':[('C','green')],
    'yellow':[('C','yellow')],
    'blue':[('C','blue')],
    'red':[('C','red')],
    'there':[('E','exist')],
    'is':[('I','identy')],
    'are':[('I','identy')],
    'a':[('N','range(1,17)')],
    'one':[('N','[1]')],
    'two':[('N','[2]')],
    'three':[('N','[3]')],
    'under':[('U','under')],
    'over':[('U','over')],
    'and':[('AND','und')],
    'next':[('NEXT', 'next')],
    'to':[('TO', 'to')],
    'of':[('TO', 'to')],
    'left':[('LR', 'left')],
    'right':[('LR', 'right')],
    'the':[('THE', 'the')]

}

# The binarized rule set for our pictures
# The second rule corresponds to:
# EN -> E N  semantics: apply E(N)
rules = [
    ['C', 'B', 'B', (0,1)],
    ['E','N','EN',(0,1)],
    ['E','I','E',(1,0)],
    ['EN','B','V',(0,1)],
    ['EN','BS','V',(0,1)],
    ['U','N','POS',(0,1)],
    ['PP','N','POS',(0,1)],
    ['POS','B','L',(0,1)],
    ['POS','BS','L',(0,1)],
    ['B','L','BS',(1,0)],
    ['V','AND','VAND',(1,0)],
    ['VAND','V','V',(0,1)],
    ['NEXT','TO','PP',(1,0)],
    ['TS','SIDE','PP',(0,1)],
    ['TO','THE','TS',(0,1)],
    ['LR','TO','SIDE',(1,0)]
]

# These are needed to interpret our logical forms with eval. They are
# imported into the namespace Grammar.sem to achieve that.
functions = {
    'block': (lambda conditions: (lambda number_requirement: (number_requirement,conditions))),
    'identy': (lambda x: x),
    'exist': (lambda n : (lambda b: len(block_filter(b, allblocks)) in n)),
    'und':(lambda v1:(lambda v2: v1 and v2)),
    'blue': (lambda x: x+[(lambda b:b.colour=="blue")]),
    'red': (lambda x: x+[(lambda b:b.colour=="red")]),
    'green': (lambda x: x+[(lambda b:b.colour=="green")]),
    'yellow':(lambda x: x+[(lambda b:b.colour=="yellow")]),
    'under':(lambda n: (lambda x:(lambda y: [(lambda b: len(position_test(block_filter(y, allblocks), block_filter(x,allblocks),
                                                                          "u")) in n and b in position_test(
        block_filter(
            y, allblocks), block_filter(x, allblocks), "u"))]))),
    'over':(lambda n: (lambda x:(lambda y: [(lambda b: len(position_test(block_filter(y, allblocks), block_filter(x,allblocks),
                                                                         "o")) in n and b in position_test(block_filter(
        y, allblocks), block_filter(x, allblocks), "o"))]))),
    'next':(lambda n: (lambda x:(lambda y: [(lambda b: len(position_test(block_filter(y, allblocks), block_filter(x, allblocks),
                                                                         "n")) in n and b in position_test(block_filter(
        y, allblocks), block_filter(x, allblocks), "n"))]))),
    'left':(lambda n: (lambda x:(lambda y: [(lambda b: len(position_test(block_filter(y, allblocks), block_filter(x,allblocks),
                                                                         "l")) in n and b in position_test(block_filter(
        y, allblocks), block_filter(x, allblocks), "l"))]))),
    'right':(lambda n: (lambda x:(lambda y: [(lambda b: len(position_test(block_filter(y, allblocks), block_filter(x,allblocks),
                                                                          "r")) in n and b in position_test(
        block_filter(
            y, allblocks), block_filter(x, allblocks), "r"))]))),
    'to':(lambda x: x),
    'the':(lambda x: x)
    
}


# Main is used for testing the grammar with the test sentences from semdata.py
# Run the main for a simple demo of our grammar with respect to a

if __name__ == '__main__':

    from semdata import test_utterances
    from world import *

    # creates the grammar 
    gram = Grammar(gold_lexicon, rules, functions)

    # use picture from world.png and world.py for testing purpose
    allblocks2 = []
    all_blocks_grid = allblocks_test.copy()
    for row in allblocks_test:
        for blo in row:
            if blo:
                allblocks2.append(blo)
    allblocks=allblocks2

    # parses all test sentences from semdata.py
    # prints the derived logical forms for each test sentence and whether the test sentence is true with respect to the example picture world.png
    for i,u in enumerate(test_utterances):

        # creates the global variable for keeping track of which block is / blocks are the described one(s)
        guessed_blocks = set()
        
        lfs = gram.gen(u)
        print("======================================================================")
        print('Utterance: {}'.format(u))
        for lf in lfs:
            print("\tLF: {}".format(lf))
            print('\tDenotation: {}'.format(gram.sem(lf)))

            # if utterance doesn't describe sentence not blocks should be guessed at all
            if gram.sem(lf) == False:
                guessed_blocks = set()

            # visualization of how the computer gives feedback about what it "understood"
            # for the example for the sentence 'there is a red triangle under a blue square' the picture object corresponding to world.png is created
            # and a png file is created and saved where the blocks that are in all_blocks_grid are marked, e.g. all blocks that are red and have shape
            # triangle and are positioned below a blue square in the grid are marked as well as the blue squares that are above the red triangle
            
            from BlockPictureGenerator import * 
            test_pic = Picture(name = "./marked_pictures/" + u)
            test_pic.blocks = allblocks.copy()
            test_pic.block_n = len(test_pic.blocks)
            test_pic.grid = all_blocks_grid

            test_pic.draw()
            guess = []
            for b in guessed_blocks:
                guess.append((b.y, b.x))
            test_pic.mark(guess)


                

    



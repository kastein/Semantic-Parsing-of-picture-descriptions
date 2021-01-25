#!/usr/bin/env python

"""
The intellectual core of the paper. For demos:

python synthesis.py

Our goal with this code is to illustrate how the learning framework
from `learning.py` and the grammar framework from `grammar.py` come
together.  

`phi_sem` is the simple feature function used in figure 2 of the paper.
We use it here for all of the illustrations.

`crude_lexicon` is a grammar that respects typing but nothing else.
Together with rules and functions from `grammar.py`, it defines a crude
grammar. The goal of learning is to refine this grammar by finding the
best pairings of lexical items and logical expressions.

For all of the illustrations, the train/test data are created in
`semdata` using a gold grammar, which has the same rules as the crude
grammar and the same functions for interpretation, but its lexicon is
perfect.

`evaluate_semparse` runs the semantic parsing model of section 4.1 of
the paper. Its training data predictions are perfect. It makes a
predictable mistake on the test data: since it never sees 'four'/4
in training, it gets the final test example wrong.

`evaluate_interpretive` implements section 4.2 of the paper, using
`LatentSGD` instead of `SGD` (both in `learning.py`). The role of the
grammar is the same as in `evaluate_semparse`, and the resulting
performance is the same as well.

`evaluate_latent_semparse` goes beyond what is in the paper, to
achieve more of a connection with published semantic parsing models.
Here, we see only the root node of the logical form in training, so
that the tree structure is a latent variable. To make it interesting,
we add a type-lifting rule to the grammar, so that many final logical
forms correspond to multiple distinct derivations. LatentSGD is used
for optimization, and the resulting performance is the same as for
the other models.

"""


__author__ = "Christopher Potts and Percy Liang"
__credits__ = []
__license__ = "GNU general public license, version 2"
__version__ = "2.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the authors' websites"


import re
from collections import defaultdict
from grammar_TEST import Grammar, rules, functions
from learning import evaluate, SGD, LatentSGD
import semdata


def phi_sem(x, y):
    """Feature function defined over full trees. It tracks the topmost
    binary relation if there is one, and it tracks all the lexical 
    features."""
    d = defaultdict(float)
    # Topmost relation symbol:
    toprel_re = re.compile(r"^(and|exist)")
    match = toprel_re.search(y[0][1])
    if match:
        d[('top', 'R', match.group(1))] = 1.0
    # Lexical features:
    for leaf in leaves(y):
        d[leaf] += 1.0
    return d

def leaves(x):
    """Recursive function for finding all the preterminals (mother--child)
    trees. Used by phi_sem"""
    # Leaf-only trees:
    if len(x[1])==1 and isinstance(x[1][0],str):
        return [(x[0],x[1][0])]
    # Recursive call for all child subtrees:
    l = []
    for child in x[1]:
        l += leaves(child)
    return l

# This crude lexicon is the starting point for learning; it respects
# typing but nothing else:
crude_lexicon = {}
"""
# numbers
for word in ['a', 'one','two', 'three']:
    crude_lexicon[word] = [('N','range(1,int(sys.float_info.max))'),('N','[1]'),('N','[2]'),('N','[3]')]
# colours
for word in ['blue','green','yellow','red']:
    crude_lexicon[word] = [('C','green'),('C','yellow'),('C','red'),('C','blue')]
# shapes
for word in ['form','forms','square','squares','triangle','triangles','circle','circles']:
    crude_lexicon[word] = [('B','[]'),('B','[(lambda b: b.shape == "rectangle")]'),('B','[(lambda b: b.shape == "triangle")]'),('B','[(lambda b: b.shape == "circle")]')]
# locations
for word in ['over','under']:
    crude_lexicon[word] = [('U','under'),('U','over')]
# rest of the words
for word in ['there','is','are','and']:
    crude_lexicon[word] = [('I','identy'),('AND','und'),('E','exist')]
"""
# no matter which language, but then we will get a memory error
for word in ('form','square','squares','triangle','triangles','circle','circles','green','yellow','blue','red','there','is','are','under','over','and','one','a','two','three'):
    crude_lexicon[word] = [('B','[]'),('B','[(lambda b: b.shape == "rectangle")]'),('B','[(lambda b: b.shape == "triangle")]'),('B','[(lambda b: b.shape == "circle")]'),('C','green'),('C','yellow'),('C','blue'),('C','red'),('E','exist'),('I','identy'),('N','range(1,17)'),('N','[1]'),('U','under'),('U','over'),('AND','und')]


# Our crude grammar, the starting point for learning. rules and
# functions are as defined in grammar.py
gram = Grammar(crude_lexicon, rules, functions)

def evaluate_semparse():
    """Evaluate the semantic parsing set-up, where we learn from and 
    predict logical forms. The set-up is identical to the simple 
    example in evenodd.py, except that classes is gram.gen, which 
    creates the set of licit parses according to the crude grammar."""    
    print("======================================================================")
    print("SEMANTIC PARSING")
    # Only (input, lf) pairs for this task:
    semparse_train = [[x,y] for x, y, d in semdata.sem_train]
    semparse_test = [[x,y] for x, y, d in semdata.sem_test]        
    evaluate(phi=phi_sem,
             optimizer=SGD,
             train=semparse_train,
             test=semparse_test,
             classes=gram.gen,
             T=10,
             eta=0.1)
    
def evaluate_interpretive():
    """Evaluate the interpretive set-up, where we learn from and 
    predict denotations. The only changes from evaluate_semparse are 
    that we use LatentSGD, and output_transform handles the mapping 
    from the logical forms we create to denotations."""
    print("======================================================================")
    print('INTERPRETIVE')
    # Only (input, denotation) pairs for this task:
    interpretive_train = [[x,d] for x, y, d in semdata.sem_train]
    interpretive_test =  [[x,d] for x, y, d in semdata.sem_test]
    evaluate(phi=phi_sem,
             optimizer=LatentSGD,
             train=interpretive_train,
             test=interpretive_test,
             classes=gram.gen,
             T=10,
             eta=0.1,
             output_transform=gram.sem)

def evaluate_latent_semparse():
    print("======================================================================")
    print('LATENT SEMANTIC PARSING')
    # Only (input, LF root node) pairs for this task; y[0][1] indexes
    # into the semantics of the root node:
    latent_semparse_train = [[x,y[0][1]] for x, y, d in semdata.sem_train]
    latent_semparse_test =  [[x,y[0][1]] for x, y, d in semdata.sem_test]  
    
    #for word in ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'):
        #crude_lexicon[word] += [('Q', 'lift(%s)' % i) for i in range(1,10)]

    for word in ('form','square','squares','triangle','triangles','circle','circles','green','yellow','blue','red','there','is','are','under','over','and','one','a','two','three'):
        crude_lexicon[word] = [('B','[]'),('B','[(lambda b: b.shape == "rectangle")]'),('B','[(lambda b: b.shape == "triangle")]'),('B','[(lambda b: b.shape == "circle")]'),('C','green'),('C','yellow'),('C','blue'),('C','red'),('E','exist'),('I','identy'),('N','range(1,17)'),('N','[1]'),('U','under'),('U','over'),('AND','und')]


    # New grammar:
    gram = Grammar(crude_lexicon, rules, functions)    
    # Now train with LatentSGD, where the output transformation is 
    # one that grabs the root node:
    evaluate(phi=phi_sem,
             optimizer=LatentSGD,
             train=latent_semparse_train,
             test=latent_semparse_test,
             classes=gram.gen,
             T=10,
             eta=0.1,
             output_transform=(lambda y : y[0][1]))


if __name__ == '__main__':

    evaluate_semparse()
    evaluate_interpretive()
    #evaluate_latent_semparse()


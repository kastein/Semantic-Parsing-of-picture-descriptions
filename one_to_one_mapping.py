import Semantic_Learner, nltk, grammar
from grammar import *
from PictureLevel import setPicParameters
import os
import Semantic_Learner

# a tryout for learning new lexical items if they have a one to one correspondance with words from the goldlexicon
# the script might have to be run a couple of times, until the picture actually includes a red circle (see first picture in "pictures")
current_pic = setPicParameters(level=1, i_picture=1, session_name="pictures")
current_pic.draw()
create_all_blocks(current_pic)

# input that is completely new to the parser
inpt = "da ist ein roter kreis"

# empty lexicon
crude = dict()
# inserting every possible category - input word mapping
# this might lead to a memory error when non-fitting rules are not excluded and new lexical items keep appearing
for word in inpt.split():
    crude[word] = list()
    for rightside in gold_lexicon.values():
        for item in rightside:
            if item not in crude[word]:
                crude[word].append(item)

learned_rules = list()
# generating all trees, only a fraction of which will make sense later
# this might even more so cause a memory error because a LOT of trees are produced here
gram = Grammar(crude, rules, functions)
lfs = gram.gen(inpt)

print('Utterance: {}'.format(inpt))
for lf in lfs:
    # proceed only if the tree applies to the picture
    if gram.sem(lf) is True:
        print(lf)
        # let's see, which blocks get marked
        for block in guessed_blocks:
            print(block)
            # the following corresponds to the user's feedback, only if the right field is marked, the rule is learned as correct
            if str(block) == "circle: red": # user clicks "yes" as soon as this is the case
                print("rule learned: ", inpt, " -> ", lf)
                learned_rules.append((inpt, lf))

    guessed_blocks.clear()

# let's see the rules we have learned and how many they are
print(learned_rules)
print(len(learned_rules))

# mapping the input sentence words to the leave nodes to create actual lexicon entries from the trees
learned_lexicon = set()
for rule in learned_rules:
    for lex in Semantic_Learner.leaves(rule):
        learned_lexicon.add(lex)

# at this point, some of the german words have multiple corresponding categories
# we would now have to work with rule probabilities (weights) in order to odd the wrong ones out
print(learned_lexicon)
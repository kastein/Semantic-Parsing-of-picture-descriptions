"""
This file defines the methods used in the functions of the grammar in grammar.py
They are used to find the blocks in the Picture object described in the input utterance
Difference between referenced and guessed blocks:
for sentences like "there is a red circle" both contain the same Block objects, i.e. the objects of all red circles in the Picture
but for e.g. the sentence "there is a green triangle over a red square over a circle" referenced blocks consists of
all green triangles that are over red squares that are over any circle
whereas guessed blocks consists of all green triangles, red squares and circles that make this sentence true
"""


def position_test(blocks, block_locations, number, position):
    """
    finds all pairs of blocks b1 and b2 from the referenced blocks from blocks and block_locations respectively
    that stand in relation position to eachother and checks if number of blocks is true
    e.g. blocks[0] is a list of all blue rectangles and block_locations[0] a list of all red circles, number is 2, position is 'u'
    then the function returns the list of all blocks that are blue rectangles and are below 2 red circles and the list
    of all blue rectangles and red circles matching the condition;
    :param blocks: tuple(list,list) first list of blocks are the referenced blocks, second list are the guessed blocks
    :param block_locations: tuple(list,list) first list of blocks are the referenced blocks, second list are the guessed blocks
    :param number: the number of blocks from block_locations that should fulfill the relation
    :param position: string for the relative position
    :return: list of all blocks from blocks that stand in relation position to any block in block_locations
    """
    ref_blocks1 = blocks[0]
    ref_blocks2 = block_locations[0]
    gue_blocks1 = blocks[1]
    gue_blocks2 = block_locations[1]

    fulfill_ref = set()
    fulfill_guess = set()
    fulfill_guess.update(gue_blocks1)
    fulfill_guess.update(gue_blocks2)

    matching_combs = []

    for b1 in ref_blocks1:
        matching_b2 = set()

        for b2 in ref_blocks2:

            match = False
            if position == "u" and b1.y > b2.y:
                match = True

            elif position == "o" and b1.y < b2.y:
                match = True

            elif position == "n":
                if b1.y == b2.y and (b1.x == b2.x + 1 or b1.x == b2.x - 1):
                    match = True

            elif position == "l" and b1.x < b2.x:
                match = True

            elif position == "r" and b1.x > b2.x:
                match = True

            if match == True:
                matching_b2.add(b2)

        if matching_b2 != []:
            matching_combs.append((b1,matching_b2))

    passed_check = set()
    for b1,b2s in matching_combs:
        if len(b2s) in number:
            fulfill_ref.add(b1)
            passed_check.add(b1)
            passed_check.update(b2s)

    all_ref = set(ref_blocks1+ref_blocks2)
    for bl in all_ref:
        if bl not in passed_check:
            fulfill_guess.remove(bl)

    fulfill_ref = list(fulfill_ref)
    if fulfill_ref == []:
        fulfill_guess = []
    else:
        fulfill_guess = list(fulfill_guess)

    return fulfill_ref, fulfill_guess


def block_filter(conditions, blocks):
    """
    checks which blocks match a certain condition such as shape == rectangle or color == green
    :param conditions: list of conditions
    :param blocks: tuple(list,list)  first list of blocks are the referenced blocks, second list are the guessed blocks
    :return: tuple(list,list) with the list of referenced blocks fulfilling the conditions and the list of guessed blocks
    fulfilling the conditions
    """
    fulfill_ref = []

    ref_blocks = blocks[0]
    gue_blocks = blocks[1]
    fulfill_guess = gue_blocks.copy()

    for b in ref_blocks:
        test = True
        for c in conditions:
            if not c(b):
                test = False
        if test:
            fulfill_ref.append(b)
        else:
            fulfill_guess.remove(b)

    return fulfill_ref, fulfill_guess

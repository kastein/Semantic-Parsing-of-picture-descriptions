def position_test(blocks, block_locations, number, position):
    """
    finds all pairs of blocks b1 form blocks and b2 from block_locations that stand in relation position to eachother
    e.g. blocks is a list of all blue rectangles and block_locations a list of all red circles and position is 'u'
    then the function returns all blocks that are blue rectangles and are below red circles
    additionally updates guessed blocks by removing all blocks from guessed_blocks that do not match, e.g. removes all
    blue rectangles that are not below a red circle and removes all red circles that are not above a blue rectangle
    :param blocks: list of blocks
    :param block_locations: list of blocks
    :param number:
    :param position: string for the relative position
    :return: list of all blocks from blocks that stand in relation position to any block in block_locations
    """
    fulfill_ref = set()
    fulfill_guess = set()
    checked = set()
    passed_check = set()

    ref_blocks1 = blocks[0]
    ref_blocks2 = block_locations[0]
    gue_blocks1 = blocks[1]
    gue_blocks2 = block_locations[1]

    fulfill_guess.update(gue_blocks1)
    fulfill_guess.update(gue_blocks2)

    for b1 in ref_blocks1:
        for b2 in ref_blocks2:
            checked.add(b1)
            checked.add(b2)

            if position == "u":
                if b1.y > b2.y:
                    fulfill_ref.add(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

            elif position == "o":
                if b1.y < b2.y:
                    fulfill_ref.add(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

            elif position == "n":
                if b1.y == b2.y and (b1.x == b2.x + 1 or b1.x == b2.x - 1):
                    fulfill_ref.add(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

            elif position == "l":
                if b1.x < b2.x:
                    fulfill_ref.add(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

            elif position == "r":
                if b1.x > b2.x:
                    fulfill_ref.add(b1)
                    passed_check.add(b1)
                    passed_check.add(b2)

    for bl in checked:
        if bl not in passed_check:
            try:
                fulfill_guess.remove(bl)
            except:
                print(bl)
                print("guessed:")
                for t in fulfill_guess:
                    print(t)
                fulfill_guess.remove(bl)

    check_number = 0
    for bl in gue_blocks2:
        if bl in fulfill_guess:
            check_number += 1

    fulfill_ref = list(fulfill_ref)

    if check_number not in number:
        fulfill_ref = []
        fulfill_guess = set()

    return fulfill_ref, fulfill_guess


def block_filter(conditions, blocks):
    """
    returns a list of all blocks that match the specific conditions and updates guessed_blocks by adding those blocks
    :param conditions: list of conditions, e.g. shape == rectangle or color == green
    :param blocks:
    :return: a list of all blocks in blocks that fulfill the conditions
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

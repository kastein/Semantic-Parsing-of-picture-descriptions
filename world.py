class Block:
    """
    Object Block has attributes colour and x and y coordinate
    """
    def __init__(self, colour, shape):
        """
        Block object only initialized with colour, coordinates are set separately
        :param colour: a colour as specified in the list colours
        """
        self.colour = colour
        self.shape = shape
        self.x = None
        self.y = None

    def set_coordinates(self, x, y):
        """
        sets the coordinates of the block w.r.t. the position in the grid
        :param x:
        :param y:
        :return:
        """
        self.x = x
        self.y = y


def set_all_coordinates(chart):
    for row in range(1,len(chart)+1):
        for column in range(1,len(chart[row-1])+1):
            if chart[row-1][column-1] != None:
                chart[row-1][column-1].set_coordinates(column,row)
                
    


one = Block("blue","rectangle")
two = Block("blue","rectangle")
three = Block("blue","triangle")
four = Block("yellow","rectangle")
five = Block("red","triangle")

world = [[None,one,two,None],[three,None,None,four],[None,five,None,None],[None,None,None,None]]

one = Block("red","triangle")
two = Block("blue","circle")
three = Block("red","circle")
four = Block("yellow","circle")
five = Block("yellow","triangle")
six = Block("blue","circle")
seven = Block("yellow","circle")
eight = Block("blue","circle")
nine = Block("red","circle")
ten = Block("green","circle")
eleven = Block("green","triangle")
twelve = Block("red","triangle")
thirteen = Block("green","rectangle")
fourteen = Block("green","circle")
fivteen = Block("yellow","circle")
sixteen = Block("blue","triangle")

world2 = [[one,two,three,four],[five,six,seven,eight],[nine,ten,eleven,twelve],[thirteen,fourteen,fivteen,sixteen]]


# choose which example picture you would like to use
# allblocks = world
allblocks = world2
set_all_coordinates(allblocks_test)




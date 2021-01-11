class Block:
    """
    Object Block has attributes colour and x and y coordinate
    """
    def __init__(self, colour):
        """
        Block object only initialized with colour, coordinates are set separately
        :param colour: a colour as specified in the list colours
        """
        self.colour = colour
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

blau = Block("blue")
gelb = Block("yellow")
blau.set_coordinates(1,3)
gelb.set_coordinates(1,2)
allblocks = [[blau,None,None,None],[None,None,None,None],[None,gelb,None,None],[None,None,None,None]]

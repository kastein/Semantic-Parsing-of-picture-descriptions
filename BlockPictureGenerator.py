import random
from tkinter import *
from PIL import Image, ImageDraw, ImageColor
import os
#from CalculCoordinates import *


# Define the Colours
red = "rgb(205,000,000)"
blue = "rgb(051,153,255)"
green = "rgb(102,205,000)"
yellow = "rgb(220,220,000)"
colours = ["yellow","red","blue","green"]
colour_dict = {"red":red,"blue":blue,"green":green,"yellow":yellow}

# Define the possible shapes
shapes = ["circle", "rectangle", "triangle"]


# Variables for the picture
size_pic = 300          # length of one side of the picture
size_grid = 200         # length of one side of the grid
dim = 4                 # number of blocks possible per row and per column
rel_blocks = 0.6        # how much of the length of one side of grid should be made up by lengths of the blocks


# Calculate coordinates automatically
#coordinates = calculate_coordinates(size_pic, size_grid, dim, rel_blocks)

# Use fixed coordinates
coordinates = {1:{1:([(55,55),(95,95)]),2:([(105,55),(145,95)]),3:([(155,55),(195,95)]),4:([(205,55),(245,95)])},
               2:{1:([(55,105),(95,145)]),2:([(105,105),(145,145)]),3:([(155,105),(195,145)]),4:([(205,105),(245,145)])},
               3:{1:([(55,155),(95,195)]),2:([(105,155),(145,195)]),3:([(155,155),(195,195)]),4:([(205,155),(245,195)])},
               4:{1:([(55,205),(95,245)]),2:([(105,205),(145,245)]),3:([(155,205),(195,245)]),4:([(205,205),(245,245)])}}


class Block:
    """
    Object Block has attributes colour and x and y coordinate and shape (can be circle, triangle or rectangle)
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

    def __str__(self):
        s = self.shape + ": " + self.colour
        return s


class Picture:
    """
    Class for Pictures displaying blocks in different colours in a 4x4 grid
    """
    def __init__(self, complexity=(3,17), name="test"):
        """
        :param complexity: a tuple (min_n, max_n + 1) where min_n is the minimal number of blocks and max_n the maximal number of blocks that should be included in the picture
                            default value: between 3 and and 16 blocks
        :param name: name for the saved file of the picture
        default value complexity: at least one block and at most 16 blocks
        default name: test.png
        """
        self.block_n = random.choice(range(complexity[0], complexity[1]))
        self.blocks = self.create_blocks(self.block_n)
        self.grid = self.create_grid()
        self.name = name

    def create_blocks(self, block_number):
        """
        :param block_number: number of blocks to be created, colours are chosen randomly
        :return: returns a list of length block_number with Block objects, coordinates not yet set
        """
        blocks_list = []
        while len(blocks_list) < block_number:
            new_colour = random.choice(colours)
            new_shape = random.choice(shapes)
            new_block = Block(new_colour, new_shape)
            blocks_list.append(new_block)
        return blocks_list

    def create_grid(self):
        """
        creates the grid by placing the created blocks at randomly chosen positions in the 4x4 grid
        sets the coordinates of each of the blocks in self.blocks
        :return: a list of lists: each inner list corresponds to one row
        """
        row1 = 4 * [None]
        row2 = 4 * [None]
        row3 = 4 * [None]
        row4 = 4 * [None]
        grid = [row1, row2, row3, row4]

        free_pos = [(i,j) for i in range(1,5) for j in range(1,5)]
        # randomly shuffle all possible positions s.t. popping an element from the list will result in getting a randomly chosen element
        random.shuffle(free_pos)

        for b in self.blocks:
            # pop chosen position in order to make sure that no two blocks will be placed at the same position
            random_pos = free_pos.pop()
            row_index = random_pos[0]
            col_index = random_pos[1]
            b.set_coordinates(col_index, row_index)
            grid[row_index-1][col_index-1] = b
        return grid


    def draw(self):
        """
        draws the picture and saves it under self.name + .png ending
        :return: nothing
        """
        pass
        image1 = Image.new("RGB", (size_pic, size_pic), "white")
        draw = ImageDraw.Draw(image1)
        edge = (size_pic-size_grid)/2
        draw.rectangle([(edge,edge),(size_pic-edge,size_pic-edge)],fill="white",outline="black")
    
        for row in coordinates:
            for column in coordinates[row]:
                if self.grid[row-1][column-1]:
                    current_block = self.grid[row-1][column-1]
                    if current_block.shape == "circle":
                        draw.ellipse(coordinates[row][column],fill=colour_dict[current_block.colour],outline="black")
                    elif current_block.shape == "triangle":
                        coords = coordinates[row][column]
                        side_length = (coords[1][0] - coords[0][0])
                        point1 = (coords[0][0] + side_length/2, coords[0][1])
                        point2 = (coords[0][0], coords[0][1] + side_length)
                        point3 = coords[1]
                        draw.polygon([point1,point2,point3],fill=colour_dict[current_block.colour],outline="black")
                    else:
                        draw.rectangle(coordinates[row][column],fill=colour_dict[current_block.colour],outline="black")

        image1.save(self.name+".png")
        #os.startfile(self.name+".png")


    def readable_grid(self):
        """
        returns a list representation of the grid consisting of n sublists,
        each corresponding to a row in the grid and an entry for each cell of
        the grid: the shape and the colour of the block in this cell or None if
        there is no block in this cell
        """
        new_grid = list()
        for row in self.grid:
            new_row = list()
            for item in row:
                if item != None:
                    new_row.append(str(item))
                else:
                    new_row.append(None)
            new_grid.append(new_row)
        return new_grid


    def mark(self, spacetobemarked):
        """
        draws a rectangle around the blocks that should be marked in the picture
        and saves the resulting new picture
        spacetobemarked = position of the block(s) that need to be marked
        """
        with Image.open(self.name+".png") as pic:
            draw = ImageDraw.Draw(pic)
            for field in spacetobemarked:
                current_coor = coordinates[field[0]][field[1]]
                top_left = current_coor[0]
                bottom_right = current_coor[1]
                draw.rectangle([(top_left[0], top_left[1]), (bottom_right[0], bottom_right[1])], outline="black")
                draw.rectangle([(top_left[0]-1, top_left[1]-1), (bottom_right[0]+1, bottom_right[1]+1)], outline="black")
                draw.rectangle([(top_left[0] - 2, top_left[1] - 2), (bottom_right[0] + 2, bottom_right[1] + 2)], outline="black")
                draw.rectangle([(top_left[0] - 3, top_left[1] - 3), (bottom_right[0] + 3, bottom_right[1] + 3)], outline="black")
            pic.save(self.name + "_guess.png")

# CODE FOR TESTING

if __name__=="__main__":
    # Create a Picture with random number of blocks and name test.png
    p1 = Picture()
    #print(p1.grid)
    p1.draw()
    print(p1.readable_grid())
    guess = [(1,1),(1,2)]
    p1.mark(guess) # creates a file "guess.jpg" that has black boxes around the blocks specified in guess
    # Create a Picture with 1, 2 or 3 blocks and name low_complexity.png
    #p2 = Picture((1,3), "low_complexity")
    #p2.draw()
    #p1.mark(guess)

    # Create a Picture with blocks in every cell
    # Used to try out different sizes and the automatic calculation of the coordinates
    p_coord_test = Picture((16,17), "full_pic_300_200_07")
    p_coord_test.draw()
    p_coord_test.mark(guess)


    # Check that coordinates are correct
    '''all_b = p_coord_test.blocks
    for b in all_b:
        print("colour: " + b.colour + "  x: " + str(b.x) + "  y: " + str(b.y))'''


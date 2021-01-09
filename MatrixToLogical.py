# file matrix into logical
from PictureGenerator import *

current_picture = p1.grid
print(current_picture)
colours = colours[:4]

class CalculateLogicals:
    def __init__(self, grid):
        self.grid = grid

    def exists(self, color):
        for row in self.grid:
            for block in row:
                if color==block:
                    return "exists(" + color + ")"
        return False

    def directly_left_of(self, color1, color2):
        for row in self.grid:
            for blockpos in range(0,len(row)):
                if row[blockpos] == color1 and blockpos < 3:
                    if row[blockpos+1] == color2:
                        return "directly-left-of(" + color1 + "," + color2 + ")"
        return False

    def left_of(self, color1, color2):
        for row in self.grid:
            for blockpos in range(0,len(row)):
                if row[blockpos] == color1 and blockpos < 3:
                    for otherblockpos in range(blockpos+1, len(row)):
                        if row[otherblockpos] == color2:
                            return "left-of(" + color1 + "," + color2 + ")"
        return False

    def logicals(self):
        logicals = list()

        #exists
        for color in colours:
            if self.exists(color):
                logicals.append(self.exists(color))

        #directly-left-of
        for color1 in colours:
            for color2 in colours:
                if self.directly_left_of(color1, color2):
                    logicals.append(self.directly_left_of(color1, color2))

        #left-of
        for color1 in colours:
            for color2 in colours:
                if self.left_of(color1, color2):
                    logicals.append(self.left_of(color1, color2))

        return logicals


l = CalculateLogicals(current_picture)
print(l.logicals())
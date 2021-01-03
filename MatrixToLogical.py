# file matrix into logical
from PictureGenerator import *

current_picture = p1.grid
print(current_picture)
colours = colours[:4]

class CalculateLogicals:
    def __init__(self, grid):
        self.grid = grid
        #self.pos11 = self.grid[0][0]
        #self.pos12 = self.grid[0][1]

    def exists(self, color):
        for row in self.grid:
            for block in row:
                if color==block:
                    return "exists(" + color + ")"
        return "not exists(" + color + ")"

    def directly_left_of(self, color1, color2):
        for row in self.grid:
            for blockpos in range(0,len(row)):
                if row[blockpos] == color1 and blockpos < 3:
                    if row[blockpos+1] == color2:
                        return "directly-left-of(" + color1 + "," + color2 + ")"
        return "not directly-left-of(" + color1 + "," + color2 + ")"

    def left_of(self, color1, color2):
        for row in self.grid:
            if color1 in row and color2 in row:
                if row.index(color1) < row.index(color2):
                    return "left-of(" + color1 + "," + color2 + ")"
        return "not left-of(" + color1 + "," + color2 + ")"

    def logicals(self):
        logicals = list()

        #exists
        for color in colours:
            logicals.append(self.exists(color))

        #directly-left-of
        for color1 in colours:
            for color2 in colours:
                logicals.append(self.directly_left_of(color1, color2))

        #left-of
        for color1 in colours:
            for color2 in colours:
                logicals.append(self.left_of(color1, color2))

        return logicals


l = CalculateLogicals(current_picture)
print(l.logicals())
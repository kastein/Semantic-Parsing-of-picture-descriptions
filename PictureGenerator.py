import random
from tkinter import *
from PIL import Image, ImageDraw, ImageColor



red = "rgb(205,000,000)"
blue = "rgb(000,000,139)"
green = "rgb(102,205,000)"
yellow = "rgb(220,220,000)"
colours = ["yellow","red","blue","green",None]
colour_dict = {"red":red,"blue":blue,"green":green,"yellow":yellow}
coordinates = {1:{1:([(55,55),(95,95)]),2:([(105,55),(145,95)]),3:([(155,55),(195,95)]),4:([(205,55),(245,95)])},2:{1:([(55,105),(95,145)]),2:([(105,105),(145,145)]),3:([(155,105),(195,145)]),4:([(205,105),(245,145)])},3:{1:([(55,155),(95,195)]),2:([(105,155),(145,195)]),3:([(155,155),(195,195)]),4:([(205,155),(245,195)])},4:{1:([(55,205),(95,245)]),2:([(105,205),(145,245)]),3:([(155,205),(195,245)]),4:([(205,205),(245,245)])}}


class Picture:
    def __init__(self):
        row1 = random.choices(colours,weights=[2,2,2,2,25],k=4)
        row2 = random.choices(colours,weights=[2,2,2,2,25],k=4)
        row3 = random.choices(colours,weights=[2,2,2,2,25],k=4)
        row4 = random.choices(colours,weights=[2,2,2,2,25],k=4)
        self.grid=[row1,row2,row3,row4]
        #self.canvas = Canvas(Tk(),width=1000, height=1000)
        

    def draw(self):
        pass
        #self.canvas.pack()
        #self.canvas.create_rectangle(10,10,370,370,fill="white")
        image1 = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(image1)
        draw.rectangle([(50,50),(250,250)],fill="white",outline="black")
    
        for row in coordinates:
            for column in coordinates[row]:
                if self.grid[row-1][column-1]:
                    draw.rectangle(coordinates[row][column],fill=colour_dict[self.grid[row-1][column-1]],outline="black") 
        
        image1.save("test.jpg")
        import os
        os.startfile("test.jpg")
        #self.canvas.create_line(100,10,100,370)
        #self.canvas.create_line(190,10,190,370)
        #self.canvas.create_line(280,10,280,370)

        #self.canvas.create_line(10,100,370,100)
        #self.canvas.create_line(10,190,370,190)
        #self.canvas.create_line(10,280,370,280)
    

p1 = Picture()
print(p1.grid)
p1.draw()


"""master = Tk()

w = Canvas(master, width=1000, height=1000)
w.pack()

w.create_rectangle(50, 20, 100, 70, fill="green2")
w.create_rectangle(50, 100, 100, 150, fill="red3")
w.create_rectangle(50, 180, 100, 230, fill="navy")"""

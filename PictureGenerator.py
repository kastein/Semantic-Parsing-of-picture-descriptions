import random
from tkinter import *
from PIL import Image, ImageDraw, ImageColor

colours = ["red3","navy","green2",None]
coordinates = {1:{1:(),2:(),3:(),4:()},2:{1:(),2:(),3:(),4:()},3:{1:(),2:(),3:(),4:()},4:{1:(),2:(),3:(),4:()}}


class Picture:
    def __init__(self):
        row1 = random.choices(colours,weights=[1,1,1,8],k=4)
        row2 = random.choices(colours,weights=[1,1,1,8],k=4)
        row3 = random.choices(colours,weights=[1,1,1,8],k=4)
        row4 = random.choices(colours,weights=[1,1,1,8],k=4)
        self.red ="rgb(205,000,000)"
        self.blue="rgb(000,000,139)"
        self.green="rgb(102,205,000)"
        self.grid=[row1,row2,row3,row4]
        #self.canvas = Canvas(Tk(),width=1000, height=1000)
        

    def draw_block(coordinates,colour):
        pass

    def draw(self):
        #self.canvas.pack()
        #self.canvas.create_rectangle(10,10,370,370,fill="white")
        
        image1 = Image.new("RGB", (600, 600), "white")
        draw = ImageDraw.Draw(image1)
        draw.rectangle([(100,100),(500,500)],fill="white",outline="black")
        draw.rectangle([(50,50),(80,80)],fill=self.red,outline="black")
        draw.rectangle([(90,90),(120,120)],fill=self.blue,outline="black")
        draw.rectangle([(130,130),(160,160)],fill=self.green,outline="black")
        
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

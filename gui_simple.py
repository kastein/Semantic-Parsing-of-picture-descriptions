import PySimpleGUI as sg
from BlockPictureGenerator import Picture
import os.path
from PIL import Image, ImageTk

start = [
    [
        sg.Text("Hello! -Description-"),
        sg.Button("Start Game", key="-START-")
    ]
]

first_item = [
    [
        sg.Image(key="-IMAGE-")  # try to read in jpg.files
    ],
    [
        #sg.Text("What is in the picture?", key="-INSTRUCTION-"),
        sg.Button("show next picture", key="-NEXT-")
    ],
    [
        sg.Text("Describe the picture:", key="-INSTRUCTION-"), # store what is being typed, when person hits enter
        sg.In(size=(25, 1), enable_events=True, key="-INPUT-"),
        sg.Button("Enter", key="-ENTER-")
    ]
]


layout = [
    [
        sg.Column(first_item)
    ]
]

starting_screen = sg.Window("Hello!", start)
actualgame = sg.Window("My Program", layout)
#window = starting_screen
window = actualgame

inpt = None
while True:
    event, values = window.read()
    print(event, values)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Beginning screen
    #if event == "-START-":
        #window.close()
        #window = actualgame
        #window.read()
    # Displaying picture and taking input
    if event == "-NEXT-":
        picture = Picture(name="guitest").draw()
        window["-IMAGE-"].update(filename="guitest.png")
    if event == "-INPUT-":
        inpt = values["-INPUT-"]
    if event == "-ENTER-":
        print(inpt)
        window["-INSTRUCTION-"].update("Did you refer to this?")
        picture = Picture(name="guitest").mark([(1,1)])
        window["-IMAGE-"].update(filename="guitest_guess.png")
        window["-INPUT-"].update("")
        #window["-WELCOME-"].update("Thank you")
        # try to say thank you to for the input
        # feedback by the grammar


window.close()
import PySimpleGUI as sg
from BlockPictureGenerator import Picture
from grammar import Grammar, gold_lexicon, rules, functions
import os.path
from PIL import Image, ImageTk

gram = Grammar(gold_lexicon, rules, functions)

'''start = [
    [
        sg.Text("Hello! -Description-"),
        sg.Button("Start Game", key="-START-")
    ]
]'''

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
    ],
    [
        sg.Button("YES", key="-YES-"),
        sg.Button("NO", key="-NO-")
    ]
]


layout = [
    [
        sg.Column(first_item)
    ]
]

#starting_screen = sg.Window("Hello!", start)
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
        #window["My Program"].update(actualgame)
        #window = actualgame
        #window.read()
    # Displaying picture and taking input
    if event == "-NEXT-":
        picture = Picture(name="guitest").draw()
        window["-IMAGE-"].update(filename="guitest.png")
        window["-INSTRUCTION-"].update("Describe the picture:")
    if event == "-INPUT-":
        inpt = values["-INPUT-"]
    if event == "-ENTER-":
        print(inpt)
        # here go into semantic parser
        lfs = gram.gen(inpt)
        print(lfs)
        window["-INSTRUCTION-"].update("Did you refer to this?")
        picture = Picture(name="guitest").mark([(1,1)])
        window["-IMAGE-"].update(filename="guitest_guess.png")
        window["-INPUT-"].update("")
    if event == "-YES-":
        window["-INSTRUCTION-"].update("Awesome!")
    if event == "-NO-":
        # ask for next guess from parser
        picture = Picture(name="guitest").mark([(1,2)])
        window["-IMAGE-"].update(filename="guitest_guess.png")

window.close()
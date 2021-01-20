import PySimpleGUI as sg
from BlockPictureGenerator import Picture
from grammar import *
import os.path
from PIL import Image, ImageTk
from PictureLevel import *

gram = Grammar(gold_lexicon, rules, functions)

starting_screen = [
    [
        sg.Text("Hello! -Description- Press 'Start Game' to start the game"),
        sg.Button("Start Game", key="-START-")
    ]
]

game_screen = [
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

layout_starting_screen = [
    [
        sg.Column(starting_screen)
    ]
]

layout_game_screen = [
    [
        sg.Column(game_screen)
    ]
]

start = sg.Window("Hello!", layout_starting_screen)
actualgame = sg.Window("My Program", layout_game_screen)
window = start
#window = actualgame

inpt = None

while True:
    event, values = window.read()
    print(event, values)

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Beginning screen
    if event == "-START-":
        window.close()
        window = actualgame
        #event, values = window.read()
        #picture = Picture(name="guitest").draw()
        #window["-IMAGE-"].update(filename="guitest.png")
        #continue

    # Displaying picture and taking input
    if event == "-NEXT-":
        picture = setPicParameters(1, 1, "pictures")
        picture.draw()
        #picture = Picture(name="guitest").draw()
        # change later
        file_name = "pictures" + "_L" + str(1) + "_" + str(1) + ".png"
        path_pict = "./" + "pictures" + "/" + file_name
        window["-IMAGE-"].update(filename=path_pict)
        window["-INSTRUCTION-"].update("Describe the picture:")

    if event == "-INPUT-":
        inpt = values["-INPUT-"]

    if event == "-ENTER-":
        inpt = inpt.lower()
        print(inpt)
        # here go into semantic parser
        lfs = gram.gen(inpt)
        for lf in lfs:
            print("\tLF: {}".format(lf))
            print('\tDenotation: {}'.format(gram.sem(lf)))
        print(guessed_blocks)
        guess = []
        for b in guessed_blocks:
            guess.append((b.y, b.x))
        Picture(name="guitest").mark(guess)
        window["-INSTRUCTION-"].update("Did you refer to this?")
        #picture = Picture(name="guitest").mark([(1,1)])
        window["-IMAGE-"].update(filename="guitest_guess.png")
        window["-INPUT-"].update("")
    if event == "-YES-":
        window["-INSTRUCTION-"].update("Awesome!")
    if event == "-NO-":
        # ask for next guess from parser
        picture = Picture(name="guitest").mark([(1,2)])
        window["-IMAGE-"].update(filename="guitest_guess.png")

window.close()
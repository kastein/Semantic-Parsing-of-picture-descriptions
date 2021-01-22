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
        sg.Text("Level 0, Picture 0:", key="-LEVEL-")
    ],
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
actualgame = sg.Window("Language Game", layout_game_screen)
window = start

level = 1
i_picture = 1
session_name = "pictures"


def picture_path(level, i_picture, session_name="pictures"):
    file_name = session_name + "_L" + str(level) + "_" + str(i_picture) + ".png"
    path_pict = "./" + session_name + "/" + file_name
    return path_pict


inpt = ""

while True:
    event, values = window.read()
    print(event, values)

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Beginning screen
    if event == "-START-":
        window.close()
        window = actualgame
        #startpic = True
        #window.read()
        #event, values = window.read()
        #picture = Picture(name="guitest").draw()
        #window["-IMAGE-"].update(filename="guitest.png")
        #continue


    # Displaying picture and taking input
    if event == "-NEXT-":
        picture = setPicParameters(level, i_picture, session_name).draw()
        window["-IMAGE-"].update(filename=picture_path(level, i_picture))
        window["-INSTRUCTION-"].update("Describe the picture:")
        window["-LEVEL-"].update("Level " + str(level) + ", Picture " + str(i_picture) + ":")
        if i_picture >= 10:
            i_picture = 0
            level += 1
        i_picture += 1


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
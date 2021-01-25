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
        sg.Button("Press here to show first picture", key="-NEXT-")
    ],
    [
        sg.Image(key="-IMAGE-")  # try to read in jpg.files
    ],
    [
        sg.Text("Describe the picture:", key="-INSTRUCTION-"), # store what is being typed, when person hits enter
        sg.In(size=(25, 1), enable_events=True, key="-INPUT-", disabled=True),
        sg.Button("Enter", key="-ENTER-", visible=False)
    ],
    [
        sg.Text("Did you refer to this?"),
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
actualgame = sg.Window("Language Game", layout_game_screen, return_keyboard_events=True)
window = start

level = 1
i_picture = 0
session_name = "pictures"


def picture_path(level, i_picture, session_name="pictures", guess=False):
    if not guess:
        file_name = session_name + "_L" + str(level) + "_" + str(i_picture) + ".png"
    else:
        file_name = session_name + "_L" + str(level) + "_" + str(i_picture) + "_guess.png"
    path_pict = "./" + session_name + "/" + file_name
    return path_pict

with open("evaluation.csv", "w", encoding="utf-8") as f:
    first_line = "picture,input,marked_picture,response\n"
    f.writelines(first_line)

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

    # Displaying picture and taking input
    if event == "-NEXT-":
        # hiding and unhiding
        window["-NEXT-"].hide_row()
        window["-YES-"].hide_row()
        window["-INPUT-"].update(disabled=False)
        window["-ENTER-"].update(visible=True)

        if i_picture >= 10:
            i_picture = 0
            level += 1
        i_picture += 1
        current_pic = setPicParameters(level, i_picture, session_name)
        current_pic.draw()
        # Katharina added following line
        create_all_blocks(current_pic)
        window["-IMAGE-"].update(filename=picture_path(level, i_picture))
        eval_picture = str(picture_path(level, i_picture))
        window["-INSTRUCTION-"].update("Describe the picture:")
        window["-LEVEL-"].update("Level " + str(level) + ", Picture " + str(i_picture) + ":")

    if event == "-INPUT-":
        inpt = values["-INPUT-"]

    if event == "-ENTER-":
        # hiding and unhiding
        window["-ENTER-"].hide_row()
        window["-YES-"].unhide_row()

        inpt = inpt.lower()
        print(inpt)
        eval_input = inpt

        # here go into semantic parser
        #guessed_blocks = []
        lfs = gram.gen(inpt)
        for lf in lfs:
            print("\tLF: {}".format(lf))
            print('\tDenotation: {}'.format(gram.sem(lf)))
        #print(guessed_blocks)
        # Katharina added following 2 lines
        if gram.sem(lf) == False:
            guessed_blocks.clear()
        guess = []
        for b in guessed_blocks:
            guess.append((b.y, b.x))
        print(guessed_blocks)
        guessed_blocks.clear()

        # mark the guessed blocks in the picture
        current_pic.mark(guess)
        window["-IMAGE-"].update(filename=picture_path(level, i_picture, guess=True))
        window["-INPUT-"].update("")
        eval_marked_picture = str(picture_path(level, i_picture, guess=True))

    if event == "-YES-":
        # hiding and unhiding
        window["-YES-"].hide_row()
        window["-ENTER-"].unhide_row()

        eval_response = "yes"
        with open("evaluation.csv", "a", encoding="utf-8") as f:
            line = eval_picture + "," + eval_input + "," + eval_marked_picture + "," + eval_response + "\n"
            f.writelines(line)

        if i_picture >= 10:
            i_picture = 0
            level += 1
        i_picture += 1
        current_pic = setPicParameters(level, i_picture, session_name)
        current_pic.draw()
        # Katharina added following line
        create_all_blocks(current_pic)
        window["-IMAGE-"].update(filename=picture_path(level, i_picture))
        eval_picture = str(picture_path(level, i_picture))
        window["-LEVEL-"].update("Level " + str(level) + ", Picture " + str(i_picture) + ":")

    if event == "-NO-":
        # hiding and unhiding
        # yet to come

        eval_response = "no"
        with open("evaluation.csv", "a", encoding="utf-8") as f:
            line = eval_picture + "," + eval_input + "," + eval_marked_picture + "," + eval_response + "\n"
            f.writelines(line)
        # ask for next guess from parser
        picture = Picture(name="guitest").mark([(1,2)])
        window["-IMAGE-"].update(filename="guitest_guess.png")

window.close()

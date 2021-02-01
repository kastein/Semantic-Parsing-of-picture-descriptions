import PySimpleGUI as sg
from BlockPictureGenerator import Picture
from grammar import *
import os.path
from PIL import Image, ImageTk
from PictureLevel import *
from Semantic_Learner import evaluate_semparse
import math

crude_lexicon={}
crude_rule = [('THE', 'the'),('LR', 'right'),('LR', 'left'),('TO', 'to'),('NEXT', 'next'),('B','[]'),('B','[(lambda b: b.shape == "rectangle")]'),('B','[(lambda b: b.shape == "triangle")]'),('B','[(lambda b: b.shape == "circle")]'),('C','green'),('C','yellow'),('C','blue'),('C','red'),('E','exist'),('I','identy'),('N','[2]'),('N','[3]'),('N','range(1,17)'),('N','[1]'),('U','under'),('U','over'),('AND','und')]


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
        guessed_blocks.clear()
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
   
        for word in inpt.split():
            if not word in crude_lexicon:
                crude_lexicon[word]=crude_rule[:]
        gram = Grammar(crude_lexicon,rules,functions)

        # here go into semantic parser
        #guessed_blocks = []
        lfs = iter(gram.gen(inpt))
        #for lf in lfs:
            #print("\tLF: {}".format(lf))
            #print('\tDenotation: {}'.format(gram.sem(lf)))
        #print(guessed_blocks)
        # Katharina added following 2 lines
        lf = next(lfs)
        while gram.sem(lf) == False:
            guessed_blocks.clear()
            lf=next(lfs)
            
        print(lf,gram.sem(lf))
        print(guessed_blocks)
        guess = []
        print("GUESSEDBLOCKS",guessed_blocks)
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
        weights = evaluate_semparse(inpt,lf,gram)
        minrule = None
        minprob = math.inf
        minword = None
        for w in weights:
            if len(w)==2:
                rule,word = w
                prob = weights[w]
                if prob < minprob:
                    minprob = prob
                    minrule = rule
                    minword = word
        #print(minprob,minword,minrule)
        #print("DELETE:",minword,minrule)
        crude_lexicon[minword].remove(minrule)
        """for word in crude_lexicon:
            print(word)
            for rule in crude_lexicon[word]:
                print(rule)"""
        gram = Grammar(crude_lexicon,rules,functions)
                       
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
        # ask for next guess from parser
        try:
            guessed_blocks.clear()
            lf = next(lfs)
            while gram.sem(lf) == False:
                guessed_blocks.clear()
                lf=next(lfs)
            guess = []
            print("GUESSEDBLOCKS",guessed_blocks)
            for b in guessed_blocks:
                guess.append((b.y, b.x))
            guessed_blocks.clear()
            current_pic.mark(guess)
            window["-IMAGE-"].update(filename=picture_path(level, i_picture, guess=True))
            window["-INPUT-"].update("")
            eval_marked_picture = str(picture_path(level, i_picture, guess=True))

        
            eval_response = "no"
            with open("evaluation.csv", "a", encoding="utf-8") as f:
                line = eval_picture + "," + eval_input + "," + eval_marked_picture + "," + eval_response + "\n"
                f.writelines(line)
        except StopIteration:
            window["-YES-"].hide_row()
            window["-ENTER-"].unhide_row()
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
        
       

window.close()

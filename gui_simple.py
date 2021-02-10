import PySimpleGUI as sg
from BlockPictureGenerator import Picture
from grammar import *
import os
from PIL import Image, ImageTk
from PictureLevel import *
from Semantic_Learner import evaluate_semparse
import math
from collections import defaultdict
from cossimforstem import sim_stemm

crude_lexicon={}
crude_rule = [('THE', 'the'),('LR', 'right'),('LR', 'left'),('TO', 'to'),('NEXT', 'next'),('B','[]'),('B','[(lambda b: b.shape == "rectangle")]'),('B','[(lambda b: b.shape == "triangle")]'),('B','[(lambda b: b.shape == "circle")]'),('C','green'),('C','yellow'),('C','blue'),('C','red'),('E','exist'),('I','identy'),('N','[2]'),('N','[3]'),('N','range(1,17)'),('N','[1]'),('U','under'),('U','over'),('AND','und')]
threshold = -0.5
total_scores = defaultdict(lambda:defaultdict(int))

starting_screen = [
    [
        sg.Text("Hello! -Description-\nthis is a test")
    ],
    [
       sg.Text("Press 'Start Game' to start the game.")
    ],
    [
        sg.Text("Please enter session name:"),
        sg.In(size=(25, 1), enable_events=True, key="-SESSION-"),
        sg.Button("Start Game", key="-START-", disabled=True)
    ]
]

game_screen = [
    [
        sg.Text("Level xx, Picture xx:", key="-LEVEL-")
    ],
    [
        sg.Text("only describe one block, e.g.: 'There is a red circle'", key="-DESCRIPTION-")
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
#session_name = "pics"


def picture_path(level, i_picture, session_name, guess=False):
    if not guess:
        file_name = session_name + "_L" + str(level) + "_" + str(i_picture) + ".png"
    else:
        file_name = session_name + "_L" + str(level) + "_" + str(i_picture) + "_guess.png"
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
        os.mkdir(session_name)
        evaluation_file = "./" + session_name + "/evaluation.csv"
        with open(evaluation_file, "w", encoding="utf-8") as f:
            first_line = "n\tlevel\tpicture\tinput\tmarked_picture\tattempts\ttree\n"
            f.writelines(first_line)
        window.close()
        window = actualgame

    if event == "-SESSION-":
        session_name = values["-SESSION-"]
        window["-START-"].update(disabled=False)

    # Displaying picture and taking input
    if event == "-NEXT-":
        guessed_blocks.clear()
        # hiding and unhiding
        window["-NEXT-"].hide_row()
        window["-YES-"].hide_row()
        window["-INPUT-"].update(disabled=False)
        window["-ENTER-"].update(visible=True)

        n = 1
        if i_picture >= 10:
            i_picture = 0
            level += 1
        i_picture += 1
        current_pic = setPicParameters(level, i_picture, session_name)
        current_pic.draw()
        # Katharina added following line
        create_all_blocks(current_pic)
        window["-IMAGE-"].update(filename=picture_path(level, i_picture, session_name))
        eval_picture = str(picture_path(level, i_picture, session_name))
        window["-INSTRUCTION-"].update("Describe the picture:")
        window["-LEVEL-"].update("Level " + str(level) + ", Picture " + str(i_picture) + ":")
        eval_attempts = 0

    if event == "-INPUT-":
        inpt = values["-INPUT-"]

    if event == "-ENTER-":
        # hiding and unhiding
        #window["-ENTER-"].hide_row()
        window["-INPUT-"].update(disabled=True)
        window["-ENTER-"].update(visible=False)
        window["-YES-"].unhide_row()
        inpt = sim_stemm(inpt.lower(),list(crude_lexicon))
        print(inpt)
        eval_input = inpt
   
        for word in inpt.split():
            if not word in crude_lexicon:
                crude_lexicon[word]=crude_rule[:]
                for rule in crude_rule:
                    total_scores[word][rule]=0
        gram = Grammar(crude_lexicon,rules,functions)

        # here go into semantic parser
        #guessed_blocks = []
        lfs = iter(gram.gen(inpt))
        #for lf in lfs:
            #print("\tLF: {}".format(lf))
            #print('\tDenotation: {}'.format(gram.sem(lf)))
        #print(guessed_blocks)
        # Katharina added following 2 lines
        guessed_blocks.clear()
        try:
            lf = next(lfs)
            while gram.sem(lf) == False:
                guessed_blocks.clear()
                lf=next(lfs)
            guess = []
            for b in guessed_blocks:
                guess.append((b.y, b.x))
            guessed_blocks.clear()

            # mark the guessed blocks in the picture
            current_pic.mark(guess)
            window["-IMAGE-"].update(filename=picture_path(level, i_picture, session_name, guess=True))
            #window["-INPUT-"].update("")
            eval_marked_picture = str(picture_path(level, i_picture, session_name, guess=True))
        except StopIteration:
            pass

    if event == "-YES-":
        guessed_blocks.clear()
        # hiding and unhiding
        window["-YES-"].hide_row()
        window["-ENTER-"].unhide_row()
        window["-INPUT-"].update(disabled=False)
        window["-ENTER-"].update(visible=True)

        window["-INPUT-"].update("")
        weights = evaluate_semparse(inpt,lf,gram)
        print("TEST",[weights[key] for key in weights],[0.0 for word in inpt],len(inpt.split()))
        if [weights[key] for key in weights] == [0.0 for word in inpt.split()]:
            print("Works!")
            for w in weights:
                if len(w)==2:
                    rule,word = w
                    crude_lexicon[word]=[rule]
        else:
            for w in weights:
                if len(w)==2:
                    rule,word = w
                    score = weights[w]
                    total_scores[word][rule]+=score
                    if total_scores[word][rule]<=threshold :
                        del total_scores[word][rule]
                        print("DELETE:",word,rule)
                        crude_lexicon[word].remove(rule)       
       
        gram = Grammar(crude_lexicon,rules,functions)
        for word in crude_lexicon:
            print(word,len(crude_lexicon[word]))
        eval_response = "yes"
        eval_attempts += 1
        with open(evaluation_file, "a", encoding="utf-8") as f:
            line = str(n) + "\t" + str(level) + "\t" + eval_picture + "\t" + eval_input + "\t" + eval_marked_picture + "\t" + str(eval_attempts) + "\t" + str(lf) + "\n"
            f.writelines(line)

        n += 1
        if i_picture >= 10:
            i_picture = 0
            level += 1
            window["-DESCRIPTION-"].update("something else")
        i_picture += 1
        current_pic = setPicParameters(level, i_picture, session_name)
        current_pic.draw()
        # Katharina added following line
        create_all_blocks(current_pic)
        window["-IMAGE-"].update(filename=picture_path(level, i_picture, session_name))
        eval_picture = str(picture_path(level, i_picture, session_name))
        window["-LEVEL-"].update("Level " + str(level) + ", Picture " + str(i_picture) + ":")
        eval_attempts = 0

    if event == "-NO-":
        # hiding and unhiding
        # yet to come
        # ask for next guess from parser
        guessed_blocks.clear()
        try:
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
            window["-IMAGE-"].update(filename=picture_path(level, i_picture, session_name, guess=True))
            #?
            #window["-INPUT-"].update("")
            eval_marked_picture = str(picture_path(level, i_picture, session_name, guess=True))
            eval_attempts += 1

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
            window["-IMAGE-"].update(filename=picture_path(level, i_picture, session_name))
            eval_picture = str(picture_path(level, i_picture))
            window["-LEVEL-"].update("Level " + str(level) + ", Picture " + str(i_picture) + ":")
        
       

window.close()

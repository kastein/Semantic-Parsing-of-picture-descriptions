import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk

first_item = [
    [
        sg.Image("ProjectSketch.png"),  # try to read in jpg.files
    ],
    [
        sg.Text("Describe the picture:"), # store what is being typed, when person hits enter
        sg.In(size=(25, 1), enable_events=True, key="-INPUT-"),
        sg.Button("Enter")
    ]
]

layout = [
    [
        sg.Column(first_item)
    ]
]

window = sg.Window("My Program", layout)

inpt = None
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-INPUT-":
        inpt = values["-INPUT-"]
    if event == "Enter":
        print(inpt)

window.close()
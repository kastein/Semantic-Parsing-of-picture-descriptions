# Semantic-Parsing-of-picture-descriptions
This project is part of the Softwareproject "Language, Action and Perception".

General research question:  Can we implement a model that learns a natural language from scratch through interaction?

Focused research question:  Can we teach a computer a mapping from natural language picture descriptions to a logical representation?

## Demo of current Status

To play the current status of our language learning game you only have to clone the repository and run the gui_simple.py script.

**Requirements**<br>
Python 3 <br>
package tkinter <br>
package PIL <br>
package PySimpleGUI <br>


## Files 
* folder marked_pictures: pictures with guessed blocks for the test sentences
* folder pictures: example pictures as created by PictureLevel.py

* BlockPictureGenerator.py: automatically creates and saves the pictures 
* CalculCoordinates.py: used to calculate the coordinates for the picture generation in BlockPictureGenerator.py
* Parser.py
* PictureLevel.py: generates a picture for a specified level by calling BlockPictureGenerator.py with corresponding parameters
* grammar.py:
* gui_simple: working GUI
* learning.py
* semdata.py:

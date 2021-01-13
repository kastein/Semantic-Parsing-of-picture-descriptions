# Semantic-Parsing-of-picture-descriptions
This project is part of the Softwareproject "Language, Action and Perception".

General research question:  Can we implement a model that learns a natural language from scratch through interaction?

Focused research question:  Can we teach a computer a mapping from natural language picture descriptions to a logical representation?

**Files**
* folder pictures: example pictures as created by PictureLevel.py
* BlockPictureGenerator.py: automatically creates and saves the pictures 
* CalculCoordinates.py: used to calculate the coordinates for the picture generation in BlockPictureGenerator.py
* Interface_sketch.pptx: sketch of the GUI design and how parts of the whole program will have to work together 
* MatrixToLogic.py: generates logic representation for a picture, probably not needed anymore as logic interpretation is taken care of in the grammar/parser
* PictureLevel.py: generates a picture for a specified level by calling BlockPictureGenerator.py with corresponding parameters
* ProjectSketch.png: example picture for testing the interface
* grammar.py:
* gui_simple: fist try of creating the GUI
* semdata.py:
* world.jpg: example picture for testing and developing of grammar.py
* world.py: list for example picture for testing and developing of grammar.py

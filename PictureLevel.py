from BlockPictureGenerator import *

"""
Number of levels and the corresponding complexity is chosen randomly so far
You have to make a subdirectory called "pictures" in order to get this work (later the subdirectory should
be created when starting the language learning game)
"""

def setPicParameters(level, i_picture, session_name):
    """
    creates a Picture object where the number of shown blocks is based on the current level
    returns the picture object after storing it in the subfolder session_name and giving it a unique file name
    level: numer (int) of the current level
    i_picture: number (int) of the current picture in the current level
    session_name: name of the current session
    returns: the Picture Object
    """

    file_name = session_name + "_L" + str(level) + "_" + str(i_picture)
    path_pict = "./" + session_name + "/" + file_name
    
    if level == 1:
        complexity = (3,4)

    elif level == 2:
        complexity = (3,4)
        
    elif level == 3:
        complexity = (3, 9)

    elif level == 4:
        complexity = (5, 15)

    # full picture at the end
    else:
        complexity = (16,17)

    current_picture = Picture(complexity, path_pict)
    return current_picture

if __name__=="__main__":
    test_picture = setPicParameters(1, 1, "pictures")
    test_picture.draw()

    test_picture = setPicParameters(1, 2, "pictures")
    test_picture.draw()

    test_picture = setPicParameters(1, 3, "pictures")
    test_picture.draw()

    test_picture = setPicParameters(1, 4, "pictures")
    test_picture.draw()

    test_picture = setPicParameters(1, 5, "pictures")
    test_picture.draw()

    test_picture = setPicParameters(1, 6, "pictures")
    test_picture.draw()

    test_picture = setPicParameters(1, 7, "pictures")
    test_picture.draw()

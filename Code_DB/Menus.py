# Menu systems of the game

# pip install opencv-python
from Loadpng import *
import os

def TitleImage(file):
    """ Converts an image to an Ascii screen """
    save_path = os.getcwd()
    if not os.path.exists(save_path + '\\' + file):
        print('Title file has been removed and cannot be found. Please place ' + file + ' back into game directory.')
        return []
    titleData = []
    img = load_image(file)
    height = img.get_height()
    width = img.get_width()

    for row in range(height):
        row_of_colors = []
        for col in range(width):
            row_of_colors += [img.get_pixel(row, col)]
        titleData += [row_of_colors]
    
    return titleData

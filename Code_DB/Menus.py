# Menu systems of the game

# pip install opencv-python
from Loadpng import *
import os
import SaveGame

# Title menu options : Text, Show if game is not playing, Option Selection Tag
TITLE_MENU = [
    ['Python Rogue : Intro to Computing', True, ''],
    ['---------------------------------', True, ''],
    ['         Continue', False, 'Back'],
    ['         New Game', True, 'New'],
    ['         Load Game', True, 'Load'],
    ['         Save Game', False, 'Save'],
    ['         Quit', True, 'Quit']
]

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

def GetSaveFiles(maxLength, page = 0):
    """ Gets a list of the save files """
    save_file_list = SaveGame.GetAllSaves()
    save_index = 1
    save_choices = { 0 : '<Back>'}
    for name in range(maxLength * page, maxLength * (page + 1)):
        if name < len(save_file_list):
            save_choices[save_index] = save_file_list[name].split('.')[0]
            save_index += 1
        else: # we reached the end of the names
            return save_choices
    if name < save_file_list.count: # Allow the next option if there are more choices to be made
        save_choices[save_index] = '<Next>'
    return save_choices
# Screens for viewing in 'Python Roguelike'
# Menus have also been moved here to lower file count, as they
# serve mostly the same function as Screens do, and all are part of the
# UI now.
#
# ASCII Lookup chart at:
# https://python-tcod.readthedocs.io/en/latest/tcod/charmap-reference.html

from Map import *
# pip install opencv-python : May use this instead of Loadpng.py
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

# Character Generation Options: Text, gap to print after text, Secondary Print ID
CHARACTER_GENERATOR = [
    ['        New Character :          ', 0, ''],
    ['---------------------------------', 0, ''],
    ['  Name: ', 8, '<Name>'],
    ['  World Name: ', 14, '<Seed>'],
    ['', 2, '<Classes>']
]

ALPHA_INPUT = {
    tcod.event.K_a : 'a',
    tcod.event.K_b : 'b',
    tcod.event.K_c : 'c',
    tcod.event.K_d : 'd',
    tcod.event.K_e : 'e',
    tcod.event.K_f : 'f',
    tcod.event.K_g : 'g',
    tcod.event.K_h : 'h',
    tcod.event.K_i : 'i',
    tcod.event.K_j : 'j',
    tcod.event.K_k : 'k',
    tcod.event.K_l : 'l',
    tcod.event.K_m : 'm',
    tcod.event.K_n : 'n',
    tcod.event.K_o : 'o',
    tcod.event.K_p : 'p',
    tcod.event.K_q : 'q',
    tcod.event.K_r : 'r',
    tcod.event.K_s : 's',
    tcod.event.K_t : 't',
    tcod.event.K_u : 'u',
    tcod.event.K_v : 'v',
    tcod.event.K_w : 'w',
    tcod.event.K_x : 'x',
    tcod.event.K_y : 'y',
    tcod.event.K_z : 'z',
    tcod.event.K_1 : '1',
    tcod.event.K_2 : '2',
    tcod.event.K_3 : '3',
    tcod.event.K_4 : '4',
    tcod.event.K_5 : '5',
    tcod.event.K_6 : '6',
    tcod.event.K_7 : '7',
    tcod.event.K_8 : '8',
    tcod.event.K_9 : '9',
    tcod.event.K_0 : '0',
    tcod.event.K_SPACE : ' ',
    tcod.event.K_BACKSPACE : 'Remove',
}

def Title(width, height):
    """Title Screen"""
    s = []
    for y in range(height):
        line = ""
        for x in range(width):
            if x == 0 and y == 0:
                line += chr(0x2554) # Upper Left Corner
            elif x == 0 and y == height - 1:
                line += chr(0x255A) # Lower Left Corner
            elif x == width - 1 and y == 0:
                line += chr(0x2557) # Upper Right Corner
            elif x == width - 1 and y == height - 1:
                line += chr(0x255D) # Lower Right Corner
            elif x == 0 or x == width - 1:
                line += chr(0x2551) # Left/Right Border
            elif y == 0 or y == height - 1:
                line += chr(0x2550) # Top/Bottom Border
            else:
                line += ' '
        s.append(line)
    return s

def WorldUI(width, height):
    """ Draw the game UI for the display """
    s = []
    for y in range(height):
        line = ""
        for x in range(width):
            if x == 0 and y == 0:
                line += chr(0x2554) # Upper Left Corner
            elif x == 0 and y == height - 1:
                line += chr(0x255A) # Lower Left Corner
            elif x == width - 1 and y == 0:
                line += chr(0x2557) # Upper Right Corner
            elif x == width - 1 and y == height - 1:
                line += chr(0x255D) # Lower Right Corner
            elif x == WorldMap.MAP_VIEW_WIDTH  + 1 and y == WorldMap.MAP_VIEW_HEIGHT + 1:
                line += chr(0x255D)
            elif x == 0 and y == WorldMap.MAP_VIEW_HEIGHT + 1:
                line += chr(0x2560) # Up/Down/Right Border T
            elif y == 0 and x == WorldMap.MAP_VIEW_WIDTH + 1:
                line += chr(0x2566) # Left/Right/Down Border T
            elif 0 < y <= WorldMap.MAP_VIEW_HEIGHT and x == WorldMap.MAP_VIEW_WIDTH + 1:
                line += chr(0x2551)
            elif x == 0 or x == width - 1:
                line += chr(0x2551) # Left/Right Border
            elif 0 < x <= WorldMap.MAP_VIEW_WIDTH and y == WorldMap.MAP_VIEW_HEIGHT + 1:
                line += chr(0x2550)
            elif y == 0 or y == height - 1:
                line += chr(0x2550) # Top/Bottom Border
            else:
                line += ' '
        s.append(line)
    return s

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
    if name < len(save_file_list): # Allow the next option if there are more choices to be made
        save_choices[save_index] = '<Next>'
    return save_choices
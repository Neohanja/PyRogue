# Screens for viewing in 'Python Roguelike'
# ASCII Lookup chart at:
# https://python-tcod.readthedocs.io/en/latest/tcod/charmap-reference.html

from Map import *
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

CHARACTER_GENERATOR = [
    ['        New Character :          ', 0, ''],
    ['---------------------------------', 0, ''],
    ['  Name: ', 8, '<Name>'],
    ['  World Name: ', 14, '<Seed>'],
    ['', 2, '<Classes>']
]

ALPHA_INPUT = {
    tcod.event.K_a : ['a', 'A'],
    tcod.event.K_b : ['b', 'B'],
    tcod.event.K_c : ['c', 'C'],
    tcod.event.K_d : ['d', 'D'],
    tcod.event.K_e : ['e', 'E'],
    tcod.event.K_f : ['f', 'F'],
    tcod.event.K_g : ['g', 'G'],
    tcod.event.K_h : ['h', 'H'],
    tcod.event.K_i : ['i', 'I'],
    tcod.event.K_j : ['j', 'J'],
    tcod.event.K_k : ['k', 'K'],
    tcod.event.K_l : ['l', 'L'],
    tcod.event.K_m : ['m', 'M'],
    tcod.event.K_n : ['n', 'N'],
    tcod.event.K_o : ['o', 'O'],
    tcod.event.K_p : ['p', 'P'],
    tcod.event.K_q : ['q', 'Q'],
    tcod.event.K_r : ['r', 'R'],
    tcod.event.K_s : ['s', 'S'],
    tcod.event.K_t : ['t', 'T'],
    tcod.event.K_u : ['u', 'U'],
    tcod.event.K_v : ['v', 'V'],
    tcod.event.K_w : ['w', 'W'],
    tcod.event.K_x : ['x', 'X'],
    tcod.event.K_y : ['y', 'Y'],
    tcod.event.K_z : ['z', 'Z'],
    tcod.event.K_BACKSPACE : ['Remove', 'Remove'],
    tcod.event.K_LSHIFT : ['Caplock', 'Caplock'],
    tcod.event.K_RSHIFT : ['Caplock', 'Caplock'],
    tcod.event.K_RETURN : ['Next', 'Next']
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
    if name < save_file_list.count: # Allow the next option if there are more choices to be made
        save_choices[save_index] = '<Next>'
    return save_choices
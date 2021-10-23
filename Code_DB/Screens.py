# Screens for viewing in 'Python Roguelike'
# ASCII Lookup chart at:
# https://python-tcod.readthedocs.io/en/latest/tcod/charmap-reference.html

from Map import *

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
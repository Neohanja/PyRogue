# Processes saved games
import os
# Remove references later, added for intellisense usage
from AIManager import *
from Map import *

GAME_SAVE_EXTENTION = '.txt' # For testing only
GAME_MAP_BREAK = '<NEXT>'

def SaveGame(mapData : WorldMap, actorData : AI_Manager):
    """ Saves the game information to a file """
    save_dir = os.getcwd() + r'\Saves'
    # Create the directory if it does not exist yet
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # ensure the save and map data exist
    if actorData == None or mapData == None:
        print('No data to save')
        return
    file_name = '\\' + actorData.player.name + GAME_SAVE_EXTENTION
    saver = open(save_dir + file_name, 'w')
    # Player info: sd = Save Data
    sd = []
    sd += actorData.SaveActors()
    sd += mapData.SaveMapData()
    sd += ['<EOF>']
    
    saver.writelines(sd)
    saver.close()

def LoadGame():
    """ Reads in a file to load the game information """
    pass
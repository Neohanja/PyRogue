# Processes saved games
import os

GAME_SAVE_EXTENTION = '.txt' # For testing only

def SaveGame(mapData, actorData):
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

def LoadGame(character_name : str, aiEngine, mapEngine):
    """ Reads in a file to load the game information """
    save_dir = os.getcwd() + r'\Saves'
    if not os.path.exists(save_dir):
        print('Save File required to be in correct directory.')
        return

    file_name = '\\' + character_name + GAME_SAVE_EXTENTION    
    if not os.path.exists(save_dir + file_name):
        print('File ' + file_name + ' does not exist or is incorrect directory.')
        return

    ai = []
    map = []

    save_file = open(save_dir + file_name, 'r')
    for line in save_file.readlines():
        line_type = line.split(';')[0]
        if line_type == '<MAP>':
            map.append(line)
        elif line_type == '<PLAYER>' or line_type == '<MONSTER>' or line_type == '<NPC>':
            ai.append(line)
        elif line_type == '<EOF>':
            break
    save_file.close()

    aiEngine.LoadActors(ai)
    mapEngine.LoadMapData(map)
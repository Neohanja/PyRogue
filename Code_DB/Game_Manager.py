# Manages the many aspects of the game, 
# to include a game loop

from Map import *
import AIManager
import Player
from Messenger import *
from NameGen import *
from MathFun import *
import SaveGame
from Screens import *
from Action import *
from Input_Handlers import *

TITLE_IMAGE = 'Title.png'

WORLD_WIDTH = 256
WORLD_HEIGHT = 256
# Game State Info
# States not yet used:
# Dialog Loop
# Stat Screen
# Help Menu
# Story Page - WIP
PLAY_STATE = [
    'Main Menu', 'Help Menu', 'Story Page', 'Dialog Loop', 'Stat Screen', 
    'Game Loop', 'Load Menu', 'CharGen', 'Loading' ]
MAIN_MENU = 0
HELP_MENU = 1
STORY_PAGE = 2
DIALOG_LOOP = 3
STAT_PAGE = 4
GAME_LOOP = 5
LOAD_MENU = 6
CHAR_GEN = 7
LOADING = 8

class GameManager:
    """ Game Manager """

    def __init__(self, Screen_Size : Vec2):
        """ Game Manager Constructor """        
        self.screenSize = Screen_Size
        self.playState = PLAY_STATE[MAIN_MENU] # Initialize the game state from the list of options (Enumeration)
        self.gamePlaying = False # Determines if the game is currently running or not.
        self.titleFull = True # Debugging option, and to show the full title menu or just the image.
        self.titleData = TitleImage(TITLE_IMAGE) # Preload the title image, so it isn't loading EVERY frame

        # for menu sequences
        self.cursorLoc = Vec2(0, 0)
        self.previousLoc = Vec2(0, 0)
        self.maxOptions = 5
        self.menuOptions = {}
        self.page = 0

        # general data for new games
        self.newName = ''
        self.seedName = ''
        self.textLock = False # For any time a text entry is being used
        self.loadingSave = False # Since it takes a few seconds to load from a 'new' a new game
        self.loadName = '' # What is the name of the save file we are loading?
    
    def Start(self):
        """ Start a new Game """
        # To-Do:
        # Character Generator
        if self.newName == '':
            self.newName = 'Default'
        if self.seedName == '':
            self.seedName = 'Drakland'

        self.world = WorldMap(WORLD_HEIGHT, WORLD_WIDTH, self.seedName)
        self.aiEngine = AIManager.AI_Manager(self.world, self, self.newName)
        self.aiEngine.ToggleDebug(True)
        self.mainCharacter = self.aiEngine.player

        sL = WorldMap.MAP_VIEW_HEIGHT + 2
        eL = self.screenSize.y - 1 - sL
        mL = WorldMap.MAP_VIEW_WIDTH - 10

        self.messenger = Messenger(sL, eL, mL)
        self.gamePlaying = True
        # Reset the name and seed for a possible new game
        self.newName = ''
        self.seedName = ''
        # Next line for testing messages that may need multiple lines
        # self.messenger.AddText('This needs to be super long to test this system and how it works, as well as getting the spacing correct for the word wrap. I\'m hoping all is well with it, since it didn\'t take long to make, compared to other systems that are just plain annoying.')
    
    # Update Loops for different game states

    def MainTitle(self, action):
        """ Main Menu Actions """
        if isinstance(action, MovementAction):
            # Move up or down on the menu
            self.cursorLoc.y = Clamp(0, self.maxOptions, self.cursorLoc.y + action.dy)
            return True
            
        elif isinstance(action, EnterAction):
            m_option = self.menuOptions[self.cursorLoc.y]
            if m_option == 'New':
                # Start with generating a new character, then the world
                self.playState = PLAY_STATE[CHAR_GEN]
                self.previousLoc.y = self.cursorLoc.y
                self.cursorLoc.y = 0
            elif m_option == 'Back':
                self.playState = PLAY_STATE[GAME_LOOP]
            elif m_option == 'Save':
                self.SaveGame()
                self.AddLog('Game Saved')
                self.playState = PLAY_STATE[GAME_LOOP]
            elif m_option == 'Load':
                # Need to go to a load menu.
                self.playState = PLAY_STATE[LOAD_MENU]
                self.previousLoc.y = self.cursorLoc.y
                self.cursorLoc.y = 0
            elif m_option == 'Quit':
                raise SystemExit()
            return True

        return False

    def LoadMenuSelections(self, action):
        """ A quick menu for the load options """
        if isinstance(action, MovementAction):
            # Move up or down on the menu
            self.cursorLoc.y = Clamp(0, self.maxOptions, self.cursorLoc.y + action.dy)
            return True
        elif isinstance(action, EscapeAction):
            # If the player presses escape, return them to the main menu
            self.page = 0
            self.cursorLoc.y = self.previousLoc.y
            self.previousLoc.y = 0
            self.playState = PLAY_STATE[MAIN_MENU]
            return True # Always return true if changing menues, as this refreshes the screen
        elif isinstance(action, EnterAction):
            m_option = self.menuOptions[self.cursorLoc.y]
            if m_option == '<Back>':
                if self.page > 0:
                    self.page -= 1
                else: # If this was the first page, go back to the main menu
                    self.cursorLoc.y = self.previousLoc.y
                    self.playState = PLAY_STATE[MAIN_MENU]
            elif m_option == '<Next>':
                self.cursorLoc.y = 0
                self.page += 1
            else:
                self.playState = PLAY_STATE[LOADING]
                self.loadName = m_option
                self.loadingSave = True
                self.page = 0
            return True
        return False

    def NewGameUpdate(self, action):
        """ When new game is selected : event system passed through for typing """
        if isinstance(action, EscapeAction):
            self.cursorLoc.y = self.previousLoc.y
            self.previousLoc.y = 0
            self.playState = PLAY_STATE[MAIN_MENU]
            return True
        
        elif isinstance(action, EnterAction): # New Game
            mSelection = self.menuOptions[self.cursorLoc.y]
            if mSelection == 'Start':
                self.gamePlaying = False
                self.playState = PLAY_STATE[LOADING] # Brings up a Loading screen
            elif mSelection == 'Name' or mSelection == 'Seed':
                self.textLock = not self.textLock
            return True
        
        elif self.textLock:
            mSelection = self.menuOptions[self.cursorLoc.y]
            nChar = action.letter
            if mSelection == 'Name':
                if nChar == 'Remove':
                    self.newName = self.newName[:len(self.newName) - 1]
                else:
                    self.newName += nChar
                self.newName = self.newName.title()
                return True
            elif mSelection == 'Seed':
                if nChar == 'Remove':
                    self.seedName = self.seedName[:len(self.seedName) - 1]
                else:
                    self.seedName += nChar
                self.seedName = self.seedName.title()
                return True

        elif isinstance(action, MovementAction) and not self.textLock:
            self.cursorLoc.y = Clamp(0, self.maxOptions, self.cursorLoc.y + action.dy)
            return True
        
        return False

    def GameLoopUpdate(self, action):
        """ Game Loop for Updating """
        if isinstance(action, MovementAction):  
            self.aiEngine.Update(Vec2(action.dx, action.dy))
            return True
        
        elif isinstance(action, UseAction):
            self.UseTerrain()
            return True

        elif isinstance(action, ExamineAction):
            self.messenger.AddText(self.world.GetExamineAction())
            return True

        elif isinstance(action, ToolTipUI):
            self.mainCharacter.ToggleTooltip()
            return True
                
        elif isinstance(action, EscapeAction):
            self.playState = PLAY_STATE[MAIN_MENU]
            self.cursorLoc.x = 0
            self.cursorLoc.y = 0
            return True

    def NewAndLoading(self, action):
        """ 
            Just a temp loading state for building game data. Since a new game/load file takes a few
            moments to load, we want a visual queue to inform the player something isn't broken.
        """
        if not self.gamePlaying:
            self.Start()

        if self.loadingSave:
            self.loadingSave = False
            self.LoadGame(self.loadName)
            self.AddLog('Game Loaded')            
            self.previousLoc.y = 0
            self.cursorLoc.y = 0

        self.playState = PLAY_STATE[GAME_LOOP]
        return True

    def Update(self, action):
        """ Actions to take during the game loop """
        refresh_screen = False

        if self.playState == PLAY_STATE[GAME_LOOP]:
            if self.GameLoopUpdate(action):
                refresh_screen = True
        elif self.playState == PLAY_STATE[MAIN_MENU]:
            if self.MainTitle(action):
                refresh_screen = True
        elif self.playState == PLAY_STATE[LOAD_MENU]:
            if self.LoadMenuSelections(action):
                refresh_screen = True
        elif self.playState == PLAY_STATE[CHAR_GEN]:
            if self.NewGameUpdate(action):
                refresh_screen = True
        elif self.playState == PLAY_STATE[LOADING]:
            if self.NewAndLoading(action):
                refresh_screen = True
        return refresh_screen

    # Draw Loops to update the screen

    def Draw(self, console):
        """ Draws updates to all game existances """
        if self.playState == PLAY_STATE[GAME_LOOP]:
            self.DrawWorld(console)
        elif self.playState == PLAY_STATE[MAIN_MENU]:
            self.DrawTitle(console)
        elif self.playState == PLAY_STATE[LOAD_MENU]:
            self.DrawLoadScreen(console)
        elif self.playState == PLAY_STATE[CHAR_GEN]:
            self.DrawCharacterGenerator(console)
        elif self.playState == PLAY_STATE[LOADING]:
            self.DrawGameLoading(console)

    def DrawLoadScreen(self, console):
        """ Draws the load screen, and borrows much of the code from the title """
        # Draw the UI
        border = Title(self.screenSize.x, self.screenSize.y)
        for line in range(len(border)):
                    console.print(x=0,y=line, string = border[line])
        height = len(self.titleData)
        width = len(self.titleData[0])
        for r in range(height):
            for c in range(width):
                console.print(x = 1 + c, y = 1 + r, string = 'X', fg = self.titleData[r][c])

        for r in range(30):
            for c in range(35):
                # Clear the box and reset the text color
                console.print(x = c + 20, y = r + 20, string = ' ', fg = [255,255,255])
        
        console.print(x = 30, y = 21, string = 'Saved Games')
        console.print(x = 21, y = 23, string = TITLE_MENU[1][0]) # --- block (for consistency)

        self.menuOptions = GetSaveFiles(10, self.page)

        for index in self.menuOptions.keys():
            self.maxOptions = index
            console.print(x = 30, y = 25 + (index * 2), string = self.menuOptions[index])
        
        # Print the user cursor
        console.print(x = 28, y = 25 + (self.cursorLoc.y * 2), string = '>')

    def DrawTitle(self, console):
        """ Draw the title screen, or the first screen seen by the player before their adventure begins"""
        # Draw the UI
        border = Title(self.screenSize.x, self.screenSize.y)
        for line in range(len(border)):
                    console.print(x=0,y=line, string = border[line])
        height = len(self.titleData)
        width = len(self.titleData[0])
        for r in range(height):
            for c in range(width):
                console.print(x = 1 + c, y = 1 + r, string = 'X', fg = self.titleData[r][c])

        if self.titleFull:
            for r in range(30):
                for c in range(35):
                    # Clear the box and reset the text color
                    console.print(x = c + 20, y = r + 20, string = ' ', fg = [255,255,255])
            line = 0
            # account for the title bar from the "max options"
            self.maxOptions = -1
            for text in TITLE_MENU:
                if text[1] or self.gamePlaying:
                    console.print(x = 21, y = 21 + (line * 2), string = text[0])                    
                    if text[2] != '':
                        self.maxOptions += 1
                        self.menuOptions[self.maxOptions] = text[2]                        
                    line += 1
            # Print the user cursor
            console.print(x = 28, y = 25 + (self.cursorLoc.y * 2), string = '>')
            console.print(x = 40, y = 25 + (self.cursorLoc.y * 2), string = '<')

    def DrawCharacterGenerator(self, console):
        """ Draws the UI and elements of the character generator screen """
        border = WorldUI(self.screenSize.x, self.screenSize.y)
        for line in range(len(border)):
            console.print(x=0,y=line, string = border[line])
        
        y_pos = 3
        op = 0
        for cs_Menu in CHARACTER_GENERATOR:
            if cs_Menu[2] == '':
                console.print(x = 3, y = y_pos, string = cs_Menu[0])
                y_pos += 2
            elif cs_Menu[2] == '<Name>':
                self.menuOptions[op] = 'Name'
                op += 1
                p_name = self.newName
                c_name = [255,255,255]
                if self.newName == '':
                    p_name = 'Default'
                if self.textLock and self.menuOptions[self.cursorLoc.y] == 'Name':
                    c_name = ColorPallet.GetColor('Portal')
                console.print(x = 3, y = y_pos, string = cs_Menu[0])
                # will do color in a little bit to notify modificaiton
                console.print(x = 3 + cs_Menu[1], y = y_pos, string = p_name, fg = c_name)
                y_pos += 2
            elif cs_Menu[2] == '<Seed>':
                self.menuOptions[op] = 'Seed'
                op += 1
                c_seed = [255,255,255]
                p_seed = self.seedName
                if self.seedName == '':
                    p_seed = 'Drakland'
                if self.textLock and self.menuOptions[self.cursorLoc.y] == 'Seed':
                    c_seed = ColorPallet.GetColor('Portal')
                console.print(x = 3, y = y_pos, string = cs_Menu[0])
                # will do color in a little bit to notify modificaiton
                console.print(x = 3 + cs_Menu[1], y = y_pos, string = p_seed, fg = c_seed)
                y_pos += 2
            elif cs_Menu[2] == '<Classes>':
                for cName in Player.CLASSES.keys():
                    self.menuOptions[op] = cName
                    op += 1
                    console.print(x = 5, y = y_pos, string = cName)
                    y_pos += 2
        console.print(x = 5, y = y_pos, string = '<Start>')
        self.menuOptions[op] = 'Start'
        self.maxOptions = op
        console.print(x = 3, y = 7 + (self.cursorLoc.y * 2), string = '>')

    def DrawWorld(self, console):
        """ Draw updates to all game existances """
        # Draw the UI
        border = WorldUI(self.screenSize.x, self.screenSize.y)
        for line in range(len(border)):
            console.print(x=0,y=line, string = border[line])
        # Find the Upper Left corner
        max_x = self.world.overworld[HEADER][MAP_WIDTH] - WorldMap.MAP_VIEW_WIDTH + 1
        max_y = self.world.overworld[HEADER][MAP_HEIGHT] - WorldMap.MAP_VIEW_HEIGHT + 1
        corner = Vec2(
                    Clamp(0, max_x, self.aiEngine.player.position.x - (WorldMap.MAP_VIEW_WIDTH // 2)),
                    Clamp(0, max_y, self.aiEngine.player.position.y - (WorldMap.MAP_VIEW_HEIGHT // 2)))

        # Draw everything else
        self.world.Draw(corner, console)
        self.aiEngine.Draw(console, corner)
        # Draw the messanger system info
        self.messenger.PrintText(console)

    def DrawGameLoading(self, console):
        """ Because it takes a few moments to load the new/saved games, make an indicator of such """
        wording = 'Loading, please wait...'
        yLoc = self.screenSize.y // 2
        xLoc = self.screenSize.x // 2 - len(wording) // 2 - 1
        border = Title(self.screenSize.x, self.screenSize.y)
        for line in range(len(border)):
                    console.print(x=0,y=line, string = border[line])

        for letter in wording:
            r = random.randint(125, 255)
            g = random.randint(125, 255)
            b = random.randint(125, 255)
            console.print(x = xLoc, y = yLoc, string = letter, fg = [r, g, b])
            xLoc += 1

    # Helper functions

    def AddLog(self, message : str):
        """ Adds a message to the messenger log. Added to game manager for ease of access """
        self.messenger.AddText(message)

    def UseTerrain(self):
        """ Uses the terrain feature located at player's location """
        # Determine the feature at this location
        feature = self.world.GetTerrainFeature(self.aiEngine.player.Position(), True)
        # Get the player location 
        loc = str(self.aiEngine.player.position.x) + ',' + str(self.aiEngine.player.position.y)
        change_map = False
        new_point = Vec2(0, 0)
        mapLoc = ''

        if feature == "Town":
            mapLoc = 't:' + loc
            if loc not in self.world.towns:
                # Create and populate the new town
                self.world.BuildTown(loc)
                self.aiEngine.PopulateNPCs(mapLoc, self.world.towns[loc][HEADER])
            self.messenger.AddText('Welcome to ' + self.world.towns[loc][HEADER][MAP_NAME] + '.')
            new_point = self.world.towns[loc][HEADER][TOWN_ENTRANCE]
            change_map = True
        elif feature == "Portal":
            loc += ',1'
            mapLoc = 'd:' + loc
            if loc not in self.world.dungeons:
                # Generate and populate the dungeon
                self.world.BuildDungeon(loc)
                self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[loc][HEADER], 1)
            self.messenger.AddText('You have entered ' + self.world.dungeons[loc][HEADER][MAP_NAME] + '.')
            new_point = self.world.dungeons[loc][HEADER][UPSTAIRS]
            
            change_map = True
        elif feature == "Upstairs":
            m = self.world.mapID.split(',')
            lvl = int(m[2]) # Get the current level
            if lvl <= 1:
                self.messenger.AddText('You Have escaped the dungeon, ' + self.world.dungeons[self.world.mapID][HEADER][MAP_NAME] + '.')
                new_point = Vec2(int(m[0]), int(m[1]))
                mapLoc = 'o:'
            else:
                self.messenger.AddText('You have traveled up a level in the dungeon.')
                new_map = m[0] + ',' + m[1] + ',' + str(lvl - 1)
                mapLoc = 'd:' + new_map
                # In the event this dungeon portion does not exist for some reason
                if new_map not in self.world.dungeons:
                    self.world.BuildDungeon(new_map)
                    self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[new_map][HEADER], lvl - 1)
                new_point = self.world.dungeons[new_map][HEADER][DOWNSTAIRS]
            change_map = True
        elif feature == "Downstairs":
            m = self.world.mapID.split(',')
            lvl = int(m[2])
            self.messenger.AddText('You have traveled down a level in the dungeon.')
            new_map = m[0] + ',' + m[1] + ',' + str(lvl + 1)
            mapLoc = 'd:' + new_map
            if new_map not in self.world.dungeons:
                # Create the new dungeon and populate it
                self.world.BuildDungeon(new_map)
                self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[new_map][HEADER], lvl + 1)
            new_point = self.world.dungeons[new_map][HEADER][UPSTAIRS]
            change_map = True

        if change_map:
            self.world.ChangeMap(mapLoc)
            self.aiEngine.player.SetSpawn(mapLoc, new_point)
    
    def SaveGame(self):
        """ Cleaning up, such as saving, on Exit """
        SaveGame.SaveGame(self.world, self.aiEngine)

    def LoadGame(self, file = 'Default'):
        """ Loads a specific game file """
        self.messenger.ClearScreen()
        SaveGame.LoadGame(file, self.aiEngine, self.world)
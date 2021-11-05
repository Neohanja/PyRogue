# Manages the many aspects of the game, 
# to include a game loop

import Map
import AIManager
import Menus
from Messenger import *
from NameGen import *
from MathFun import *
from SaveGame import *
from Screens import *
from Action import *
from Input_Handlers import *

WORLD_WIDTH = 256
WORLD_HEIGHT = 256
# Game State Info
PLAY_STATE = ['Main Menu', 'Help Menu', 'Story PAge', 'Dialog Loop', 'Stat Screen', 'Game Loop']
MAIN_MENU = 0
HELP_MENU = 1
STORY_PAGE = 2
DIALOG_LOOP = 3
STAT_PAGE = 4
GAME_LOOP = 5

class GameManager:
    """ Game Manager """

    def __init__(self, Screen_Size : Vec2, DebugMode = False):
        """ Game Manager Constructor """        
        self.width = Screen_Size.x
        self.height = Screen_Size.y
        self.playState = PLAY_STATE[MAIN_MENU]
        self.gamePlaying = True

        self.world = Map.WorldMap(WORLD_HEIGHT, WORLD_WIDTH)

        self.aiEngine = AIManager.AI_Manager(self.world, self)
        self.aiEngine.ToggleDebug(DebugMode)
        self.mainCharacter = self.aiEngine.player

        sL = Map.WorldMap.MAP_VIEW_HEIGHT + 2
        eL = Screen_Size.y - 1 - sL
        mL = Map.WorldMap.MAP_VIEW_WIDTH - 10

        self.messenger = Messenger(sL, eL, mL)
        # Next line for testing messages that may need multiple lines
        # self.messenger.AddText('This needs to be super long to test this system and how it works, as well as getting the spacing correct for the word wrap. I\'m hoping all is well with it, since it didn\'t take long to make, compared to other systems that are just plain annoying.')
    
    def Start(self):
        """ Pre-game stuff """
        pass

    # Update Loops for different game states

    def MainTitle(self, action):
        if isinstance(action, EscapeAction):
            raise SystemExit()

        elif isinstance(action, UseAction):
            self.playState = PLAY_STATE[GAME_LOOP]
            return True

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

        elif isinstance(action, SaveAction):
            self.SaveGame()
            self.AddLog('Game Saved')
            return True
        
        elif isinstance(action, LoadAction):
            self.LoadGame()
            self.AddLog('Game Loaded')
            return True
                
        elif isinstance(action, EscapeAction):
            self.playState = PLAY_STATE[MAIN_MENU]
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

        return refresh_screen # It shouldn't reach this point, but who knows

    # Draw Loops to update the screen

    def Draw(self, console):
        """ Draws updates to all game existances """
        if self.playState == PLAY_STATE[GAME_LOOP]:
            self.DrawWorld(console)
        if self.playState == PLAY_STATE[MAIN_MENU]:
            self.DrawTitle(console)

    def DrawTitle(self, console):
        # Draw the UI
        border = Title(self.width, self.height)
        for line in range(len(border)):
                    console.print(x=0,y=line, string = border[line])
        colorData = Menus.TitleImage('Title.png')
        height = len(colorData)
        width = len(colorData[0])
        for r in range(height):
            for c in range(width):
                console.print(x = 1 + c, y = 1 + r, string = 'X', fg = colorData[r][c])

    def DrawWorld(self, console):
        """ Draw updates to all game existances """
        # Draw the UI
        border = WorldUI(self.width, self.height)
        for line in range(len(border)):
                    console.print(x=0,y=line, string = border[line])
        # Find the Upper Left corner
        max_x = self.world.overworld[Map.HEADER][Map.MAP_WIDTH] - Map.WorldMap.MAP_VIEW_WIDTH + 1
        max_y = self.world.overworld[Map.HEADER][Map.MAP_HEIGHT] - Map.WorldMap.MAP_VIEW_HEIGHT + 1
        corner = Vec2(
                    Clamp(0, max_x, self.aiEngine.player.position.x - (Map.WorldMap.MAP_VIEW_WIDTH // 2)),
                    Clamp(0, max_y, self.aiEngine.player.position.y - (Map.WorldMap.MAP_VIEW_HEIGHT // 2)))

        # Draw everything else
        self.world.Draw(corner, console)
        self.aiEngine.Draw(console, corner)
        # Draw the messanger system info
        self.messenger.PrintText(console)

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
            if loc not in self.world.towns:
                # Create and populate the new town
                self.world.BuildTown(loc)
            self.messenger.AddText('Welcome to ' + self.world.towns[loc][Map.HEADER][Map.MAP_NAME] + '.')
            new_point = Vec2(self.world.towns[loc][Map.HEADER][Map.MAP_WIDTH]//2, self.world.towns[loc][Map.HEADER][Map.MAP_HEIGHT] - 1)
            mapLoc = 't:' + loc
            change_map = True
        elif feature == "Portal":
            loc += ',1'
            mapLoc = 'd:' + loc
            if loc not in self.world.dungeons:
                # Generate and populate the dungeon
                self.world.BuildDungeon(loc)
                self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[loc][Map.HEADER][Map.MAP_RNG], 1)
            self.messenger.AddText('You have entered ' + self.world.dungeons[loc][Map.HEADER][Map.MAP_NAME] + '.')
            new_point = Vec2(self.world.dungeons[loc][Map.HEADER][Map.UPSTAIRS].x, self.world.dungeons[loc][Map.HEADER][Map.UPSTAIRS].y)
            
            change_map = True
        elif feature == "Upstairs":
            m = self.world.mapID.split(',')
            lvl = int(m[2]) # Get the current level
            if lvl <= 1:
                self.messenger.AddText('You Have escaped the dungeon, ' + self.world.dungeons[self.world.mapID][Map.HEADER][Map.MAP_NAME] + '.')
                new_point = Vec2(int(m[0]), int(m[1]))
                mapLoc = 'o:'
            else:
                self.messenger.AddText('You have traveled up a level in the dungeon.')
                new_map = m[0] + ',' + m[1] + ',' + str(lvl - 1)
                mapLoc = 'd:' + new_map
                # In the event this dungeon portion does not exist for some reason
                if new_map not in self.world.dungeons:
                    self.world.BuildDungeon(new_map)
                    self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[new_map][Map.HEADER][Map.MAP_RNG], lvl - 1)
                new_point = Vec2(self.world.dungeons[new_map][Map.HEADER][Map.DOWNSTAIRS].x, self.world.dungeons[new_map][Map.HEADER][Map.DOWNSTAIRS].y)                
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
                self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[new_map][Map.HEADER][Map.MAP_RNG], lvl + 1)
            new_point = Vec2(self.world.dungeons[new_map][Map.HEADER][Map.UPSTAIRS].x, self.world.dungeons[new_map][Map.HEADER][Map.UPSTAIRS].y)            
            change_map = True

        if change_map:
            self.world.ChangeMap(mapLoc)
            self.aiEngine.player.SetSpawn(mapLoc, new_point)
    
    def SaveGame(self):
        """ Cleaning up, such as saving, on Exit """
        SaveGame(self.world, self.aiEngine)

    def LoadGame(self):
        """ Loads a specific game file """
        self.messenger.ClearScreen()
        LoadGame('Default', self.aiEngine, self.world)
        
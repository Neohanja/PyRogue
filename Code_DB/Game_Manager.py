# Manages the many aspects of the game, 
# to include a game loop

import Map
import AIManager
import tcod
from NameGen import *
from MathFun import *
from Screens import WorldUI
from Action import *
from Input_Handlers import *

WORLD_WIDTH = 256
WORLD_HEIGHT = 256

class GameManager:
    """ Game Manager """

    def __init__(self, Screen_Size : Vec2, DebugMode = False):
        """ Game Manager Constructor """
        self.width = Screen_Size.x
        self.height = Screen_Size.y

        self.world = Map.WorldMap(WORLD_HEIGHT, WORLD_WIDTH)
        self.world.BuildOverworld() # Initialize the world

        self.aiEngine = AIManager.AI_Manager(self.world)
        self.aiEngine.ToggleDebug(DebugMode)

        self.eAction = ''
    
    def Start(self):
        """ Pre-game stuff """
        pass

    def Update(self, action):
        """ Actions to take during the game loop """
        if isinstance(action, MovementAction):                    
            self.aiEngine.Update(Vec2(action.dx, action.dy))
            self.eAction = ''
            return True
        
        elif isinstance(action, UseAction):
            self.eAction = ''
            self.UseTerrain()
            return True

        elif isinstance(action, ExamineAction):
            self.eAction = self.world.GetExamineAction()
            return True
                
        elif isinstance(action, EscapeAction):
            raise SystemExit()

        return False # It shouldn't reach this point, but who knows

    def Draw(self, console):
        """ Draw updates to all game existances """
        # Draw the UI
        border = WorldUI(self.width, self.height)
        for line in range(len(border)):
                    console.print(x=0,y=line, string = border[line])
        if self.eAction != '':
                    console.print(x = 1, y = Map.WorldMap.MAP_VIEW_HEIGHT + 4, string = self.eAction)
        # Find the Upper Left corner
        max_x = self.world.width - Map.WorldMap.MAP_VIEW_WIDTH + 1
        max_y = self.world.width - Map.WorldMap.MAP_VIEW_HEIGHT + 1
        corner = Vec2(
                    Clamp(0, max_x, self.aiEngine.player.position.x - (Map.WorldMap.MAP_VIEW_WIDTH // 2)),
                    Clamp(0, max_y, self.aiEngine.player.position.y - (Map.WorldMap.MAP_VIEW_HEIGHT // 2)))

        # Draw everything else
        self.world.Draw(corner, console)
        self.aiEngine.Draw(console, corner)

    # Helper functions
    def PrintLog(self, console):
        """ Prints the player log """
        pass

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
                self.world.BuildTown(GenTownName(), loc)
            self.eAction += 'Welcome to ' + self.world.towns[loc][Map.HEADER][Map.MAP_NAME] + '.'
            new_point = Vec2(self.world.towns[loc][Map.HEADER][Map.MAP_WIDTH]//2, self.world.towns[loc][Map.HEADER][Map.MAP_HEIGHT] - 1)
            mapLoc = 't:' + loc
            change_map = True
        elif feature == "Portal":
            loc += ',1'
            mapLoc = 'd:' + loc
            if loc not in self.world.dungeons:
                # Generate and populate the dungeon
                self.world.BuildDungeon(GenTownName(), loc)
                self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[loc][Map.HEADER][Map.MAP_RNG], 1)
            self.eAction += 'You have entered ' + self.world.dungeons[loc][Map.HEADER][Map.MAP_NAME] + '.'
            new_point = Vec2(self.world.dungeons[loc][Map.HEADER][Map.UPSTAIRS].x, self.world.dungeons[loc][Map.HEADER][Map.UPSTAIRS].y)
            
            change_map = True
        elif feature == "Upstairs":
            m = self.world.mapID.split(',')
            lvl = int(m[2]) # Get the current level
            if lvl <= 1:
                self.eAction += 'You Have escaped the dungeon, ' + self.world.dungeons[self.world.mapID][Map.HEADER][Map.MAP_NAME] + '.'
                new_point = Vec2(int(m[0]), int(m[1]))
                mapLoc = 'o:'
            else:
                self.eAction += 'You have traveled up a level in the dungeon.'
                new_map = m[0] + ',' + m[1] + ',' + str(lvl - 1)
                mapLoc = 'd:' + new_map
                # In the event this dungeon portion does not exist for some reason
                if new_map not in self.world.dungeons:
                    d_name = self.world.dungeons[m[0] + ',' + m[1] + ',1'][Map.HEADER][Map.MAP_NAME]
                    self.world.BuildDungeon(d_name, new_map)
                    self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[new_map][Map.HEADER][Map.MAP_RNG], lvl - 1)
                new_point = Vec2(self.world.dungeons[new_map][Map.HEADER][Map.DOWNSTAIRS].x, self.world.dungeons[new_map][Map.HEADER][Map.DOWNSTAIRS].y)                
            change_map = True
        elif feature == "Downstairs":
            m = self.world.mapID.split(',')
            lvl = int(m[2])
            self.eAction += 'You have traveled down a level in the dungeon.'
            new_map = m[0] + ',' + m[1] + ',' + str(lvl + 1)
            mapLoc = 'd:' + new_map
            if new_map not in self.world.dungeons:
                # Create the new dungeon and populate it
                d_name = self.world.dungeons[m[0] + ',' + m[1] + ',1'][Map.HEADER][Map.MAP_NAME]
                self.world.BuildDungeon(d_name, new_map)
                self.aiEngine.PopulateMonsters(mapLoc, self.world.dungeons[new_map][Map.HEADER][Map.MAP_RNG], lvl + 1)
            new_point = Vec2(self.world.dungeons[new_map][Map.HEADER][Map.UPSTAIRS].x, self.world.dungeons[new_map][Map.HEADER][Map.UPSTAIRS].y)            
            change_map = True

        if change_map:
            self.world.ChangeMap(mapLoc)
            self.aiEngine.player.SetSpawn(mapLoc, new_point)
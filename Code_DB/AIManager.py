# Dedicated to running and playing the AI manipulations
import Monster
import Player
#import NPC

# Other imports required for functionality
import Map
import random
from MathFun import *

class AI_Manager:
    """ AI Manager class : Includes player as an Actor """
    # All Actors will be agents of the over-all class, rather than
    # making an instance of the AI Manager class. Initializing the class
    # will simply set up specific game items, such as the map and such

    Instance = None # Static class for reference
    
    def __init__(self, map_data : Map.WorldMap):
        """ Initialize the AI Manager Program """
        AI_Manager.Instance = self # Sets this as the static AI Manager Instance

        # AI figures and the map
        self.monsters = {}
        self.npcs = {}
        self.map = map_data
        
        # Always need a player
        self.player = Player.Player(map_data)
        self.player.SetSpawn('o:', self.map.GetEmptySpot('o:'))
        self.map.SetPlayer(self.player)

    def Draw(self, console, corner):
        """ Draws the individual actors on the screen"""
        self.player.Draw(console, corner)

        mapID = self.map.GetCurrentMap()

        if mapID in self.monsters:
            for m in self.monsters[mapID]:
                m.Draw(console, corner)

    def ToggleDebug(self, toggle):
        """ Turns on or off the Dev-mode debug options s"""
        self.player.debug = toggle

    def PopulateMonsters(self, d_Index : str, dRNG : random.Random, level : int):
        """ Populates a dungeon """
        m_count = dRNG.randint(3 * level, 5 * level)

        if d_Index not in self.monsters:
            self.monsters[d_Index] = []

        for m in range(m_count):
            which_monster = dRNG.choice(Monster.DUNGEON)
            new_monster = Monster.Monster(which_monster, self.map, self.player)
            spawn_loc = self.map.GetEmptySpot(d_Index)
            while self.EntityHere(spawn_loc, d_Index):
                spawn_loc = self.map.GetEmptySpot(d_Index)
            new_monster.SetSpawn(d_Index, spawn_loc)
            self.monsters[d_Index] += [new_monster]

    def PopulateNPCs(self, t_Index : str):
        """ Populates a town """
        pass

    def Update(self, playerMove : Vec2):
        """ Updates all AI Agents and Player logic """
        self.player.Update(playerMove)

        mapID = self.map.GetCurrentMap()

        if mapID in self.monsters:
            for m in self.monsters[mapID]:
                m.Update()

    def EntityHere(self, location : Vec2, mapID : str):
        """ Checks if any other entities are in this spot """
        if self.player.mapLoc == mapID and self.player.Position() == location:
            return True

        if mapID in self.monsters:
            for monster in self.monsters[mapID]:
                if monster.Position() == location:
                    return True
        if mapID in self.npcs:
            for npc in self.npcs[mapID]:
                if npc.Position() == location:
                    return True

        return False # If it gets to this point, then there is nothing here
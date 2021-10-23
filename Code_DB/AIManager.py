# Dedicated to running and playing the AI manipulations
import Monster
import Player
#import NPC

import Map
from MathFun import *

class AI_Manager:
    """ AI Manager class : Includes player as an Actor """
    # All Actors will be agents of the over-all class, rather than
    # making an instance of the AI Manager class. Initializing the class
    # will simply set up specific game items, such as the map and such
    
    def __init__(self, map_data : Map.WorldMap):
        """ Initialize the AI Manager Program """
        self.monsters = []
        self.npcs = []
        self.map = map_data
        
        self.player = Player.Player(Vec2(5, 5), "Default", '@', [255,255,255], map_data)
        self.monsters += [Monster.Monster(Vec2(15, 15), 'Monster', 'M', [255,0,0], map_data)]
        self.map.SetPlayer(self.player)

    def Draw(self, console, corner):
        """ Draws the individual actors on the screen"""
        self.player.Draw(console, corner)

        for m in self.monsters:
            m.Draw(console, corner)

    def ToggleDebug(self, toggle):
        """ Turns on or off the Dev-mode debug options s"""
        self.player.debug = toggle

    def Move(self, playerMove : Vec2):
        """ Moves all AI Agents """
        self.player.Move(playerMove)

        for m in self.monsters:
            m.Move(self.player)
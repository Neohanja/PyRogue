import Actor
from FSM import *
from MathFun import *
import random
from Map import *

MONSTER_STATS = {
    "Goblin" : ['G', 'Green'],
    "Orc" : ['O', 'Orange']
}

# Biome Spawn Disbursement
DUNGEON = ['Goblin', 'Orc']

# Indexes
M_ICON = 0
M_COLOR = 1

class Monster(Actor.Actor):
    """ Monster class, for all things trying to harm/kill the player"""
    
    def __init__(self, monster_ID : str, map_data : WorldMap, target):
        super().__init__(monster_ID, MONSTER_STATS[monster_ID][M_ICON], MONSTER_STATS[monster_ID][M_COLOR], map_data)
        """ Constructor """
        self.FSM = FSM(self.map_data, self, target)
        self.sight = 5

    def Update(self):
        """ Game Update loop for Monster Actor """
        self.FSM.Update()        
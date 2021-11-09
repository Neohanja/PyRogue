import Actor
from FSM import *
from MathFun import *
import random
from Map import *
import Stats

MONSTER_STATS = {
    "Goblin" : ['G', 'Green', 10],
    "Orc" : ['O', 'Orange', 15]
}

# Biome Spawn Disbursement
DUNGEON = ['Goblin', 'Orc']

# Indexes
M_ICON = 0
M_COLOR = 1
M_SIGHT = 2

class Monster(Actor.Actor):
    """ Monster class, for all things trying to harm/kill the player"""
    
    def __init__(self, monster_ID : str, map_data : WorldMap, target, ai_manager):
        super().__init__(monster_ID, MONSTER_STATS[monster_ID][M_ICON], MONSTER_STATS[monster_ID][M_COLOR], map_data, ai_manager)
        """ Constructor """
        self.FSM = FSM(self.map_data, self, target)
        self.sight = MONSTER_STATS[monster_ID][M_SIGHT]

    def CreateStats(self):
        """ 
            Creates the stat list for this entity
        """
        monster = MONSTER_STATS[self.name]
        self.stats['Hit Points'] = Stats.Stat('HP', 5, 5, 1, 'Vit', 2)
        self.stats['Strength'] = Stats.Stat('Str', 5, 0, 0)
        self.stats['Dexterity'] = Stats.Stat('Dex', 5, 0, 0)
        self.stats['Vitality'] = Stats.Stat('Vit', 5, 0, 0)
        self.stats['Damage'] = Stats.Stat('Dmg', 1, 0, 0, 'Str', 2)

    def Update(self):
        """ Game Update loop for Monster Actor """
        self.FSM.Update()

    def OnCollide(self, other):
        """ What happens when the actor collides with something """
        if other.actorType == 'Player':
            self.Attack(other)
        else:
            return super().OnCollide(other)
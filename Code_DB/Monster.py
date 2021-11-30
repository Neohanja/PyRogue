import Actor
from FSM import *
from MathFun import *
import random
from Map import *
import Stats


MONSTER_STATS = {
    "Goblin" : ['G', 'Green', 10, 3, 1, 15],
    "Orc" : ['O', 'Orange', 15, 5, 3, 35],
    "Overlord" : ['Y', 'Red', 25, 15, 5, 55]
}

# Biome Spawn Disbursement
DUNGEON = [['Goblin', 'ul'], ['Orc', 'l3']]
DUNGEON_BASEMENT = [['Goblin', 'ul'], ['Orc', 'l3'], ['Overlord', 'uq']]

# Spawn codes: ul = unlimited, l# = limit 3 times the level, uq = unique, only one

# Indexes
M_ICON = 0
M_COLOR = 1
M_SIGHT = 2
M_HP = 3
M_DMG = 4
M_XP = 5

class Monster(Actor.Actor):
    """ Monster class, for all things trying to harm/kill the player"""
    
    def __init__(self, monster_ID : str, map_data : WorldMap, target, ai_manager):
        super().__init__(monster_ID, MONSTER_STATS[monster_ID][M_ICON], MONSTER_STATS[monster_ID][M_COLOR], map_data, ai_manager)
        """ Constructor """
        self.FSM = FSM(self.map_data, self, target)
        self.sight = MONSTER_STATS[monster_ID][M_SIGHT]
        self.actorType = 'Monster'

    def CreateStats(self):
        """ 
            Creates the stat list for this entity
        """
        monster = MONSTER_STATS[self.name]
        self.stats['Hit Points'] = Stats.Stat('HP', monster[M_HP], monster[M_HP], 1, 'Vit', 1)
        self.stats['Experience'] = Stats.Stat('XP', monster[M_XP], stat_type = 2)
        self.stats['Strength'] = Stats.Stat('Str', 5)
        self.stats['Dexterity'] = Stats.Stat('Dex', 5)
        self.stats['Vitality'] = Stats.Stat('Vit', 5)
        self.stats['Damage'] = Stats.Stat('Dmg', monster[M_DMG], 0, 0, 'Str', 1)

    def Update(self):
        """ Game Update loop for Monster Actor """
        self.FSM.Update()

    def GetXP(self):
        return self.stats['Experience'].Total(False)

    def OnCollide(self, other):
        """ What happens when the actor collides with something """
        if other.actorType == 'Player':
            self.Attack(other)
        else:
            return super().OnCollide(other)
        
class Boss(Monster):
    def __init__(self, monster_ID: str, map_data: WorldMap, target, ai_manager):
        super().__init__(monster_ID, map_data, target, ai_manager)
        self.name += ' ' + GetCitizenName(random.randint(3, 6), random.Random())
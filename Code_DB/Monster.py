import Actor
from MathFun import *
import random
from Map import *

MONSTER_STATS = {
    "Goblin" : ['G', 'Jumbalia']
}

# Indexes
M_ICON = 0
M_COLOR = 1

class Monster(Actor.Actor):
    """ Monster class, for all things trying to harm/kill the player"""
    
    def __init__(self, monster_ID : str, map_data : WorldMap):
        super().__init__(monster_ID, MONSTER_STATS[monster_ID][M_ICON], MONSTER_STATS[monster_ID][M_COLOR], map_data)
        """ Constructor """
        self.sight = 0

    def Move(self, player : Actor.Actor):
        """ Track the player's location, and move """
        offset = self.position - player.Position()
        if abs(offset.x) <= self.sight  and abs(offset.y) <= self.sight:
            if offset.x > 0:
                super().Move(Vec2(1, 0))
            elif offset.y > 0:
                super().Move(Vec2(0, 1))
            elif offset.x < 0:
                super().Move(Vec2(-1, 0))
            elif offset.y < 0:
                super().Move(Vec2(0, -1))
            else:
                pass # Player is hit
        else:
            direction = random.randint(0, 6) # 4+ for 'resting'
            move_direction = Vec2(0, 0)
            if direction == 0 and self.position.x < WorldMap.MAP_VIEW_WIDTH:
                move_direction.x += 1
            elif direction == 1 and self.position.y < WorldMap.MAP_VIEW_HEIGHT:
                move_direction.y += 1
            elif direction == 2 and self.position.x > WorldMap.START_X:
                move_direction.x -= 1
            elif direction == 3 and self.position.y > WorldMap.START_Y:
                move_direction.y -= 1
            super().Move(move_direction)
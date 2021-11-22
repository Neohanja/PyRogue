# Baseline for NPC and NPC Functions
from Actor import Actor

class NPC(Actor):
    """ NPC Class for non-hositle characters """
    def __init__(self, identity : str, map_data, parent) -> None:
        super().__init__(identity, 'N', 'Blue', map_data, parent)        
        self.actorType = 'NPC'
        self.name = identity
        self.quest = {} # Dictionary of quests available
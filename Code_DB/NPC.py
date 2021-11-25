# Baseline for NPC and NPC Functions
from Actor import Actor

# NPC Codes
NPC_COLOR = 0
NPC_DIALOG = 1

NPC_JOBS = {
    'Villager' : ['Light Blue', 'Hello, adventurer!'],
    'Merchant' : ['Orange', 'View my wares?']
}

class NPC(Actor):
    """ NPC Class for non-hositle characters """
    def __init__(self, identity : str, job, map_data, parent) -> None:
        super().__init__(identity, '@', NPC_JOBS[job][NPC_COLOR], map_data, parent)
        self.actorType = 'NPC'
        self.job = job
        self.name = identity
        self.quest = {} # Dictionary of quests available

    
    def GetDialog(self, other):
        """ Get the dialog of the NPC """
        if self.job in NPC_JOBS:
            self.SendMessage(self.name + ' says: \"' + NPC_JOBS[self.job][NPC_DIALOG] + '\"')
        else:
            super().GetDialog(other)
# Player Class, since the player is a unique actor
from Actor import *
from Map import *

# Initial Classes (for stat distrubution)
# Class Name : Bonus stats (if/when skills get worked in, add here as well)
CLASSES = {
    '<Classes Not Implemented yet>' : [], # part of the to-do list
    'Warrior' : [['Strength', 2], ['Vitality', 2]],
    'Rogue' : [['Dexterity', 2], ['Strength', 2]]
}

# A kind of helper for the player to understand the buttons to press
# to play the game
HOTKEYS = [
    'E - Enter/Use',
    'I - Info',
    'WASD/Arrows - Movement',
    'ESC - Main Menu'
]

# XP Chart: 0 = 0 XP, because players start at level 1
LEVEL_REQ = [ 0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500, 
              6600, 7800, 9100, 10500, 12000, 13600, 15300, 17100, 19000]

class Player(Actor):
    """ Player Class """
    def __init__(self, map_data : WorldMap, ai_manager, new_name):
        super().__init__(new_name, '@', 'White', map_data, ai_manager)
        """ Constructor Specific toward Player """
        
        self.actorType = 'Player'
        self.debug = False
        self.showTooltip = True
    
    def Update(self, offset : Vec2):
        self.Move(offset)
        if 't' in self.mapLoc:
            if self.map_data.OutsideMap(self.Position()):
                self.position = self.map_data.GetTownLoc()
                self.mapLoc = 'o:'
                self.map_data.ChangeMap('o:')

    def CreateStats(self):
        """ 
            Creates the stat list for this entity; 
            Super() should always be included for child classes 
        """        
        self.stats['Level'] = Stat('Lvl', 1, 0, 2)
        self.stats['Experience'] = Stat('Exp', 0, 0, 2)
        self.stats['Hit Points'] = Stat('HP', 10, 10, 1, 'Vit', 2)
        self.stats['Strength'] = Stat('Str', 5, 0, 0)
        self.stats['Dexterity'] = Stat('Dex', 5, 0, 0)
        self.stats['Vitality'] = Stat('Vit', 5, 0, 0)
        self.stats['Damage'] = Stat('Dmg', 1, 0, 0, 'Str', 2)
    
    def OnDeath(self):
        """ What to do when the player is defeated """
        pass

    def ToggleTooltip(self):
        """ Turns on and off the tooltip (help menu) """
        self.showTooltip = not self.showTooltip
        
    def OnCollide(self, other):
        """ What happens when the actor collides with something """
        if other.actorType == 'Monster':
            self.Attack(other)
        elif other.actorType == 'NPC':
            other.GetDialog(other)
        else:
            return super().OnCollide(other)

    def GainExp(self, experience : int):
        """ Give the character XP. Assumed for now this is only in increase """
        self.stats['Experience'].LevelUp(experience, [])
        my_xp = self.stats['Experience'].Total(False)
        my_lvl = self.stats['Level'].Total(False)

        if my_lvl >= len(LEVEL_REQ):
            return # we don't need to process a level up, at max level        
        while my_xp >= LEVEL_REQ[my_lvl]: # In the event we gain a ton of XP, and it levels us a few times
            # Level up stuff
            self.stats['Level'].LevelUp(1, []) # No stats passing through, as this will be handled later
            my_lvl += 1
            self.stats['Hit Points'].LevelUp(3, []) # Temp
            self.stats['Hit Points'].AddTo(150) # until HP is higher than 150, this should always heal full
            self.stats['Damage'].LevelUp(1, []) # Temp

    def Draw(self, console, corner):
        super().Draw(console, corner) # Ensure to conform to the Actor.Draw() first

        # Player Specific functionality
        x = WorldMap.MAP_VIEW_WIDTH + 2
        console.print(x = x, y = 1, string = "Name: " + self.name)
        y = 2
        for stat in self.stats.keys():
            d = str(self.stats[stat])
            console.print(x = x, y = y, string = d)
            y += 1
        
        if self.showTooltip:
            suf = ' (F1 to Hide)'
        else:
            suf = ' (F1 to Show)'

        y += 1
        console.print(x = x, y = y, string = 'Hotkeys:' + suf)
        y += 1

        if self.showTooltip:
            for tooltips in HOTKEYS:
                y += 1
                console.print(x = x, y = y, string = tooltips)

        console.print(x = WorldMap.MAP_VIEW_WIDTH - 2, y = WorldMap.MAP_VIEW_HEIGHT + 3, string = str(self.position.ToString()))
# Player Class, since the player is a unique actor
from Actor import *
from ColorPallet import GetColor
from Map import *

# A kind of helper for the player to understand the buttons to press
# to play the game
HOTKEYS = [
    'E - Enter/Use',
    'I - Info',
    'Q - Use Potion',
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
        self.defeated_dungeons = []
    
    def Update(self, offset : Vec2):
        self.Move(offset)
        if 't' in self.mapLoc:
            if self.map_data.OutsideMap(self.Position()):
                self.position = self.map_data.GetTownLoc()
                self.mapLoc = 'o:'
                self.map_data.ChangeMap('o:')
                
    def SaveFormatter(self):
        sd = super().SaveFormatter()
        sd += '<Defeated>'
        for save_score in self.defeated_dungeons:
            sd += '$' + save_score
        sd += ';'
        return sd

    def CreateStats(self):
        """ 
            Creates the stat list for this entity; 
            Super() should always be included for child classes 
        """        
        self.stats['Level'] = Stat('Lvl', 1, 0, 2)
        self.stats['Experience'] = Stat('Exp', 0, 0, 2)
        self.stats['Gold'] = Stat('Gold', 5, 0, 2)
        self.stats['Potions'] = Stat('Potions', 2, 0, 2)
        self.stats['Hit Points'] = Stat('HP', 10, 10, 1, 'Vit', 1)
        self.stats['Strength'] = Stat('Str', 5, 0, 0)
        self.stats['Dexterity'] = Stat('Dex', 5, 0, 0)
        self.stats['Vitality'] = Stat('Vit', 5, 0, 0)
        self.stats['Damage'] = Stat('Dmg', 6, 0, 0, 'Str', 1)
    
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
            self.stats['Hit Points'].LevelUp(3, [])
            self.stats['Hit Points'].mod_val = self.stats['Hit Points'].base_val # Completely heal
            self.stats['Damage'].LevelUp(1, [])
            self.SendMessage(self.name + ' leveled up, gaining +3 hit points and +1 to damage!')
    
    def GainGold(self, coin_count):
        """ Gives the character gold. Will be used for potions """
        if not 'Gold' in self.stats:
            self.stats['Gold'] = Stat('Gold', 0, 0, 2)
        self.stats['Gold'].LevelUp(coin_count, [])
            
    def UsePotion(self):
        """ Tells the player to attempt to use a potion """
        if not 'Potions' in self.stats:
            self.stats['Potions'] = Stat('Potions', 5, 0, 2)
        
        if self.stats['Potions'].Total() <= 0:
            self.SendMessage('You are out of potions!!!')
            return False # Didn't use a potion, if it matters later on
        elif self.stats['Hit Points'].IsFull():
            self.SendMessage('You are already at full health.')
            return False
        else:
            self.SendMessage('You gain 5 hp from the potion!')
            self.stats['Hit Points'].AddTo(5)
            self.stats['Potions'].Use()
            return True

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
        
        portal_st = str(len(self.defeated_dungeons)) + ' / ' + str(len(self.defeated_dungeons) + len(self.map_data.overworld[0][6]))
        y += 1
        console.print(x = x, y = y, string = 'Portals Defeated (0): ', fg = GetColor('Portal'))
        y += 1
        console.print(x = x, y = y, string = portal_st, fg = GetColor('Portal'))
        y += 2
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
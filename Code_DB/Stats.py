# Stat system for Actors

class Stat:
    """ Individual stat """
    def __init__(self, short_name, base_val, mod_val, stat_type : int):
        self.sName = short_name
        self.base_val = base_val
        self.mod_val = mod_val
        self.stat_type = stat_type
    
    def IsEmpty(self):
        """ Returns if the value is empty (aka: Dead)"""
        if self.mod_val <= 0:
            return True
        else:
            return False
    
    def PercentRemaining(self):
        """ Returns the ratio of mod value to base value (ie, health, mana, rage) """
        return int((self.mod_val / self.base_val) * 100)
    
    def Total(self, include_mods = True):
        """ Returns the total for a skill/stat/etc. """
        if include_mods:
            return self.base_val + self.mod_val
        else:
            return self.base_val

    def AddTo(self, increase : int):
        """ Heals or adds to a stat : -increase for damage"""
        self.mod_val += increase
        if self.stat_type == 1 and self.mod_val > self.base_val:
            self.mod_val = self.base_val

    
    def __repr__(self):
        if self.stat_type == 0: # Basic stats, such as Strength
            return self.sName + ": " + str(self.base_val) + "+" + str(self.mod_val) + " total:" + str(self.Total())
        elif self.stat_type == 1: # Derived, such as HP
            return self.sName + ": " + str(self.mod_val) + "/" + str(self.base_val) + " (" + str(self.PercentRemaining()) + "%)"
        
        # Default:
        return self.sName + ": " + str(self.Total())
# Stat system for Actors

class Stat:
    """ Individual stat """
    def __init__(self, short_name = 'Blank', base_val = 0, mod_val = 0, stat_type = 0, derived_stat = '', derived_mod = 0):
        """ 
            Base Stats: Short name, base value, modified value, stat type

            For stat type : 
                0 = Regular (base + mod)
                1 = Derived stat (mod out of base, or mod/base)
                2 = just base (mod not used)
        """
        self.sName = short_name
        self.base_val = base_val
        self.mod_val = mod_val
        self.stat_type = stat_type
        self.derived_stat = derived_stat # stat this relies on
        self.derived_mod = derived_mod # how much gain from the derived stat this stat receives

    def CopyStats(self, other):
        """ Copies the stats of another stat """
        self.sName = other.sName
        self.base_val = other.base_val
        self.mod_val = other.mod_val
        self.stat_type = other.stat_type
        self.derived_stat = other.derived_stat
        self.derived_mod = other.derived_mod
    
    def IsEmpty(self):
        """ Returns if the value is empty (aka: Dead)"""
        if self.stat_type == 0 and self.mod_val <= 0:
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

    def LevelUp(self, increase : int, stat_list : list):
        """ Increase the base value, in the event of leveling up or such """
        # Uses recursion to increase the stats, this will loop through
        # each stat and check if it's increase (or decrease, if increase is
        # negative) effects the stats in the list.
        pass_list = []
        while len(stat_list) > 0:
            stat = stat_list.pop(0) # get the first stat in a list
            if stat.sName == self.sName:
                # Ignore if the stat was also pass through the mod list, we are already modding it
                continue
            if stat.derived_stat == self.sName: # if this is a stat we can mod, mod it
                # An example of recursion, where this will take anything that hasn't been checked
                # yet (stat_list) and everything that has been checked, but not modded (pass_list)
                # and check them for this stat. For all purposes, most of the stats should
                # only have a single derivative, but more complex systems may have stats that
                # derived from a derived stat. An example is that Vitality effects Health 
                # (1 Vit = 2 HP), and Strength - for now - effects damage (1 Str = 2 Dmg).
                # When skills are introduced, this will have a larger effect, as Coup De Grace
                # May scale with damage, which scales with Strength.
                stat.LevelUp(stat.derived_mod * increase, pass_list + stat_list)
            else: # if we skipped it, add it to the next list
                pass_list += [stat]
        self.base_val += increase
    
    def __repr__(self):
        if self.stat_type == 0: # Basic stats, such as Strength
            return self.sName + ": " + str(self.base_val) + "+" + str(self.mod_val) + " total:" + str(self.Total())
        elif self.stat_type == 1: # Derived, such as HP
            return self.sName + ": " + str(self.mod_val) + "/" + str(self.base_val) + " (" + str(self.PercentRemaining()) + "%)"
        
        # Default:
        return self.sName + ": " + str(self.Total())
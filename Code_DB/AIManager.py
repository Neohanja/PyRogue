# Dedicated to running and playing the AI manipulations
import Monster
import Player
import NPC

# Other imports required for functionality
import Map
import random
from NameGen import *
from MathFun import *
from Stats import Stat

class AI_Manager:
    """ AI Manager class : Includes player as an Actor """
    # All Actors will be agents of the over-all class, rather than
    # making an instance of the AI Manager class. Initializing the class
    # will simply set up specific game items, such as the map and such

    Instance = None # Static class for reference
    
    def __init__(self, map_data : Map.WorldMap, game_master, player_name = 'Default'):
        """ Initialize the AI Manager Program """
        AI_Manager.Instance = self # Sets this as the static AI Manager Instance

        # AI figures and the map
        self.monsters = {}
        self.npcs = {}
        self.map = map_data
        self.gm = game_master
        
        # Always need a player
        self.player = Player.Player(map_data, self, player_name)
        # This is done in the map gen now, when the player is set to the map
        # self.player.SetSpawn('o:', self.map.GetEmptySpot('o:'))
        self.map.SetPlayer(self.player, self)

    def SaveActors(self):
        """ Saves all actors to a file """
        asd = []
        asd += ['<PLAYER>;' + self.player.SaveFormatter() + '\n']
        for mapID in self.monsters.keys():
            for monster in self.monsters[mapID]:
                asd += ['<MONSTER>;' + monster.SaveFormatter() + '\n']
        for mapID in self.npcs.keys():
            for npc in self.npcs[mapID]:
                asd += ['<NPC>;' + npc.SaveFormatter() + '\n']
        return asd

    def LoadActors(self, actor_list : list):
        """ Loads the actors from a file """
        new_map_load = 'o:' # default
        self.monsters.clear()
        self.npcs.clear()
        for actor in actor_list:
            actor_data = actor.split(';')
            aName = actor_data[1]
            aMap = actor_data[2]
            aLoc = actor_data[3].split(',')
            aPos = Vec2(int(aLoc[0]), int(aLoc[1]))
            dList = []
            # Load stats
            if len(actor_data) > 4:
                stat_list = {}
                for stat in actor_data[4:]:
                    s_data = stat.split(',')
                    if s_data[0] == '<STAT>':
                        stat_list[s_data[1]] = Stat(s_data[2], int(s_data[3]), int(s_data[4]), int(s_data[5]))
                    elif '$' in stat:
                        dung = stat.split('$')
                        for dung_defeat in dung[1:]:
                            dList += [dung_defeat]
                        
            # Not too complex, now to figure out which actor to add. Replace player, add monster/NPC        
            if actor_data[0] == '<PLAYER>':
                self.player.SetSpawn(aMap, aPos)
                self.player.name = aName
                self.player.LoadStats(stat_list)
                new_map_load = aMap
                self.player.defeated_dungeons = dList
            elif actor_data[0] == '<MONSTER>':
                if ' ' in aName:
                    mName = aName.split(' ')
                    monster = Monster.Boss(mName[0], self.map, self.player, self, mName[1])
                else:
                    monster = Monster.Monster(aName, self.map, self.player, self)
                monster.SetSpawn(aMap, aPos)
                monster.LoadStats(stat_list)
                if aMap in self.monsters:
                    self.monsters[aMap] += [monster]
                else:
                    self.monsters[aMap] = [monster]
            elif actor_data[0] == '<NPC>':
                pass # Awaiting NPC integration
        self.map.ChangeMap(new_map_load)


    def Draw(self, console, corner):
        """ Draws the individual actors on the screen"""
        self.player.Draw(console, corner)

        mapID = self.map.GetCurrentMap()

        if mapID in self.monsters:
            for m in self.monsters[mapID]:
                m.Draw(console, corner)
        if mapID in self.npcs:
            for npc in self.npcs[mapID]:
                npc.Draw(console, corner)

    def ToggleDebug(self, toggle):
        """ Turns on or off the Dev-mode debug options s"""
        self.player.debug = toggle

    def AddLog(self, message : str):
        """ Added a send message to log function here for ease of access """
        self.gm.AddLog(message)

    def PopulateMonsters(self, d_Index : str, dungeon_header : list, level : int):
        """ Populates a dungeon """
        dRNG = dungeon_header[3]

        m_count = dRNG.randint(3 * level, 5 * level)

        if d_Index not in self.monsters:
            self.monsters[d_Index] = []

        master_list = []
        monster_choices = {}
        must_include = []
        spawn_list = []

        if isinstance(dungeon_header[6], str) and dungeon_header[6] == 'Last Floor':
            master_list = Monster.DUNGEON_BASEMENT
        else:
            master_list = Monster.DUNGEON

        for m_choice in master_list:
            # Unlimited, or 'ul'
            if m_choice[1] == 'ul':
                monster_choices[m_choice[0]] = m_count
                spawn_list += [m_choice[0]]
            # since 'ul' is currently the only other one containing l, we can safely put this here.
            # l = Level * number for max able to be spawned
            elif 'l' in m_choice[1]:
                # remove the l to get the number, mutliply by the level
                count = int(m_choice[1][1:]) * level
                # max number that can be spawned in this location
                monster_choices[m_choice[0]] = count
                spawn_list += [m_choice[0]]
            # s = static number of max able to be spawned, does not use level to multiply
            elif 's' in m_choice[1]:
                # remove the s to get the number of max able to be spawned in this level.
                count = int(m_choice[1][1:])
                monster_choices[m_choice[0]] = count
                spawn_list += [m_choice[0]]
            # uq = unique monster. Unique monsters mean, at the moment, that if this is in the spawn pool,
            # at least one must be spawned into the level as well. We add it to the different list.
            # At the moment, this is the dungeon boss.
            elif m_choice[1] == 'uq':
                must_include = [m_choice[0]]

        for m in range(m_count):
            new_monster = None
            # Go through manditory monsters first
            if len(must_include) > 0:
                new_monster = Monster.Boss(must_include.pop(0), self.map, self.player, self)
            # Then all others
            else:
                which_monster = dRNG.choice(spawn_list)
                # ensure we spawn only up to the max possible
                monster_choices[which_monster] -= 1
                # should never go below 0, but just in case, using <= is good practice
                if monster_choices[which_monster] <= 0:
                    # remove this monster from the possible spawns if we reach the max count.
                    spawn_list.remove(which_monster)
                # Create the monster, then place it into the world    
                new_monster = Monster.Monster(which_monster, self.map, self.player, self)
            
            if new_monster == None:
                break # If we ran out of monsters, end the loop.
            
            spawn_loc = self.map.GetEmptySpot(d_Index)
            while self.EntityHere(spawn_loc, d_Index):
                spawn_loc = self.map.GetEmptySpot(d_Index)
            new_monster.SetSpawn(d_Index, spawn_loc)
            self.monsters[d_Index] += [new_monster]

    def PopulateNPCs(self, t_Index : str, town_header):
        """ Populates a town """
        # 3 = Map RNG
        tRNG = town_header[3] # random.Random('temp seed for testing')
        buildings = town_header[4]
        citizens = tRNG.randint(len(buildings) // 3, len(buildings) // 3 * 2)
        
        if t_Index not in self.npcs:
            self.npcs[t_Index] = []
        
        npc_jobs = [job for job in NPC.NPC_JOBS.keys()]
        
        for c in range(citizens):
            cName = GetCitizenName(tRNG.randint(5, 10), tRNG).title()
            new_npc = NPC.NPC(cName, tRNG.choice(npc_jobs), self.map, self)
            spawn_loc = tRNG.choice(buildings)
            while self.EntityHere(spawn_loc, t_Index):
                spawn_loc = tRNG.choice(buildings)
            new_npc.SetSpawn(t_Index, spawn_loc)
            self.npcs[t_Index] += [new_npc]

    def CheckCollision(self, actor_a, offset):
        """ Checks if an actor (A) is trying to enter the space of another actor. If so, return it """
        loc = actor_a.Position() + offset
        if actor_a is not self.player:
            if loc == self.player.position:
                return self.player
        
        mapID = self.player.mapLoc
        if mapID in self.monsters:
            for monster in self.monsters[mapID]:
                if actor_a is monster:
                    continue
                elif loc == monster.position:
                    return monster
        if mapID in self.npcs:
            for npc in self.npcs[mapID]:
                if actor_a is npc:
                    continue
                elif loc == npc.position:
                    return npc

        return None # Return nothing if we hit nothing 

    def Update(self, playerMove : Vec2):
        """ Updates all AI Agents and Player logic """
        self.player.Update(playerMove)

        mapID = self.map.GetCurrentMap()
        if mapID in self.monsters:
            for m in self.monsters[mapID]:
                m.Update()
        if mapID in self.npcs:
            for npc in self.npcs[mapID]:
                npc.Update(Vec2(0, 0))
    
    def Defeated(self, attacker, defender):
        """ Handles an actor being defeated by another actor """
        self.AddLog(attacker.name + ' has defeated ' + defender.name + '!')
        
        if defender.actorType == 'Player':
            # place player has been defeated stuff here
            pass
        elif defender.actorType == 'Monster' and attacker.actorType == 'Player':
            xp = defender.GetXP()
            gold = defender.GetGold()
            attacker.GainExp(xp)
            attacker.GainGold(gold)
            self.AddLog(attacker.name + ' gains ' + str(xp) + ' experience and ' + str(gold) + ' gold.')
            mapID = self.map.GetCurrentMap()
            if mapID in self.monsters:
                self.monsters[mapID].remove(defender)
            if isinstance(defender, Monster.Boss):
                self.AddLog('Dungeon ' + self.map.dungeons[self.map.mapID][0][0] + ' has been destroyed!')
                self.map.ClosePortal(self)                

    def EntityHere(self, location : Vec2, mapID : str):
        """ Checks if any other entities are in this spot """
        if self.player.mapLoc == mapID and self.player.Position() == location:
            return True

        if mapID in self.monsters:
            for monster in self.monsters[mapID]:
                if monster.Position() == location:
                    return True
        if mapID in self.npcs:
            for npc in self.npcs[mapID]:
                if npc.Position() == location:
                    return True
        return False # If it gets to this point, then there is nothing here
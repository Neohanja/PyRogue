# A group of functions designed to help build a town
from AStar import AStar
from MathFun import *
from NameGen import *
import random

# Minimum distance for buildings to be apart from each other
BUILDING_MIN_DISTANCE = 5
T_NAME = 0
T_WIDTH = 1
T_HEIGHT = 2
T_RNG = 3
T_LEVEL = 4
T_UP = 5
T_DOWN = 6

# Overworld header data
HEADER = 0
MAP_NAME = 0
MAP_WIDTH = 1
MAP_HEIGHT = 2
MAP_RNG = 3
WORLD_SEED = 4
OVER_TOWNS = 5
MAP_ASTAR = 7

def PlaceTowns(overworld : list):
    """ Places towns on the overmap """
    mapper = overworld[HEADER][MAP_ASTAR]
    oRNG = overworld[HEADER][MAP_RNG]
    town_count = oRNG.randint(3, 10) # For now, define between 3 to 10 starting towns
    seed = overworld[HEADER][WORLD_SEED]
        
    width = overworld[HEADER][MAP_WIDTH]
    height = overworld[HEADER][MAP_HEIGHT]
        
    # Find the center town first
    tLoc = Vec2(width // 2, height // 2)
    tSpiral = Spiral(tLoc)
    while overworld[tSpiral.GetLoc().y + 1][tSpiral.GetLoc().x] != 'Grass':# self.SpaceBlocked(tSpiral.GetLoc()):
            # If the center is not available, spiral around it until a space is open. The start
            # town should be as close the center as possible.
            tSpiral.Step()
    tLoc = tSpiral.GetLoc()
    # Add town to map
    overworld[HEADER][OVER_TOWNS][str(tLoc)] = GenTownName(seed + str(tLoc))
    first = str(tLoc) # Get the address for the first town, or "start town"
    overworld[tLoc.y + 1][tLoc.x] = 'Town'
    
    towns = 0
    tries = 0
    # We set a max amount of tries, in the event the computer is unable to find a suitable place
    # to build a town. This prevents the player waiting too long for a game to start, as well as
    # ensuring we don't run into a possible infinite loop.
    while towns < town_count and tries < 1000:
        x = oRNG.randint(1, width - 2) # no towns on the very edge of the map
        y = oRNG.randint(1, height - 2) # no towns on the very edge of the map
        if overworld[y + 1][x] == 'Grass': # For now, we only want towns on Grass Tiles
            ntLoc = Vec2(x, y)
            path = mapper.FindPath(ntLoc, tLoc, False)
            if path != []: # If we can build a path to the new town (ntLoc)
                # Since we came this far, we can build the town!
                overworld[HEADER][OVER_TOWNS][str(ntLoc)] = GenTownName(seed + str(ntLoc))
                overworld[ntLoc.y + 1][ntLoc.x] = 'Town'
                towns += 1
                tLoc = ntLoc
            tries += 1 # increase the amount of times we tried to place a town, regardless of the outcome.
    return first

def TownGenerator(town_header : list):
    """ Generates a town with specified dimentions"""
    height = town_header[T_HEIGHT]
    width = town_header[T_WIDTH]
    tRNG = town_header[T_RNG]
    town_design = [] # The layout

    for y in range(height):
        new_row = []
        for x in range(width):
            new_row += ['Grass'] # Grass, the default tile.
        town_design += [new_row]

    # Will have to mess with this later so buildings aren't too sparse
    room_count = tRNG.randint(10, 20)
    tries = 0
    rooms = 0
    # Start initial building list: Add the center to ensure nothing is built in
    # the town center.
    cX = width // 2
    cY = height // 2 
    pending_rooms = [Room(Vec2(cX - 3, cY - 3), Vec2(cX + 3, cY + 3))] # Town Center

    while rooms < room_count and tries < 1000:
        sizeX = tRNG.randint(5, 10)
        sizeY = tRNG.randint(5, 10)
        startX = tRNG.randint(3, width - sizeX - 4)
        startY = tRNG.randint(3, height - sizeY - 4)
        test_room = Room(Vec2(startX, startY), Vec2(startX + sizeX, startY + sizeY))

        keep_room = True
        # Make sure rooms are overlapping other rooms, including town center
        for check_room in pending_rooms:
            if test_room.WithinBounds(check_room, BUILDING_MIN_DISTANCE):
                keep_room = False
        # If this building isn't too close to anything else, add it to the list
        if keep_room:
            pending_rooms += [test_room]
            rooms += 1
            # Add a proper door
            door_wall = tRNG.randint(0,3)
            dX = test_room.start.x
            dY = test_room.start.y
            if door_wall % 2 == 0:
                dX = tRNG.randint(test_room.start.x + 1, test_room.end.x - 1)
                if door_wall > 1:
                    dY = test_room.end.y
            else:
                dY = tRNG.randint(test_room.start.y + 1, test_room.end.y - 1)
                if door_wall > 1:
                    dX = test_room.end.x

            test_room.door = Vec2(dX, dY)

        tries += 1

    # Remove the 'town square'
    pending_rooms.pop(0)
    # Get the list of room centers for spawning and stuff
    t_spawn = [room.center for room in pending_rooms]
    p_spawn = tRNG.randint(0, len(t_spawn) - 1)
    # Build the town header proper
    town_header.append(t_spawn) # Empty dictionary for building centers
    town_header.append(t_spawn.pop(p_spawn)) # Spawn Point
    town_header.append(Vec2(cX, height - 1)) # Above is a work in progress, should only happen the first spawn

    # Build the rooms to the grid
    for build_room in pending_rooms:
        for y in range(build_room.start.y, build_room.end.y + 1):
            for x in range(build_room.start.x, build_room.end.x + 1):
                if Vec2(x, y) == build_room.door:
                    town_design[y][x] = 'Door'
                elif y == build_room.start.y or y == build_room.end.y \
                    or x == build_room.start.x or x == build_room.end.x:
                    town_design[y][x] = 'Wall'
                else:
                    town_design[y][x] = 'Room Floor'

    # Start the path making thing
    path_maker = AStar(town_design)
    town_header.append(path_maker)

    for make_path in pending_rooms:
        next_path = path_maker.FindPath(make_path.center, Vec2(cX, cY), True)
        for add_path in next_path:
            if town_design[add_path.y][add_path.x] == 'Grass':
                town_design[add_path.y][add_path.x] = 'Road'    
    return town_design
# A group of functions designed to help build a Dungeon
from AStar import AStar
from MathFun import *

# Minimum distance for buildings to be apart from each other
# 0 means they can be touching, negative means they can overlap
# -1 for shared walls, for example
BUILDING_MIN_DISTANCE = 5

D_NAME = 0
D_WIDTH = 1
D_HEIGHT = 2
D_RNG = 3
D_LEVEL = 4
D_UP = 5
D_DOWN = 6

# Most of this will be the same (for now) as the town generator, but with some changes to give more depth
def DungeonGenerator(dungeon_header : list):
    """ Generates a town with specified dimentions"""
    dungeon = []
    width = dungeon_header[D_WIDTH]
    height = dungeon_header[D_HEIGHT]
    level = dungeon_header[D_LEVEL]
    dRNG = dungeon_header[D_RNG]

    # Used to determine the bottom of the dungeon. With this math,
    # the absolute max depth will be 18 - May change later for an added challenge
    # I also want there to be a chance for 1-level dungeons, so not starting at 100%
    is_bottom = dRNG.random() > 0.95 - (0.05 * level)

    for y in range(height):
        new_row = []
        for x in range(width):
            new_row += ['Grass'] # Default to grass, but will change to a void. this is because void is not walkable and will block A*
        dungeon += [new_row]

    # Will have to mess with this later so rooms aren't too sparse
    room_max = dRNG.randint(3 + level, level * 5)
    tries = 0

    # Start the list of rooms
    pending_rooms = []

    # We want to keep the number of tries within a limit, to ensure the generator doesn't keep
    # trying if the dungeon is small, and the room count is large. Setting a max limit to the
    # number of tries helps keep the possibility of an infinite loop under control.
    while len(pending_rooms) < room_max and tries < 1000:
        sizeX = dRNG.randint(5, 10)
        sizeY = dRNG.randint(5, 10)
        startX = dRNG.randint(3, width - sizeX - 4)
        startY = dRNG.randint(3, height - sizeY - 4)
        test_room = Room(Vec2(startX, startY), Vec2(startX + sizeX, startY + sizeY))

        keep_room = True
        # Make sure rooms are overlapping other rooms, including town center
        for check_room in pending_rooms:
            if test_room.WithinBounds(check_room, BUILDING_MIN_DISTANCE):
                keep_room = False
        # If this building isn't too close to anything else, add it to the list
        if keep_room:
            pending_rooms += [test_room]
            # Add a proper door
            door_wall = dRNG.randint(0,3)
            dX = test_room.start.x
            dY = test_room.start.y
            if door_wall % 2 == 0:
                dX = dRNG.randint(test_room.start.x + 1, test_room.end.x - 1)
                if door_wall > 1:
                    dY = test_room.end.y
            else:
                dY = dRNG.randint(test_room.start.y + 1, test_room.end.y - 1)
                if door_wall > 1:
                    dX = test_room.end.x

            test_room.door = Vec2(dX, dY)

        tries += 1
    
    # Build the rooms to the grid
    for build_room in pending_rooms:
        for y in range(build_room.start.y, build_room.end.y + 1):
            for x in range(build_room.start.x, build_room.end.x + 1):
                if Vec2(x, y) == build_room.door:
                    dungeon[y][x] = 'Door'
                elif y == build_room.start.y or y == build_room.end.y \
                    or x == build_room.start.x or x == build_room.end.x:
                    dungeon[y][x] = 'Wall'
                else:
                    dungeon[y][x] = 'Room Floor'

    # Add the up and down stairs
    up_stairs = dRNG.choice(pending_rooms).center
    down_stairs = dRNG.choice(pending_rooms).center

    # make sure the up and down stairs are in the same place
    while up_stairs == down_stairs:
        down_stairs = dRNG.choice(pending_rooms).center
    
    # Add the stairs to the header information
    dungeon_header.append(up_stairs)
    dungeon_header.append(down_stairs)
    
    # And to the map
    dungeon[up_stairs.y][up_stairs.x] = 'Upstairs'

    # Do not place stairs if we are at the bottom of the portal/dungeon
    if not is_bottom: 
        dungeon[down_stairs.y][down_stairs.x] = 'Downstairs'
    # But we do need a way to tell the dungeon it is the bottom
    else:
        dungeon_header[D_DOWN] = 'Last Floor'

    # Start the path making thing
    path_maker = AStar(dungeon)

    # Add the A* program to the dungeon header, to ensure there is no real need to rebuild it later
    dungeon_header.append(path_maker)

    for room_num in range(len(pending_rooms)):
        next_room = room_num + 1
        if next_room == len(pending_rooms):
            next_room = 0
        hallway = path_maker.FindPath(pending_rooms[room_num].door, pending_rooms[next_room].door, True)
        for add_path in hallway:
            if dungeon[add_path.y][add_path.x] == 'Grass':
                dungeon[add_path.y][add_path.x] = 'Room Floor'

    # Fill in the void with walls where needed
    for row in range(height):
        for col in range(width):
            if dungeon[row][col] == 'Grass':
                if CheckSurroundingFor(dungeon, Vec2(col, row), Vec2(width, height), ['Door', 'Room Floor']):
                    dungeon[row][col] = 'Wall'
                else:
                    dungeon[row][col] = 'Void'
    
    return [dungeon_header] + dungeon

def CheckSurroundingFor(search_array, loc : Vec2, upper_bounds : Vec2, inquiry):
    """ Searches the surrounding spots for a specific tile : Inquiry should be a list """
    for y in range (-1, 2):
        for x in range (-1, 2):
            if 0 <= loc.x + x < upper_bounds.x and 0 <= loc.y + y < upper_bounds.y:
                if search_array[loc.y + y][loc.x + x] in inquiry:
                    return True
    return False
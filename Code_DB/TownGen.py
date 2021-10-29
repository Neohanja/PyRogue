# A group of functions designed to help build a town
from AStar import AStar
from MathFun import *
import random

# Minimum distance for buildings to be apart from each other
BUILDING_MIN_DISTANCE = 5

def TownGenerator(height, width):
    """ Generates a town with specified dimentions"""
    town_design = []

    for y in range(height):
        new_row = []
        for x in range(width):
            new_row += ['Grass'] # Grass, temporarily.
        town_design += [new_row]

    # Will have to mess with this later so buildings aren't too sparse
    room_count = random.randint(10, 20)
    tries = 0
    rooms = 0
    # Start initial building list: Add the center to ensure nothing is built in
    # the town center.
    cX = width // 2
    cY = height // 2 
    pending_rooms = [Room(Vec2(cX - 3, cY - 3), Vec2(cX + 3, cY + 3))]

    while rooms < room_count and tries < 1000:
        sizeX = random.randint(5, 10)
        sizeY = random.randint(5, 10)
        startX = random.randint(3, width - sizeX - 4)
        startY = random.randint(3, height - sizeY - 4)
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
            door_wall = random.randint(0,3)
            dX = test_room.start.x
            dY = test_room.start.y
            if door_wall % 2 == 0:
                dX = random.randint(test_room.start.x + 1, test_room.end.x - 1)
                if door_wall > 1:
                    dY = test_room.end.y
            else:
                dY = random.randint(test_room.start.y + 1, test_room.end.y - 1)
                if door_wall > 1:
                    dX = test_room.end.x

            test_room.door = Vec2(dX, dY)

        tries += 1
    
    # Remove the 'town square'
    pending_rooms.pop(0)

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

    for make_path in pending_rooms:
        next_path = path_maker.FindPath(make_path.center, Vec2(cX, cY), True)
        for add_path in next_path:
            if town_design[add_path.y][add_path.x] == 'Grass':
                town_design[add_path.y][add_path.x] = 'Road'
    
    return town_design
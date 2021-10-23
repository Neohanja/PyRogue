# A group of functions designed to help build a town
from MathFun import *
import random


def TownGenerator(height, width):
    """ Generates a town with specified dimentions"""
    town_design = []

    for y in range(height):
        new_row = []
        for x in range(width):
            new_row += ['Grass'] # Dirt, temporarily
        town_design += [new_row]
    
    room_count = random.randint(5,10)
    tries = 0
    rooms = 0
    pending_rooms = []

    while rooms < room_count and tries < 1000:
        sizeX = random.randint(5, 10)
        sizeY = random.randint(5, 10)
        startX = random.randint(3, width - sizeX - 4)
        startY = random.randint(3, height - sizeY - 4)
        test_room = Room(Vec2(startX, startY), Vec2(startX + sizeX, startY + sizeY))

        keep_room = True
        if len(pending_rooms) > 0:
            for check_room in pending_rooms:
                if test_room.WithinBounds(check_room):
                    keep_room = False
        if keep_room:
            pending_rooms += [test_room]
            rooms += 1
        tries += 1

    for build_room in pending_rooms:
        for y in range(build_room.start.y, build_room.end.y + 1):
            for x in range(build_room.start.x, build_room.end.x + 1):
                if y == build_room.start.y or y == build_room.end.y \
                    or x == build_room.start.x or x == build_room.end.x:
                    town_design[y][x] = 'Wall'
                else:
                    town_design[y][x] = 'Dirt'
    
    return town_design


class Room:
    """ Determines a room (or building) based on parameters """
    def __init__(self, start : Vec2, end : Vec2):
        """ Constructor """
        self.start = start
        self.end = end
    
    def WithinBounds(self, other):
        """ Checks if 2 boundaries intersect """
        self_center = Vec2(
            (self.end.x - self.start.x) // 2 + self.start.x,
            (self.end.y - self.start.y) // 2 + self.start.y)
        other_center = Vec2(
            (other.end.x - other.start.x) // 2 + other.start.x,
            (other.end.y - other.start.y) // 2 + other.start.y)
        
        return self.PointWithinBounds(other.start.x, other.start.y) or \
            self.PointWithinBounds(other.start.x, other.end.y) or \
            self.PointWithinBounds(other.end.x, other.start.y) or \
            self.PointWithinBounds(other.end.x, other.end.y) or \
            self.PointWithinBounds(other_center.x, other_center.y) or \
            other.PointWithinBounds(self.start.x, self.start.y) or \
            other.PointWithinBounds(self.start.x, self.end.y) or \
            other.PointWithinBounds(self.end.x, self.start.y) or \
            other.PointWithinBounds(self.end.x, self.end.y) or \
            other.PointWithinBounds(self_center.x, self_center.y)

    def PointWithinBounds(self, x, y):
        """ Checks if a point is within the bounds """
        return self.start.x <= x <= self.end.x and self.start.y <= y <= self.end.y
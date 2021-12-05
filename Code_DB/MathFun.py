# Math Function needed to do many of the game system functionality
# Classes:
# - Vector 2: A point on the Cortesian plane (R x R), or (x, y) coordinates
# - Room: All the functionality of a rectangle, with an exit point (door) and
#   functions to determine where the inside of the room is and its edges

from numpy import sqrt # Needed to find a point on a circle

# Vector 2 (x, y) for location information
class Vec2:
    """ A Vector 2 class with math funcitons as needed """
    def __init__(self, x : int, y : int):
        """ Constructor """
        self.x = x
        self.y = y
    
    def Move(self, dx, dy):
        """ Moves the Vector2 by +/- x and +/- y """
        self.x += dx
        self.y += dy
    
    def Dot(self, other):
        """ Returns the Dot Matrix value of this and another Vector2"""
        return self.x * other.x + self.y * other.y

    def __repr__(self):
        """ String representation of the Vector 2"""
        return str(self.x) + ',' + str(self.y)

    def ToString(self):
        """ A proper string variation, much like __repr__ """
        return 'x: ' + str(self.x) + ' y: ' + str(self.y)

    # Override the + operator for 2 Vector 2s
    def __add__(self, other):
        """ Adds 2 Vector2 together """
        return Vec2(self.x + other.x, self.y + other.y)

    def Copy(self):
        """ Returns a copy of this Vector 2, rather than a reference"""
        return Vec2(self.x, self.y)
    
    def Distance(self, other):
        """ calculates the distance between this and another Vector 2 """
        x_sqr = self.x - other.x
        x_sqr = x_sqr * x_sqr # Square the result for x_1 - x_2
        y_sqr = self.y - other.y
        y_sqr = y_sqr * y_sqr # Square the result for y_1 - y_2
        return sqrt(x_sqr + y_sqr) # Distance formula for 2 points
    
    # Override the - operator for 2 Vector 2s : Aka - The offset between 2 points
    def __sub__(self, other):
        """ Subtracts a Vector2 from this Vector2 """
        return Vec2(self.x - other.x, self.y - other.y)
    
    # Overrides the == operator, checking if 2 Vector 2s are in the same spot
    def __eq__(self, other):
        """ Checks if 2 Vector2 are at the same point """
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        else:
            return False
    
    # Overrides the * operator, for a single point value
    def __mul__(self, const):
        """ Allows multiplication of a constant value by Vector2 """
        return Vec2(self.x * const, self.y * const)

# A Boundary Box to check if things are within a specific range. Called room
# since this is a majority of the box's intents.

class Room:
    """ Determines a room (or building) based on parameters """
    def __init__(self, start : Vec2, end : Vec2):
        """ Constructor """
        self.start = start
        self.end = end
        self.center = Vec2(
            (self.end.x - self.start.x) // 2 + self.start.x,
            (self.end.y - self.start.y) // 2 + self.start.y)
        self.door = Vec2(self.center.x, self.center.y)
    
    def WithinBounds(self, other, distance):
        """ Checks if 2 boundaries intersect """
        
        return self.PointWithinBounds(other.start.x, other.start.y, distance) or \
            self.PointWithinBounds(other.start.x, other.end.y, distance) or \
            self.PointWithinBounds(other.end.x, other.start.y, distance) or \
            self.PointWithinBounds(other.end.x, other.end.y, distance) or \
            self.PointWithinBounds(other.center.x, other.center.y, distance) or \
            other.PointWithinBounds(self.start.x, self.start.y, distance) or \
            other.PointWithinBounds(self.start.x, self.end.y, distance) or \
            other.PointWithinBounds(self.end.x, self.start.y, distance) or \
            other.PointWithinBounds(self.end.x, self.end.y, distance) or \
            other.PointWithinBounds(self.center.x, self.center.y, distance)

    def PointWithinBounds(self, x, y, distance):
        """ Checks if a point is within the bounds """
        return self.start.x - distance <= x <= self.end.x + distance and \
            self.start.y - distance <= y <= self.end.y + distance

class Spiral:
    """ A class for making a spiral pattern for algorithms that need them """
    def __init__(self, initPos : Vec2):
        """ Constructor """
        self.initialPoint = initPos
        self.currentPoint = Vec2(initPos.x, initPos.y)
        self.stepDir = 0
        self.stepDist = 1
    
    def Step(self):
        """ Get the next step in the spiral """
        if self.stepDir == 0: # Go Right
            self.currentPoint.x -= 1
            if self.currentPoint.x == self.initialPoint.x - self.stepDist:
                self.stepDir = 1
        elif self.stepDir == 1: # Then Up
            self.currentPoint.y -= 1
            if self.currentPoint.y == self.initialPoint.y - self.stepDist:
                self.stepDir = 2
        elif self.stepDir == 2: # Next, Left
            self.currentPoint.x += 1
            if self.currentPoint.x == self.initialPoint.x + self.stepDist:
                self.stepDir = 3
        elif self.stepDir == 3: # Then Down
            self.currentPoint.y += 1
            if self.currentPoint.y == self.initialPoint.y + self.stepDist:
                self.stepDir = 0
                self.stepDist += 1 # If we hit this point, now we restart the spiral and increase the distance
        
    def GetLoc(self):
        return self.currentPoint
    
    def GetTID(self):
        return str(self.currentPoint)

# Additional math helper functions

def Clamp(a, b, val):
    """ Clamps a value between a and b where a < b"""
    if val < a:
        return a
    elif val > b:
        return b
    else:
        return val

def Lerp(a, b, val : float):
    """ Interpolates from a point between a and b, based on a percentage of val (0.00 to 1.00) """
    return a + val * (b - a)

def Curve(val):
    """ 6x^5 - 15x^4 + 10x^3 : Smooth Curving interpolation of points"""
    return val * val * val * (10.0 + val * (val * 6.0 - 15.0))

def PointOnCircle(x, radius = 1):
    """ Based on the radius of a circle, find where the x value falls, and return the y value """
    # r = x^2 + y^2 : Formula for a circle
    # r - x^2 = y^2
    # sqrt(r - x^2) = y
    return sqrt(radius - x * x)

def Floor(val):
    """ Returns the greatest int less than or equal to value (val) """
    t = int(val)
    if val < 0: # Since t truncates the decimal, -0.12 becomes 0. We need it to be -1, though.
        t -= 1
    return t

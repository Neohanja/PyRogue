# Math Function needed to do many of the system functionality

from numpy import sqrt # Needed to find a point on a circle

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
        return 'x: ' + str(self.x) + ' y: ' + str(self.y)

    # Override the + operator for 2 Vector 2s
    def __add__(self, other):
        """ Adds 2 Vector2 together """
        return Vec2(self.x + other.x, self.y + other.y)
    
    # Override the - operator for 2 Vector 2s : Aka - The offset between 2 points
    def __sub__(self, other):
        """ Subtracts a Vector2 from this Vector2"""
        return Vec2(self.x - other.x, self.y - other.y)
    
    # Overrides the == operator, checking if 2 Vector 2s are in the same spot
    def __eq__(self, other):
        """ Checks if 2 Vector2 are at the same point """
        return self.x == other.x and self.y == other.y
    
    # Overrides the * operator, for a single point value
    def __mul__(self, const):
        """ Allows multiplication of a constant value by Vector2 """
        return Vec2(self.x * const, self.y * const)
    
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

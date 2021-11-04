# Noise Function
# Based on Perlin Noise
# Uses dot matrices to find the angle between an offset a nd

import random
from MathFun import *

class Noise:
    """ Class of Noise """
    
    def __init__(self, sqr_size, wRNG):
        """ Constructor """
        # Step 1: Initialize the table
        # Since I am not building a random number generator,
        # I will be making a premutation table to insure the
        # same number is pulled every time a cordinate is used
        self.sqr_size = sqr_size
        self.pTable = []
        # Step 2: Populate the table
        for col in range(sqr_size):
            new_row = []                        # start a new row
            for row in range(sqr_size):
                x = wRNG.randint(0,100) / 100 # Get a random number 0.0 to 1.0
                y = PointOnCircle(x)            # Get the point on the circle for the y cord based on x
                quad = wRNG.randint(0, 3)     # determine the quadrant of the point
                if quad == 1 or quad == 2:      # Quads will rotate clockwise, starting with +x/+y
                    y *= -1
                if quad == 2 or quad == 3:
                    x *= -1
                new_row += [Vec2(x, y)]         # Add this random rotation to the table
            self.pTable += [new_row]            # Add this row to the pre-table

    def Noise2D(self, x : float, y : float):
        """ Returns the Curvature of Noise based on the (x, y) coordinate provided """
        ix = Floor(x) # The Left x value, or greatest int <= x
        iy = Floor(y) # The Lower y value, or greatest int <= y

        fx = x - ix # The fraction portion of x : ie, -1.23 = 0.23
        fy = y - iy # The fraction portion of y : ie,  3.14 = 0.14

        cx = Curve(fx) # Get the smoothed value of fx
        cy = Curve(fy) # Get the smoothed value of fy

        # Get the Dot matrices to calculate the gradient 
        # toward each corner, using the corners 'random direction'
        # and the offset from the point in a box to said corner
        x1 = self.pTable[(ix) % self.sqr_size][(iy) % self.sqr_size].Dot(Vec2(ix - x, iy - y))
        x2 = self.pTable[(ix + 1) % self.sqr_size][(iy) % self.sqr_size].Dot(Vec2(ix + 1 - x, iy - y))

        a = Lerp(x1, x2, cx) # Top of the 'box'

        x1 = self.pTable[ix % self.sqr_size][(iy + 1) % self.sqr_size].Dot(Vec2(ix - x, iy + 1 - y))
        x2 = self.pTable[(ix + 1) % self.sqr_size][(iy + 1) % self.sqr_size].Dot(Vec2(ix + 1 - x, iy + 1 - y))

        b = Lerp(x1, x2, cx) # Bottom of the 'box'

        return Lerp(a, b, cy) # Meet in the middle

    def BuildMap(self, width, height, offset : Vec2, scale : float):
        """ Builds a map for the perlin noise"""
        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                sample_x = (x + offset.x) / scale
                sample_y = (y + offset.y) / scale
                row += [self.Noise2D(sample_x, sample_y)]
            grid += [row]
        return grid
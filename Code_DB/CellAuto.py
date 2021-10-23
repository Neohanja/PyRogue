# Cellular Automata, based loosely on Conway's Game of Life Simulation
import random

def CellAuto(width, height, chance, smoothing, birth, death):
    """ Build a 2-d array based on cellular automata (ie: Conway's game of life)"""
    grid = []
    
    # Initial grid with random chance of cell being "alive" or "dead"
    for row in range(height):
        new_row = []
        for col in range(width):
            new_row += [random.randint(0,100) < chance]
        grid += [new_row]

    # Smooth the noise
    for i in range(smoothing):
        new_grid = []
        for row in range(height):
            new_row = []
            for col in range(width):
                alive = grid[row][col]
                surrounding = 0
                # Count the amount of surrounding cells alive
                for x in range(-1,2):
                    for y in range(-1,2):
                        if 0 <= col + x < width and 0 <= row + y < height:
                            if grid[row + y][col + x]:
                                surrounding += 1
                        else: # Outside the border will assume living cell
                            surrounding += 1
                # If the surrounding count is less than death (under-pop)
                if surrounding < death:
                    alive = False
                # If the surrounding count is enough to revive
                elif surrounding > birth:
                    alive = True
                new_row += [alive]
            new_grid += [new_row]
        grid = new_grid
    return grid
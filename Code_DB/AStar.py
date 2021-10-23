# An implementation for A* pathfinding,
# used for AI movement, path building for
# towns and dungeons, and making sure something
# can be accessed by the player at all times
from Map import WorldMap
import MathFun

class ANode:
    """ Individual node information for each node """

    def __init__(self, point : MathFun.Vec2, goal : MathFun.Vec2, parent_node = None):
        self.manhattan_cost = abs(point.x - goal.x) + abs(point.y - goal.y)
        self.point = point
        self.parent_node = parent_node
        self.previous_cost = 0
        if self.parent_node != None:
            self.previous_cost = self.parent_node.total_cost
        self.total_cost = self.previous_cost + self.manhattan_cost

    def __eq__(self, other):
        """ == operator overload """
        return self.point == other.point

    def __lt__(self, other):
        """ Less than < operator """
        return self.total_cost < other.total_cost
    
    def __gt__(self, other):
        """ Greater than > operator """
        return self.total_cost > other.total_cost

class AStar:

    def __init__(self, grid):
        """ Constructor """
        self.open_nodes = []
        self.closed_nodes = []
        self.level_grid = grid
        self.max_x = len(grid[0])
        self.max_y = len(grid)

    def FindPath(self, start : MathFun.Vec2, end : MathFun.Vec2, include_goal : bool):
        """ Finds an A* path from start to end. 
            Including Goal ends at the end point,
            Excluding Goal stops the spot prior to 
            the end point
        """
        # Clear the open and closed list
        self.open_nodes.clear()
        self.closed_nodes.clear()
        # Get the first point, and start from there. None means there is no "parent"
        start_node = ANode(start, end)
        self.open_nodes.append(start_node)

        while len(self.open_nodes) > 0:
            if self.open_nodes[0].point == end:
                path = []
                cur_node = self.open_nodes[0]
                if not include_goal:
                    cur_node = cur_node.parent_node
                while cur_node != None:
                    path.append(cur_node.point)
                    cur_node = cur_node.parent_node
                
            self.AddSurrounding(self.open_nodes[0], end)
            self.closed_nodes.append(self.open_nodes.pop(0))
            self.open_nodes.sort()

    def AddSurrounding(self, point : ANode, goal : MathFun.Vec2):
        """ Adds the surrounding areas to the current node """
        start = point.point
        # No diagonals, as the characters and world can only move the north/east/south/west
        for neighbor in [MathFun.Vec2(-1, 0), MathFun.Vec2(1, 0), MathFun.Vec2(0, -1), MathFun.Vec2(0, 1)]:
            if 0 <= start.x + neighbor.x < self.max_x and 0 <= start.y + neighbor.y < self.max_y:
                next_point = MathFun.Vec2(start.x + neighbor.x, start.y + neighbor.y)
                if WorldMap.map_symbols[self.grid[next_point.y][next_point.x]][2]:
                    add_node = ANode(next_point, goal, point.total_cost)
                    if not AStar.IsNodeInList(self.open_nodes, add_node) and not AStar.IsNodeInList(self.closed_nodes, add_node):
                        self.open_nodes.append(add_node)
                        self.open_nodes.sort() # sort the list, to ensure the lowest cost is at the bottom of the list

        

    def IsNodeInList(node_list, node):
        for check_node in node_list:
            if check_node == node:
                return True
        return False
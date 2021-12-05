# An implementation for A* pathfinding,
# used for AI movement, path building for
# towns and dungeons, and making sure something
# can be accessed by the player at all times
import Map
import MathFun

class ANode:
    """ Individual node information for each node """

    def __init__(self, point : MathFun.Vec2, goal : MathFun.Vec2, parent_node = None):
        # Since things cannot move diagonally, we calculate manhattan distance
        self.manhattan_cost = abs(point.x - goal.x) + abs(point.y - goal.y)
        # The (x, y) of this point
        self.point = point
        # The node prior to this one, if one exists
        self.parent_node = parent_node
        # Initialize the cost of the previous node. If none, then the cost = 0
        previous_cost = 0
        # Get parent's cost
        if isinstance(self.parent_node, ANode):
            previous_cost = self.parent_node.total_cost
        #This point's total cost will be the parent's cost plus our distance cost
        self.total_cost = previous_cost + self.manhattan_cost

    def __eq__(self, other):
        """ == operator overload """
        if isinstance(other, ANode):
            return self.point == other.point
        else:
            return False

    def GetPath(self):
        """ 
            Recursively calls the parent node to return the complete path to get to
            this node
        """
        # Base Case
        if self.parent_node == None:
            # If this is the start point, there will be no parent. Based on how A*
            # works, we also need to account that since this is the start point,
            # we should not include this point as the NPC/Path will include it and
            # it will cause the NPC to be idle for a round (or more, depending on
            # the frequency of being called).
            return []
        else:
            # Call the parent's Get Path Function
            path = self.parent_node.GetPath()
            # Make sure this point is last, as it comes after the parent.
            return path + [self.point]
    
    def __repr__(self):
        """str(ANode) representation of this point. Returns the Vector2 version."""
        return str(self.point)

    # Operations for sorting an ANode List
    def __lt__(self, other):
        """ Less than < operator """
        return self.manhattan_cost < other.manhattan_cost
    
    def __gt__(self, other):
        """ Greater than > operator """
        return self.manhattan_cost > other.manhattan_cost

# The algorith class for A* pathfinding. Stores the map for future use, to make sure it
# doesn't need to be called each time the pathfinder is used.

class AStar:
    """ 
        A Star Algorithm. Stores the map (grid) and nodes are built/rebuilt each time
        Find Path is called. Can be modified later if endless terrain is used.
    """
    def __init__(self, grid):
        """ Constructor """
        # Determines if a node is open or closed
        self.node_list = {}
        self.open_list = []
        # The map storage
        self.grid = grid
        # The max dimensions of the map
        self.max_x = len(grid[0])
        self.max_y = len(grid)

    def FindPath(self, start : MathFun.Vec2, end : MathFun.Vec2, include_goal : bool):
        """ 
            Finds an A* path from start to end. 
            Including Goal ends at the end point,
            Excluding Goal stops the spot prior to 
            the end point
        """
        # Clear the lists
        self.node_list.clear()
        self.open_list.clear()

        # Get the first point, and start from there. None means there is no "parent"
        start_node = ANode(start, end)
        self.open_list.append(start_node)

        if start == end:
            # In the event the pathfinder is at the end point already,
            # it is useless to send it to the next point
            return []
        # Process the list of open nodes, until there are no more nodes to process
        while len(self.open_list) > 0:
            if self.open_list[0].point == end:
                cur_node = self.open_list[0]
                if not include_goal: # Skip the goal if we program that. Useful for NPCs
                    cur_node = cur_node.parent_node
                return cur_node.GetPath() # call the recursion on the A* Nodes to get the path
            self.node_list[str(self.open_list[0])] = 'Closed'
            self.AddSurrounding(self.open_list.pop(0), end)
        return [] # return a blank list if nothing was found.

    def AddSurrounding(self, point : ANode, goal : MathFun.Vec2):
        """ Adds the surrounding areas to the current node """
        start = point.point.Copy()
        # No diagonals, as the characters and world can only move the north/east/south/west
        for neighbor in [MathFun.Vec2(-1, 0), MathFun.Vec2(1, 0), MathFun.Vec2(0, -1), MathFun.Vec2(0, 1)]:
            if 0 <= start.x + neighbor.x < self.max_x and 0 <= start.y + neighbor.y < self.max_y:
                next_point = MathFun.Vec2(start.x + neighbor.x, start.y + neighbor.y)
                if not Map.MAP_SYMBOLS[self.grid[next_point.y][next_point.x]][Map.SYMBOL_BLOCK_MOVEMENT]:
                    self.AddNode(ANode(next_point, goal, point))
    
    def AddNode(self, node : ANode):
        """ 
            Checks if this node is new, or already in the open/closed list 
            If it is a new node, adds it to the open list
        """
        # Ensure we have not already used this node
        if str(node) in self.node_list:
            return # Node is already being processed
        
        self.node_list[str(node)] = 'Open'
        self.open_list.append(node)
        self.open_list.sort()
# An implementation for A* pathfinding,
# used for AI movement, path building for
# towns and dungeons, and making sure something
# can be accessed by the player at all times
import Map
import MathFun

class ANode:
    """ Individual node information for each node """

    def __init__(self, point : MathFun.Vec2, goal : MathFun.Vec2, parent_node = None):
        self.manhattan_cost = abs(point.x - goal.x) + abs(point.y - goal.y)
        self.point = point
        self.parent_node = parent_node
        self.previous_cost = 0
        if isinstance(self.parent_node, ANode):
            self.previous_cost = self.parent_node.total_cost
        self.total_cost = self.previous_cost + self.manhattan_cost

    def __eq__(self, other):
        """ == operator overload """
        if isinstance(other, ANode):
            return self.point == other.point
        else:
            return False
    
    def __repr__(self):
        return str(self.point)

    def __lt__(self, other):
        """ Less than < operator """
        return self.total_cost < other.total_cost
    
    def __gt__(self, other):
        """ Greater than > operator """
        return self.total_cost > other.total_cost

class AStar:
    def __init__(self, grid):
        """ Constructor """
        self.node_status = {}
        self.open_list = []
        self.grid = grid
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
        self.node_status.clear()
        self.open_list.clear()

        # Get the first point, and start from there. None means there is no "parent"
        start_node = ANode(start, end)
        self.node_status[str(start_node)] = 'Open'
        self.open_list.append(start_node)

        if start == end:
            # In the event the pathfinder is at the end point already,
            # it is useless to send it to the next point
            include_goal = False

        while len(self.open_list) > 0:
            if self.open_list[0].point == end:
                path = []
                cur_node = self.open_list[0]
                if not include_goal:
                    cur_node = cur_node.parent_node
                while isinstance(cur_node, ANode):
                    path.append(cur_node.point)
                    cur_node = cur_node.parent_node
                return path

            self.node_status[str(self.open_list[0])] = 'Closed'    
            self.AddSurrounding(self.open_list.pop(0), end)

        return []

    def AddSurrounding(self, point : ANode, goal : MathFun.Vec2):
        """ Adds the surrounding areas to the current node """
        start = point.point
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
        if str(node) in self.node_status:
            return # Node is already being processed
        
        self.node_status[str(node)] = 'Open'
        self.open_list.append(node)
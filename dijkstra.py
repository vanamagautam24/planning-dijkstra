import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import copy

class Node:
    def __init__(self, state, parent, cost, distance):
        self.state = state              
        self.parent = parent                   
        self.cost = cost
        self.distance = distance 

    def __repr__(self):
        return str(self.state)
    
    def switch_(self, fn):
        """ Single Dispatcher for replicating a switch type operation. 
            note - There is no built-in method in python for switch.
            A decorator is created to perform switch operation
        """
        registry = dict()
        registry['default'] = fn

        def register(case):
            def inner(fn):
                registry[case] = fn
                return fn
            return inner
        
        def decorator(case):
            fn = registry.get(case, registry['default'])
            return fn()
        
        decorator.register = register
        return decorator

    def check_obstacle_space(self, potential_node):
        """ check_obstacle_space checks for obstacles. If the start node and goal node lies in the obstacle space
            then the function returns True indicating that the points fall in the obstacle space. If the coordinate points don't fall in the obstacle space False is returned.
        """
        x, y = potential_node[0], potential_node[1]
        if (x < 0) or (x > 400) or (y < 0) or (y > 250):
            return True
        if ((x - 300) ** 2 + (y - 185) ** 2 - 45 * 45) <= 0:
            return True
        elif ((0.316 * x + 178.608 - y) >= 0 and (0.857 * x + 106.429 - y) <= 0 and (-0.114 * x + 189.091 - y) <= 0) or ((-3.2 * x + 450 - y) >= 0 and (-1.232 * x + 220.348 - y) <= 0 and not (-0.114 * x + 189.091 - y) <= 0):
            return True
        elif (-0.571 * x + 174.286 - y) <= 0 and (160 - x) <= 0 and (0.571 * x + 25.714 - y) >= 0 and (-0.575 * x + 261 - y) >= 0 and (240 - x) >= 0 and (0.571 * x - 54.286 - y) <= 0:
            return True
        else:
            return False

    def common_move(self, potential_node, direction_val, direction):
        """ Common function - Contains steps which are frequently used for directions. Think of it as a utility function."""
        if not self.check_obstacle_space(potential_node):
            move_node = Node(copy.deepcopy(self.state), Node(self.state, self.parent, self.cost, self.distance), self.cost + direction_val, direction_val)
            if direction == 'up':
                move_node.state[1] = move_node.state[1] + 1
            elif direction == 'down':
                move_node.state[1] = move_node.state[1] - 1
            elif direction == 'left':
                move_node.state[0] = move_node.state[0] - 1
            elif direction == 'right':
                move_node.state[0] = move_node.state[0] + 1
            elif direction == 'up_left':
                move_node.state[0], move_node.state[1]  = move_node.state[0] - 1, move_node.state[1] + 1
            elif direction == 'up_right':
                move_node.state[0], move_node.state[1]  = move_node.state[0] + 1, move_node.state[1] + 1
            elif direction == 'down_left':
                move_node.state[0], move_node.state[1]  = move_node.state[0] - 1, move_node.state[1] - 1
            elif direction == 'down_right':
                move_node.state[0], move_node.state[1]  = move_node.state[0] - 1, move_node.state[1] - 1
            return move_node
        return None

    # direction methods
    def up(self):
        potential_node = (self.state[0], self.state[1] + 1)
        up_node = self.common_move(potential_node, 1, "up")
        return up_node

    def down(self):
        potential_node = (self.state[0], self.state[1] - 1)
        down_node = self.common_move(potential_node, 1, "down")
        return down_node

    def left(self):
        potential_node = (self.state[0] - 1, self.state[1])
        left_node = self.common_move(potential_node, 1, "left")
        return left_node

    def right(self):
        potential_node = (self.state[0] + 1, self.state[1])
        right_node = self.common_move(potential_node, 1, "right")
        return right_node
    
    def up_left(self):
        potential_node = (self.state[0] - 1, self.state[1] + 1)
        up_left = self.common_move(potential_node, 1.414, "up_left")
        return up_left
    
    def up_right(self):
        potential_node = (self.state[0] + 1, self.state[1] + 1)
        up_right = self.common_move(potential_node, 1.414, "up_right")
        return up_right

    def down_left(self):
        potential_node = (self.state[0] - 1, self.state[1] - 1)
        down_left = self.common_move(potential_node, 1.414, "down_left")
        return down_left

    def down_right(self):
        potential_node = (self.state[0] + 1, self.state[1] - 1)
        down_right = self.common_move(potential_node, 1.414, "down_right")
        return down_right

    def generate_children(self):
        """ Generates children by registering switch_ dispatcher """
        children = []
        @self.switch_
        def move():
            return "Invalid move"
        
        move.register("up")(lambda: children.append(self.up()))
        move.register("down")(lambda: children.append(self.down()))
        move.register("left")(lambda: children.append(self.left()))
        move.register("right")(lambda: children.append(self.right()))  
        move.register("up_left")(lambda: children.append(self.up_left()))       
        move.register("up_right")(lambda: children.append(self.up_right()))       
        move.register("down_left")(lambda: children.append(self.down_left()))       
        move.register("down_right")(lambda: children.append(self.down_right()))  

        if self.up():
            move("up")
        if self.down():
            move("down")
        if self.left():
            move("left")
        if self.right():
            move("right")
        if self.up_left():
            move("up_left")
        if self.up_right():
            move("up_right")
        if self.down_left():
            move("down_left")
        if self.down_right():
            move("down_right")
        
        return children
    


pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250
CYAN = (0, 255, 255)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
counter = 0
while True:
    display_surface.fill((0,0,0))
    # draw obstacles.
    pygame.draw.circle(display_surface, CYAN, (300, 65), 40)
    pygame.draw.polygon(display_surface, CYAN, [[200, 109], [234, 129], [234, 170], [200, 190], [167, 171], [165, 131]])
    pygame.draw.polygon(display_surface, CYAN, [[36, 65], [115, 40], [80, 70], [106, 150]])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


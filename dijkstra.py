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


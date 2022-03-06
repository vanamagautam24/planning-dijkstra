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


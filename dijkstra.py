import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import copy

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


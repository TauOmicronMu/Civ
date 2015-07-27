#!/usr/bin/python

import sys #must import sys before the try clause.

try:
    import time
    import random
    import math
    import os
    import getopt
    import pygame
    import pickle
    import constants as c
    from socket import *
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

'''Loads in tile images'''
cattle_tile = pygame.image.load(os.path.join("dat", "cattle_tile.png"))
city_tile = pygame.image.load(os.path.join("dat", "city_tile.png"))
fish_tile = pygame.image.load(os.path.join("dat", "fish_tile.png"))
forest_tile = pygame.image.load(os.path.join("dat", "forest_tile.png"))
gold_tile = pygame.image.load(os.path.join("dat", "gold_tile.png"))
grass_tile = pygame.image.load(os.path.join("dat", "grass_tile.png"))
hill_tile = pygame.image.load(os.path.join("dat", "hill_tile.png"))
iron_tile = pygame.image.load(os.path.join("dat", "iron_tile.png"))
marble_tile = pygame.image.load(os.path.join("dat", "marble_tile.png"))
sheep_tile = pygame.image.load(os.path.join("dat", "sheep_tile.png"))
silver_tile = pygame.image.load(os.path.join("dat", "silver_tile.png"))
stone_tile = pygame.image.load(os.path.join("dat", "stone_tile.png"))
water_tile = pygame.image.load(os.path.join("dat", "water_tile.png"))


'''Generate a grid of size c.gridx by c.gridy'''

grid = [[0 for x in range(c.gridx_dim)] for y in range(c.gridy_dim)]

pygame.init()

size = c.window_size
camera = [0, 0]
mouse_pos = tuple(v//2 for v in size)
screen = pygame.display.set_mode(size)

pygame.display.set_caption(c.window_caption)

quitflag = False

clock = pygame.time.Clock()

while not quitflag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitflag = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            column = (mouse_pos[0] + camera[0]) // c.WIDTH
            row = (mouse_pos[1] + camera[1]) // c.HEIGHT
            grid[row][column] = 0
            print("row: " + str(row) + " column: " + str(column))
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

    '''Game logic goes here'''
    if mouse_pos[0] < 100:
        camera[0] -= 4
    elif mouse_pos[0] >= c.window_size[0]-100:
        camera[0] += 4

    if mouse_pos[1] < 100:
        camera[1] -= 4
    elif mouse_pos[1] >= c.window_size[1]-100:
        camera[1] += 4

    camera[0] = max(0, min(c.WIDTH*c.gridx_dim - c.window_size[0], camera[0]))
    camera[1] = max(0, min(c.HEIGHT*c.gridy_dim - c.window_size[1], camera[1]))

    mouse_grid_pos = list(p+c for p,c in zip(mouse_pos, camera))

    '''Rendering/Drawing goes here (Below the white screen fill)'''

    screen.fill(c.BLACK)

    '''Draw grid'''
    for row in range(c.gridx_dim):
        for column in range(c.gridy_dim):
            colour = c.WHITE
            pygame.draw.rect(screen,
                             colour,
                             [c.WIDTH * column - camera[0],
                              c.HEIGHT * row - camera[1],
                              c.WIDTH-c.MARGIN,
                              c.HEIGHT-c.MARGIN])

    '''Display what has been drawn'''
    pygame.display.flip()

    '''Limit the program to 60 FPS'''
    clock.tick(60)

#Clean up
pygame.quit()

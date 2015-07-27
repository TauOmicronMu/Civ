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

'''Generate a grid of size c.gridx by c.gridy'''

grid = [[0 for x in range(c.gridx_dim)] for y in range(c.gridy_dim)]

pygame.init()

size = c.window_size
screen = pygame.display.set_mode(size)

pygame.display.set_caption(c.window_caption)

quitflag = False

clock = pygame.time.Clock()

while not quitflag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitflag = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (c.cell_WIDTH+ c.MARGIN)
            row = pos[1] // (c.HEIGHT + c.MARGIN)
            grid[row][column] = 0
            print("row: " + str(row) + " column: " + str(column))

    '''Game logic goes here'''

    '''Rendering/Drawing goes here (Below the white screen fill)'''

    screen.fill(c.BLACK)

    '''Draw grid'''
    for row in range(c.gridx_dim):
        for column in range(c.gridy_dim):
            colour = c.WHITE
            pygame.draw.rect(screen,
                             colour,
                             [(c.MARGIN + c.WIDTH) * column + c.MARGIN,
                              (c.MARGIN + c.HEIGHT) * row + c.MARGIN,
                              c.WIDTH,
                              c.HEIGHT])

    '''Display what has been drawn'''
    pygame.display.flip()

    '''Limit the program to 60 FPS'''
    clock.tick(60)

#Clean up
pygame.quit()
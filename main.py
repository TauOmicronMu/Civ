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
    from City import * #Loads the City class.
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


'''Init PyGame'''
pygame.init()
size = c.window_size
screen = pygame.display.set_mode(size)

'''Load in tile images'''
tile_imgs = {}
TILE_NAMES = ["cattle", "city", "fish", "forest", "gold", "grass", "hill", "horses", "iron", "marble", "sheep", "silver", "stone", "water"]
LAND_NAMES = ["cattle", "city", "forest", "gold", "grass", "hill", "horses", "iron", "marble", "sheep", "silver", "stone"]
SEA_NAMES = ["fish", "water"]
TILE = {}
for (i, name) in zip(xrange(len(TILE_NAMES)), TILE_NAMES):
    tile_imgs[name] = pygame.image.load(os.path.join("dat", "%s_tile.png" % name)).convert(screen)
    TILE[name] = i

'''Generate a grid of size c.gridx by c.gridy'''
grid = [[TILE['water'] for x in range(c.gridx_dim)] for y in range(c.gridy_dim)]

def gen_blob():
    blob_size = random.randint(30, 130)
    blob_x_base = random.randint(0,c.gridx_dim-1)
    blob_y_base = random.randint(0,c.gridy_dim-1)
    while grid[blob_y_base][blob_x_base] != TILE['water']:
        blob_x_base = random.randint(0,c.gridx_dim-1)
        blob_y_base = random.randint(0,c.gridy_dim-1)

    blob_x, blob_y = blob_x_base, blob_y_base
    deposit_type = 'horses'
    deposit_count = 1
    for i in xrange(blob_size):
        blob_x, blob_y = (blob_x_base+blob_x*3)//4, (blob_y_base+blob_y*3)//4
        while grid[blob_y][blob_x] != TILE['water']:
            u, v = random.choice(((1, 0), (0, 1), (-1, 0), (0, -1)))
            blob_x += u
            blob_y += v
            if blob_x < 0 or blob_y < 0 or blob_x >= c.gridx_dim or blob_y >= c.gridy_dim:
                blob_x, blob_y = blob_x_base, blob_y_base
                deposit_type = 'grass'
                deposit_count = 1

        grid[blob_y][blob_x] = TILE[deposit_type]
        deposit_count -= 1
        if deposit_count <= 0:
            if random.random() < 0.1:
                deposit_type = random.choice(('cattle', 'forest', 'forest', 'forest', 'gold', 'hill', 'hill', 'iron', 'marble',
                    'sheep', 'silver', 'stone'))
                if deposit_type == "forest" or deposit_type == "hill":
                    deposit_count = random.randint(2,5)
                else:
                    deposit_count = random.randint(0,2)
            else:
                deposit_type = 'grass'
                deposit_count = 1

def populate_with_fish():
    for row in range(c.gridx_dim):
        for column in range(c.gridy_dim):
            if grid[row][column] == TILE['water']:
                chance_number = random.randint(0,9)
                if chance_number == 0:
                    grid[row][column] = TILE['fish']

def place_player_cities():
    #Place player 1's city in the top left ninth of the map, ensuring that it's on land.
    city_created = False
    while city_created == False:
        random_x_coord = random.randint(0, math.floor((c.gridx_dim - 1)/3.0))
        random_y_coord = random.randint(0, math.floor((c.gridy_dim - 1)/3.0))
        for tile in LAND_NAMES:
            if grid[random_x_coord][random_y_coord] == TILE[tile]:
                grid[random_x_coord][random_y_coord] = TILE["city"]
                player_one_city = City(1, c.CITY_MAX_HEALTH, c.CITY_DAMAGE, random_x_coord, random_y_coord)
                city_created = True
                print "x : " + str(random_x_coord) + " y: " + str(random_y_coord)
    #Place player 2's city in the bottom right ninth of the map, ensuring that it's on land.
    city_created = False
    while city_created == False:
        random_x_coord = random.randint(math.floor((c.gridx_dim - 1)*(2.0/3.0)), (c.gridx_dim - 1))
        random_y_coord = random.randint(math.floor((c.gridy_dim - 1) * (2.0/3.0)), (c.gridy_dim - 1))
        for tile in LAND_NAMES:
            if grid[random_x_coord][random_y_coord] == TILE[tile]:
                grid[random_x_coord][random_y_coord] = TILE["city"]
                player_two_city = City(2, c.CITY_MAX_HEALTH, c.CITY_DAMAGE, random_x_coord, random_y_coord)
                city_created = True
                print "x : " + str(random_x_coord) + " y: " + str(random_y_coord)



#increment or decrement blob count to change the number of islands/blobs.
for blob_count in xrange(12):
    gen_blob()

populate_with_fish()
place_player_cities()

camera = [0, 0]
mouse_pos = tuple(v//2 for v in size)
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
            #grid[column][row] = TILE['fish']
            print("row: " + str(row) + " column: " + str(column) + " ")
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

    '''Rendering/Drawing goes here (Below the black screen fill)'''

    screen.fill(c.BLACK)

    '''Draw grid'''
    for row in range(c.gridx_dim):
        for column in range(c.gridy_dim):
            colour = c.WHITE
            screen.blit(tile_imgs[TILE_NAMES[grid[column][row]]], (c.WIDTH*column - camera[0], c.HEIGHT*row - camera[1]))
            """
            pygame.draw.rect(screen,
                             colour,
                             [c.WIDTH * column - camera[0],
                              c.HEIGHT * row - camera[1],
                              c.WIDTH-c.MARGIN,
                              c.HEIGHT-c.MARGIN])
            """

    '''Display what has been drawn'''
    pygame.display.flip()

    '''Limit the program to 60 FPS'''
    clock.tick(60)

#Clean up
pygame.quit()

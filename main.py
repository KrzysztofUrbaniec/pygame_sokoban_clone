import pygame, sys
from pygame.locals import *
from map import LevelMap, Floor, Box, Wall, BoxSpot
from constants import *
from entities import Player
import logging
from debug import debug

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

def main():
    global DISPLAYSURF, SCREENSURF, FPSCLOCK
    DISPLAYSURF = pygame.display.set_mode((DISPLAYSURF_WIDTH, DISPLAYSURF_HEIGHT))
    SCREENSURF = pygame.Surface((SCREENSURF_WIDTH, SCREENSURF_HEIGHT))
    pygame.display.set_caption('Sokoban')
    FPSCLOCK = pygame.time.Clock()

    level1 = LevelMap('my_projects/sokoban/levels/level1.txt', SCREENSURF)

    # Player
    player_img = pygame.image.load('my_projects/sokoban/images/player.png')
    player_rect = player_img.get_rect()
    player_rect.x, player_rect.y = level1.start_x, level1.start_y
    player_step_count = 0
    
    while True:
        SCREENSURF.fill(LIGHTBLUE)

        direction = None
        
        # Set all box states to False at the beginning of the loop, so it the box was moved
        # to right spot, but then was removed, the state won't stay as True
        for box in level1.boxes:
            box.state = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Player movement and changing position
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player_rect.x -= level1.tile_size
                    direction = LEFT
                    player_step_count += 1
                if event.key == K_RIGHT:
                    player_rect.x += level1.tile_size
                    direction = RIGHT
                    player_step_count += 1
                if event.key == K_UP:
                    player_rect.y -= level1.tile_size
                    direction = UP
                    player_step_count += 1
                if event.key == K_DOWN:
                    player_rect.y += level1.tile_size
                    direction = DOWN
                    player_step_count += 1
                if event.key == K_r:
                    reset_level(level1, player_rect)

        # Boxes movement
        for box in level1.boxes:
            if box.rect.x == player_rect.x and box.rect.y == player_rect.y:
                if direction == DOWN:
                    box.rect.y += level1.tile_size
                if direction == UP:
                    box.rect.y -= level1.tile_size
                if direction == LEFT:
                    box.rect.x -= level1.tile_size
                if direction == RIGHT:
                    box.rect.x += level1.tile_size

            # Check if moved box collides with walls - if yes, then return in to previous position
            for tile in level1.tiles:
                if box.rect.x == tile.rect.x and box.rect.y == tile.rect.y and isinstance(tile, Wall):
                    if direction == DOWN:
                        box.rect.y -= level1.tile_size
                        player_rect.y -= level1.tile_size
                    if direction == UP:
                        box.rect.y += level1.tile_size
                        player_rect.y += level1.tile_size
                    if direction == LEFT:
                        box.rect.x += level1.tile_size
                        player_rect.x += level1.tile_size
                    if direction == RIGHT:
                        box.rect.x -= level1.tile_size
                        player_rect.x -= level1.tile_size

                if box.rect.colliderect(tile.rect) and isinstance(tile, BoxSpot):
                    box.state = True

            # Check if currently moving box collides with other box
            for box2 in level1.boxes:
                if box.rect.x == box2.rect.x and box.rect.y == box2.rect.y and box is not box2:
                    if direction == DOWN:
                        box.rect.y -= level1.tile_size
                        player_rect.y -= level1.tile_size
                    if direction == UP:
                        box.rect.y += level1.tile_size
                        player_rect.y += level1.tile_size
                    if direction == LEFT:
                        box.rect.x += level1.tile_size
                        player_rect.x += level1.tile_size
                    if direction == RIGHT:
                        box.rect.x -= level1.tile_size
                        player_rect.x -= level1.tile_size    

        # Collisions with other tiles
        for rect in level1.tiles:
            if rect.x == player_rect.x and rect.y == player_rect.y and isinstance(rect, Wall):
                if direction == DOWN:
                    player_rect.y -= level1.tile_size
                if direction == UP:
                    player_rect.y += level1.tile_size
                if direction == LEFT:
                    player_rect.x += level1.tile_size
                if direction == RIGHT:
                    player_rect.x -= level1.tile_size
        
        # Check if all boxes are in proper spots
        boxes_boolean = [box.state for box in level1.boxes]
        if False not in boxes_boolean:
            print("Victory")

        # Scroll variables
        cameraX = player_rect.x - SCREENSURF_WIDTH // 2
        cameraY = player_rect.y - SCREENSURF_HEIGHT // 2

        level1.draw_map((cameraX, cameraY)) 

        SCREENSURF.blit(player_img, (player_rect.x - cameraX, player_rect.y - cameraY))
        create_step_count_label(player_step_count)
        
        scaled_surf = pygame.transform.scale(SCREENSURF, DISPLAYSURF.get_size())
        DISPLAYSURF.blit(scaled_surf, (0,0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def reset_level(level, player_rect):
    level.tiles, level.boxes = level.create_tiles()
    player_rect.x, player_rect.y = level.start_x, level.start_y

def create_step_count_label(player_step_count):
    text_font = pygame.font.SysFont('comicsans', 18)
    count_text = text_font.render(f'Step count: {player_step_count}', True, TEXT_COLOR, TEXT_COLOR)
    count_text.set_colorkey(WHITE)
    SCREENSURF.blit(count_text, (SCREENSURF_WIDTH*0.04, SCREENSURF_HEIGHT*0.95))

if __name__ == '__main__':
    main()


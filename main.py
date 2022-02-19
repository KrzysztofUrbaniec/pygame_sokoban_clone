import pygame, sys
from pygame.locals import *
from map import LevelMap
from constants import *
from entities import Player
import logging

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
    

    while True:
        SCREENSURF.fill(LIGHTBLUE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        level1.draw_map()
        SCREENSURF.blit(player_img, player_rect)

        scaled_surf = pygame.transform.scale(SCREENSURF, DISPLAYSURF.get_size())
        DISPLAYSURF.blit(scaled_surf, (0,0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()


import pygame, sys, os
from pygame.locals import *
from map import LevelMap, Wall, BoxSpot
from constants import *
import logging
from debug import debug

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

def main():
    global DISPLAYSURF, SCREENSURF, FPSCLOCK
    DISPLAYSURF = pygame.display.set_mode((DISPLAYSURF_WIDTH, DISPLAYSURF_HEIGHT))
    SCREENSURF = pygame.Surface((SCREENSURF_WIDTH, SCREENSURF_HEIGHT))
    pygame.display.set_caption('Sokoban')
    FPSCLOCK = pygame.time.Clock()

    levels = load_levels("my_projects/sokoban/levels")
    level_counter = 0
    current_level = levels[level_counter]
    while True:
        level_counter, level_passed = run_level(current_level, levels, level_counter)
        level_counter, current_level = next_level(levels, level_counter, level_passed)
    
def next_level(levels, level_counter, level_passed):

    if level_passed:
        create_won_msg(levels, level_counter)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if level_counter < len(levels):
                        for level in levels:
                            level.tiles, level.boxes = level.create_tiles()
                        return level_counter, levels[level_counter]
                    else:
                        level_counter = 0
                        # Reset positions of tiles for all levels
                        for level in levels:
                            level.tiles, level.boxes = level.create_tiles()
                        return level_counter, levels[0]
        
        if not level_passed:
            if level_counter == len(levels):
                level_counter = 0
                # Reset positions of tiles for all levels
                for level in levels:
                    level.tiles, level.boxes = level.create_tiles()
                return level_counter, levels[0]
            elif level_counter < 0:
                level_counter = len(levels) - 1
                for level in levels:
                    level.tiles, level.boxes = level.create_tiles()
                return level_counter, levels[level_counter]
            elif level_counter < len(levels):
                        for level in levels:
                            level.tiles, level.boxes = level.create_tiles()
                        return level_counter, levels[level_counter]


def run_level(current_level, levels, level_counter):
    # Player
    player_img = pygame.image.load('my_projects/sokoban/images/player.png')
    player_img.set_colorkey(WHITE)
    player_rect = player_img.get_rect()
    player_rect.x, player_rect.y = current_level.start_x, current_level.start_y
    player_step_count = 0
    
    level_passed = False

    while True:
        SCREENSURF.fill(LIGHTBLUE)

        direction = None
        
        # Set all box states to False at the beginning of the loop, so it the box was moved
        # to right spot, but then was removed, the state won't stay as True
        for box in current_level.boxes:
            box.state = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Player movement and changing position
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player_rect.x -= current_level.tile_size
                    direction = LEFT
                    player_step_count += 1
                if event.key == K_RIGHT:
                    player_rect.x += current_level.tile_size
                    direction = RIGHT
                    player_step_count += 1
                if event.key == K_UP:
                    player_rect.y -= current_level.tile_size
                    direction = UP
                    player_step_count += 1
                if event.key == K_DOWN:
                    player_rect.y += current_level.tile_size
                    direction = DOWN
                    player_step_count += 1
                if event.key == K_r:
                    reset_level(current_level, player_rect)
                    player_step_count = 0
                if event.key == K_e:
                    return level_counter + 1, level_passed
                if event.key == K_q:
                    return level_counter - 1, level_passed

        # Boxes movement
        for box in current_level.boxes:
            if box.rect.x == player_rect.x and box.rect.y == player_rect.y:
                if direction == DOWN:
                    box.rect.y += current_level.tile_size
                if direction == UP:
                    box.rect.y -= current_level.tile_size
                if direction == LEFT:
                    box.rect.x -= current_level.tile_size
                if direction == RIGHT:
                    box.rect.x += current_level.tile_size

            # Check if moved box collides with walls - if yes, then return in to previous position
            for tile in current_level.tiles:
                if box.rect.x == tile.rect.x and box.rect.y == tile.rect.y and isinstance(tile, Wall):
                    if direction == DOWN:
                        box.rect.y -= current_level.tile_size
                        player_rect.y -= current_level.tile_size
                        player_step_count -= 1
                    if direction == UP:
                        box.rect.y += current_level.tile_size
                        player_rect.y += current_level.tile_size
                        player_step_count -= 1
                    if direction == LEFT:
                        box.rect.x += current_level.tile_size
                        player_rect.x += current_level.tile_size
                        player_step_count -= 1
                    if direction == RIGHT:
                        box.rect.x -= current_level.tile_size
                        player_rect.x -= current_level.tile_size
                        player_step_count -= 1

                if box.rect.colliderect(tile.rect) and isinstance(tile, BoxSpot):
                    box.state = True

            # Check if currently moving box collides with other box
            for box2 in current_level.boxes:
                if box.rect.x == box2.rect.x and box.rect.y == box2.rect.y and box is not box2:
                    if direction == DOWN:
                        box.rect.y -= current_level.tile_size
                        player_rect.y -= current_level.tile_size
                        player_step_count -= 1
                    if direction == UP:
                        box.rect.y += current_level.tile_size
                        player_rect.y += current_level.tile_size
                        player_step_count -= 1
                    if direction == LEFT:
                        box.rect.x += current_level.tile_size
                        player_rect.x += current_level.tile_size
                        player_step_count -= 1
                    if direction == RIGHT:
                        box.rect.x -= current_level.tile_size
                        player_rect.x -= current_level.tile_size    
                        player_step_count -= 1

        # Collisions with other tiles
        for rect in current_level.tiles:
            if rect.x == player_rect.x and rect.y == player_rect.y and isinstance(rect, Wall):
                if direction == DOWN:
                    player_rect.y -= current_level.tile_size
                    player_step_count -= 1
                if direction == UP:
                    player_rect.y += current_level.tile_size
                    player_step_count -= 1
                if direction == LEFT:
                    player_rect.x += current_level.tile_size
                    player_step_count -= 1
                if direction == RIGHT:
                    player_rect.x -= current_level.tile_size
                    player_step_count -= 1

        # Scroll variables
        cameraX = player_rect.x - SCREENSURF_WIDTH // 2
        cameraY = player_rect.y - SCREENSURF_HEIGHT // 2

        current_level.draw_map((cameraX, cameraY)) 

        SCREENSURF.blit(player_img, (player_rect.x - cameraX, player_rect.y - cameraY))
        create_step_count_label(player_step_count)
        create_level_label(levels, level_counter)
        
        scaled_surf = pygame.transform.scale(SCREENSURF, DISPLAYSURF.get_size())
        DISPLAYSURF.blit(scaled_surf, (0,0))

        # Check if all boxes are in proper spots
        boxes_boolean = [box.state for box in current_level.boxes]
        if False not in boxes_boolean:
            pygame.display.update()
            level_passed = True
            return level_counter + 1, level_passed

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def load_levels(path_to_level_directory):
    levels = [level for level in os.listdir(path_to_level_directory)]
    file_count = len(levels)
    map_levels = []
    for level_number in range(1, file_count+1):
        level_name = 'level' + '_' + str(level_number) + '.txt'
        level = os.path.join(path_to_level_directory, level_name)
        logging.debug(level)
        map_levels.append(LevelMap(level, SCREENSURF))

    return map_levels

def reset_level(level, player_rect):
    level.tiles, level.boxes = level.create_tiles()
    player_rect.x, player_rect.y = level.start_x, level.start_y

def create_won_msg(levels, level_counter):
    text_font = pygame.font.SysFont('comicsans', 48)
    # if level_counter == len(levels):
    #     congrats_text = text_font.render("Congratulations!", False, TEXT_COLOR, WHITE)    
    #     completed_text = text_font.render("You completed all levels", False, TEXT_COLOR, WHITE)

    #     congrats_text_rect = congrats_text.get_rect()
    #     congrats_text_rect.centerx, congrats_text_rect.centery = SCREENSURF_WIDTH * 0.5, SCREENSURF_HEIGHT * 0.4
    #     congrats_text.set_colorkey(WHITE)

    #     completed_text_rect = completed_text.get_rect()
    #     completed_text_rect.centerx, completed_text_rect.centery = SCREENSURF_WIDTH * 0.5, SCREENSURF_HEIGHT * 0.6
    #     completed_text.set_colorkey(WHITE)

    #     SCREENSURF.blit(congrats_text, congrats_text_rect)
    #     SCREENSURF.blit(completed_text, completed_text_rect)
    # else:
    won_text = text_font.render("You won!", False, TEXT_COLOR, WHITE)
    won_text_rect = won_text.get_rect()
    won_text_rect.centerx, won_text_rect.centery = SCREENSURF_WIDTH * 0.5, SCREENSURF_HEIGHT * 0.5
    won_text.set_colorkey(WHITE)
    SCREENSURF.blit(won_text, won_text_rect)

    create_press_spacebar_msg(levels, level_counter)

    scaled_surf = pygame.transform.scale(SCREENSURF, DISPLAYSURF.get_size())
    DISPLAYSURF.blit(scaled_surf, (0,0))
    pygame.display.update()

def create_press_spacebar_msg(levels, level_counter):
    text_font = pygame.font.SysFont('comicsans', 24)
    if level_counter == len(levels):
        press_spacebar_text = text_font.render("Press spacebar to proceed to the first level", False, TEXT_COLOR, WHITE)
    else:
        press_spacebar_text = text_font.render("Press spacebar to proceed to the next level", False, TEXT_COLOR, WHITE)
    press_spacebar_text_rect = press_spacebar_text.get_rect()
    press_spacebar_text_rect.centerx, press_spacebar_text_rect.centery = SCREENSURF_WIDTH * 0.5, SCREENSURF_HEIGHT * 0.9
    press_spacebar_text.set_colorkey(WHITE)

    SCREENSURF.blit(press_spacebar_text, press_spacebar_text_rect)

def create_level_label(levels, level_counter):
    text_font = pygame.font.SysFont('comicsans', 18)
    logging.debug(level_counter)
    level_text = text_font.render(f'Level {level_counter + 1} of {len(levels)}', False, TEXT_COLOR, WHITE)
    level_text_rect = level_text.get_rect()
    level_text_rect.centerx, level_text_rect.centery = SCREENSURF_WIDTH * 0.12, SCREENSURF_HEIGHT * 0.05
    level_text.set_colorkey(WHITE)
    SCREENSURF.blit(level_text, level_text_rect)

def create_step_count_label(player_step_count):
    text_font = pygame.font.SysFont('comicsans', 18)
    count_text = text_font.render(f'Step count: {player_step_count}', False, TEXT_COLOR, WHITE)
    count_text_rect = count_text.get_rect()
    count_text_rect.centerx, count_text_rect.centery = SCREENSURF_WIDTH * 0.12, SCREENSURF_HEIGHT * 0.10
    count_text.set_colorkey(WHITE)
    SCREENSURF.blit(count_text, count_text_rect)

if __name__ == '__main__':
    main()


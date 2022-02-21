import pygame
from entities import Player
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

class Tile:

    def __init__(self, x, y, image, parent_surface):
        self.x = x
        self.y = y
        self.parent_surface = parent_surface
        self.image = image
        self.rect = image.get_rect()
        # Set rect x & y to position on the grid, so the image will be rendered in proper place
        self.rect.x, self.rect.y = self.x, self.y

    def draw_tile(self, camera):
        # Draw the image
        self.parent_surface.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))

class Box(Tile):

    def __init__(self, x, y, image, parent_surface):
        super().__init__(x, y, image, parent_surface)
        self.state = False

class BoxSpot(Tile):

    def __init__(self, x, y, image, parent_surface):
        super().__init__(x, y, image, parent_surface)

class Floor(Tile):

    def __init__(self, x, y, image, parent_surface):
        super().__init__(x, y, image, parent_surface)

class Wall(Tile):
    
    def __init__(self, x, y, image, parent_surface):
        super().__init__(x, y, image, parent_surface)

class LevelMap:
    
    def __init__(self, level_file, parent_surface):
        self.level_file = level_file
        self.parent_surface = parent_surface
        
        self.level_map = self.read_map_from_file()
        self.tile_size = 16

        self.start_x = 0
        self.start_y = 0

        self.tiles, self.boxes = self.create_tiles()


    def read_map_from_file(self):
        # Load file with the map        
        with open(self.level_file, 'r') as map_data:
            map = []

            # Read file in rows and append them to map list without the last character ('\n')
            for line in map_data.readlines():
                row = []
                for tile in line:
                    if tile != '\n':
                        row.append(tile)
                map.append(row)

        return map

    def create_tiles(self):
        tiles = []
        boxes = []
        for y, row in enumerate(self.level_map):
            # Create different tiles in starting positions
            for x, tile in enumerate(row):
                if tile == '1':
                    tiles.append(Wall(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/wall.png'), self.parent_surface))
                if tile == '2':
                    tiles.append(Floor(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/floor.png'), self.parent_surface))
                if tile == '3':
                    tiles.append(Floor(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/floor.png'), self.parent_surface))
                    self.start_x, self.start_y = x*self.tile_size, y*self.tile_size
                if tile == '4':
                    tiles.append(Floor(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/floor.png'), self.parent_surface))
                    box = Box(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/box.png'), self.parent_surface)
                    boxes.append(box)
                if tile == '5':
                    tiles.append(BoxSpot(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/box_spot.png'), self.parent_surface))

        return tiles, boxes

    def draw_map(self, camera):
        # Draw each tile according to its rect's position
        for tile in self.tiles:
            tile.draw_tile(camera)
        
        for box in self.boxes:
            box.draw_tile(camera)

# if __name__ == "__main__":
#     level1 = LevelMap()
#     print(level1.read_map_from_file())
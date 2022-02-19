import pygame
from entities import Player

class Tile:

    def __init__(self, x, y, image, parent_surface):
        self.x = x
        self.y = y
        self.parent_surface = parent_surface
        self.image = image
        self.rect = image.get_rect()
        # Set rect x & y to position on the grid, so the image will be rendered in proper place
        self.rect.x, self.rect.y = self.x, self.y

    def draw_tile(self):
        # Draw the image
        self.parent_surface.blit(self.image, (self.rect.x, self.rect.y))

class LevelMap:
    
    def __init__(self, level_file, parent_surface):
        self.level_file = level_file
        self.parent_surface = parent_surface
        
        self.level_map = self.read_map_from_file()
        self.tile_size = 16

        self.start_x = 0
        self.start_y = 0

        self.tiles = self.create_tiles()


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
        for y, row in enumerate(self.level_map):
            # Create different tiles in right spots
            for x, tile in enumerate(row):
                if tile == '1':
                    tiles.append(Tile(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/wall.png'), self.parent_surface))
                if tile == '2':
                    tiles.append(Tile(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/floor.png'), self.parent_surface))
                if tile == '3':
                    self.start_x, self.start_y = x*self.tile_size, y*self.tile_size
                if tile == '4':
                    tiles.append(Tile(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/box.png'), self.parent_surface))
                if tile == '5':
                    tiles.append(Tile(x*self.tile_size, y*self.tile_size, pygame.image.load('my_projects/sokoban/images/box_spot.png'), self.parent_surface))

        return tiles

    def draw_map(self):
        # Draw each tile according to its rect's position
        for tile in self.tiles:
            tile.draw_tile()

# if __name__ == "__main__":
#     level1 = LevelMap()
#     print(level1.read_map_from_file())
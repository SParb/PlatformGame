from settings import *


class Level:
    def __init__(self, data):
        self.tile_list = []
        self.collide_tile_list = []
        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile not in [0, 1]:
                    img = sprites1_dict[tile]
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1

    def draw(self, screen_scroll):

        for tile in self.tile_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

from settings import *


class Level:
    def __init__(self, data, x_offset, y_offset):
        self.tile_list = []
        self.collide_tile_list = []
        self.x_offset = x_offset
        self.y_offset = y_offset

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile[1] not in [0, 1]:
                    img = sprites1_dict[tile[1]]
                    img_rect = img.get_rect()
                    img_rect.x = (column_count + self.x_offset) * tile_size
                    img_rect.y = (row_count + self.y_offset) * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1

    def draw(self, x_screen_scroll, y_screen_scroll):
        for tile in self.tile_list:
            tile[1][0] += x_screen_scroll
            tile[1][1] += y_screen_scroll
            screen.blit(tile[0], tile[1])

    def editor_draw(self, offset):
        for tile in self.tile_list:
            tile[1][0] += offset[0]
            tile[1][1] += offset[1]
            screen.blit(tile[0], tile[1])
        offset = [0, 0]
        return offset

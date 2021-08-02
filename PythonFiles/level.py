from settings import *


class Level:
    def __init__(self, data):
        self.tile_list = []
        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile != 0:
                    img = pygame.transform.scale(pygame.image.load(blockID.get(tile)), (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

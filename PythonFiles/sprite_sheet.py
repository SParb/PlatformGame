import pygame


class Spritesheet:
    def __init__(self, filename, tile_size, imgtilesize, imgwidth, imgheight):
        self.filename = filename
        self.tile_size = tile_size
        self.sprite_sheet = pygame.transform.scale(pygame.image.load(filename),
                                                   ((imgwidth*tile_size)//imgtilesize, (imgheight*tile_size)//imgtilesize))
        self.coors = self.sprite_sheet.get_rect().size
        self.xsize = self.coors[0]//tile_size
        self.ysize = self.coors[1]//tile_size

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        sprite = sprite.convert_alpha()
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def create_sprite_dic(self, c):
        sprites_dic = {}
        counter = c
        for y in range(self.ysize):
            for x in range(self.xsize):
                sprite = self.get_sprite(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                sprites_dic[counter] = sprite
                counter += 1
        return sprites_dic





"""pygame.init()
title_font = pygame.font.SysFont("Calibri", 60)
button_font = pygame.font.SysFont("Calibri", 20)
res = (1200, 800)
tile_size = 20
screen = pygame.display.set_mode(res)
screen_width = screen.get_width()
screen_height = screen.get_height()
running = True
sprites = Spritesheet("../Images/Blocks/Dungeon_assets/Assets.png", 20)
xcor, ycor = sprites.sprite_sheet.get_rect().size
sprite1 = sprites.get_sprite(0, 0, 20, 20)  # xcor, ycor, tilesizex, tilesizey
dict = sprites.create_sprite_dic()
while running:
    screen.fill((0, 60, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    sprites.blit_tiles(dict, screen)
    pygame.display.update()
pygame.quit()"""
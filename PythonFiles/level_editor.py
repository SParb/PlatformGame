from level import *


def hover_tile():  # when a grid tile is hovered it is highlighted
    mouse = pygame.mouse.get_pos()
    if mouse[0] < level_width and mouse[1] < level_height:
        x = mouse[0] // tile_size
        y = mouse[1] // tile_size
        htile = pygame.Rect(x * tile_size, y*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, (0, 70, 0), htile, width=2)


def change_tile(x, y, left_click, selected):  # change the tile when clicked
    x = x // tile_size
    y = y // tile_size
    if left_click:
        write_to_file(x, y, selected)
    else:
        write_to_file(x, y, 0)


def write_to_file(x, y, selected):
    with open(data, "r") as file:
        linelist = file.readlines()
        newrow = linelist[y].split(",")
        if newrow[x] == newrow[-1]:
            newrow[x] = str(selected)+"\n"
        else:
            newrow[x] = str(selected)
        newstr = ""
        for char in newrow:
            newstr += char
            newstr += ","
        newstr = newstr[:-1]
        linelist[y] = newstr

    with open(data, "w") as file:
        file.writelines(linelist)
    file.close()

def draw_tile_list():  # draw the list of tile types
    tile_list = []
    posx = level_width + tile_size * 2
    posy = tile_size
    count = 0
    for id in blockID:
        img = pygame.transform.scale(pygame.image.load(blockID.get(id)), (tile_size, tile_size))
        img_rect = img.get_rect()
        img_rect.x = posx
        img_rect.y = posy
        tile = (img, img_rect, id)
        tile_list.append(tile)
        if count >= 3:
            count = 0
            posx = level_width + tile_size * 2
            posy += tile_size * 2
        else:
            posx += tile_size * 2
            count += 1
    for tile in tile_list:
        screen.blit(tile[0], tile[1])
    return tile_list



pygame.init()
res = (1400, 900)
screen = pygame.display.set_mode(res)
screen_width = screen.get_width()
screen_height = screen.get_height()
level_width = 1200
level_height = 800
pygame.display.set_caption("Platform game editor")
background = pygame.image.load("../Images/Backgrounds/background_forest.jpg")
selected_block = None

data = "../LevelTileMaps/level1a"
running = True
edit_level = Level(read_level_data(data))
while running:
    click = False
    rclick = False
    mx, my = pygame.mouse.get_pos()
    screen.fill((60, 25, 60))
    screen.blit(background, (0, 0))
    edit_level.draw()
    draw_grid()
    hover_tile()
    t_list = draw_tile_list()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
            if event.button == 3:
                rclick = True

    if selected_block is not None:  # shows selected block in tile list
        pygame.draw.rect(screen, (0, 255, 255), selected_block[1], width=2)
        if mx < level_width and my < level_height:
            if click:
                change_tile(mx, my, True, selected_block[2])
                edit_level = Level(read_level_data(data))
            if rclick:
                change_tile(mx, my, False, selected_block[2])
                edit_level = Level(read_level_data(data))
    for tile in t_list:  # changes selected block in tile list when clicked
        if tile[1].collidepoint((mx, my)):
            pygame.draw.rect(screen, (0, 255, 0), tile[1], width=2)
            if click:
                selected_block = tile


    pygame.display.update()
    clock.tick(60)

pygame.quit()

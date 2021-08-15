from level import *


def draw_text(text, font, colour, surface, x, y):
    text = font.render(text, 1, colour)
    textrect = text.get_rect()
    textrect.topleft = (x, y)
    surface.blit(text, textrect)


def hover_tile():  # when a grid tile is hovered it is highlighted
    mouse = pygame.mouse.get_pos()
    if mouse[0] < level_width and mouse[1] < level_height:
        x = mouse[0] // tile_size
        y = mouse[1] // tile_size
        htile = pygame.Rect(x * tile_size, y*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, (0, 70, 0), htile, width=2)


def draw_block_grid():
    for line in range(0, 40):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (level_width-1, line * tile_size))
    for line in range(0, 60):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, level_height-1))
    for tile in edit_level.tile_list:
        block = pygame.Rect(tile[1].x+1, tile[1].y+1, tile_size-2, tile_size-2)
        pygame.draw.rect(screen, (0, 0, 0), block, width=3)


def change_tile(x, y, left_click, selected):  # change the tile when clicked
    x = (x + total_offset) // tile_size
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


def draw_tile_list(xstart, ystart, width):  # draw the list of tile types
    listbackground = pygame.Rect(level_width, 0, screen_width-level_width, screen_height)
    pygame.draw.rect(screen, (0, 100, 0), listbackground)
    tile_list = []
    posx = xstart
    posy = ystart
    count = 0
    for id in sprites1_dict:
        img = sprites1_dict[id]
        img_rect = img.get_rect()
        img_rect.x = posx
        img_rect.y = posy
        tile = (img, img_rect, id)
        tile_list.append(tile)
        if count >= width:
            count = 0
            posx = xstart
            posy += tile_size
        else:
            posx += tile_size
            count += 1
    for tile in tile_list:
        screen.blit(tile[0], tile[1])
    return tile_list


pygame.init()
res = (1750, 900)
offset = 0
total_offset = 0
screen = pygame.display.set_mode(res)
screen_width = screen.get_width()
screen_height = screen.get_height()
level_width = 1200
level_height = 800
pygame.display.set_caption("Platform game editor")
background = pygame.image.load("../Images/Backgrounds/background_forest.jpg")
selected_block = None
data = "../LevelTileMaps/level1"
running = True
grid = False
edit_level = Level(read_level_data(data))
while running:
    click = False
    mx, my = pygame.mouse.get_pos()
    screen.fill((0, 100, 0))
    screen.blit(background, (0, 0))
    offset = edit_level.editor_draw(offset)
    if grid:
        draw_block_grid()
    t_list1 = draw_tile_list(level_width + tile_size, tile_size, 24)
    hover_tile()
    grid_button = pygame.Rect(tile_size, screen_height-30-button_height, button_width, button_height)
    camera_limit = pygame.Rect(tile_size*25, level_height, 201, tile_size)
    pygame.draw.rect(screen, (0, 70, 0), grid_button, border_radius=10)
    pygame.draw.rect(screen, (200, 70, 0), camera_limit)
    left, middle, right = pygame.mouse.get_pressed(num_buttons=3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == pygame.KEYDOWN:  # move camera left or right
            if event.key == pygame.K_d:
                if total_offset != (len(read_level_data(data)[0]*tile_size)) - level_width:
                    offset = -5 * tile_size
                    total_offset += 5 * tile_size
            if event.key == pygame.K_a:
                if total_offset != 0:
                    offset = 5 * tile_size
                    total_offset -= 5 * tile_size
    if grid_button.collidepoint((mx, my)):  # toggle grid
        pygame.draw.rect(screen, (0, 30, 0), grid_button, border_radius=10)
        if click:
            if grid:
                grid = False
            else:
                grid = True

    draw_text("Toggle grid", button_font, (255, 255, 255), screen, tile_size+button_height//2, screen_height-button_height-20)
    draw_text("Offset: " + str(total_offset), button_font, (255, 255, 255), screen,
              screen_width - 700,
              screen_height - button_height - 20)
    draw_text("Max camera offset", button_font, (255, 255, 255), screen, tile_size*26, level_height)

    if selected_block is not None:  # shows selected block in tile list
        draw_text("Selected block ID: "+str(selected_block[2]), button_font, (255, 255, 255), screen, screen_width-500,
                  screen_height - button_height - 20)
        pygame.draw.rect(screen, (0, 255, 255), selected_block[1], width=2)
        if mx < level_width and my < level_height:
            if left:
                change_tile(mx, my, True, selected_block[2])
                edit_level = Level(read_level_data(data))
                offset = -total_offset
            if right:
                change_tile(mx, my, False, selected_block[2])
                edit_level = Level(read_level_data(data))
                offset = -total_offset
    else:
        draw_text("Selected block ID: None", button_font, (255, 255, 255), screen, screen_width-500,
                  screen_height - button_height - 20)

    for t in t_list1:  # changes selected block in tile list when clicked
        if t[1].collidepoint((mx, my)):
            pygame.draw.rect(screen, (0, 255, 0), t[1], width=2)
            if click:
                selected_block = t
    pygame.display.update()
    clock.tick(60)


pygame.quit()

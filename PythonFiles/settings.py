import pygame


pygame.init()
title_font = pygame.font.SysFont("Calibri", 60)
button_font = pygame.font.SysFont("Calibri", 20)
res = (1200, 800)
screen = pygame.display.set_mode(res)
screen_width = screen.get_width()
screen_height = screen.get_height()
ui_width = screen_width
ui_height = 120
char_width = 60
char_height = 80
tile_size = 20
animation_cooldown = 5
button_width = 200
button_height = 50
blockID = {2: "../Images/Blocks/grass_block_mid.png", 3: "../Images/Blocks/grass_block_left.png",
           4: "../Images/Blocks/grass_block_right.png", 5: "../Images/Blocks/dirt_block_midmid.png",
           6: "../Images/Blocks/dirt_block_midleft.png", 7: "../Images/Blocks/dirt_block_midright.png",
           8: "../Images/Blocks/dirt_block_botmid.png", 9: "../Images/Blocks/dirt_block_botleft.png",
           10: "../Images/Blocks/dirt_block_botright.png", 11: "../Images/Blocks/stone_brick_topright.png",
           12: "../Images/Blocks/stone_brick_midright.png", 13: "../Images/Blocks/stone_brick_botright.png"}
pygame.display.set_caption("Platform game")
icon = pygame.image.load("../Images/sword_icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("../Images/Backgrounds/background_forest.jpg")
clock = pygame.time.Clock()


def load_animations(name, frames, action, slow):
    images = []
    for num in range(0, frames):
        image = pygame.image.load(f"../Images/{name}/{action}/{name}_{action}_{num}.png")
        if (name == "Player" and
                ((action == "Attack1" or action == "Attack2") and num == 2) or (action == "Attack2" and num == 3)):
            image = pygame.transform.scale(image, (char_width * 7 // 3, char_height * 5 // 4))
            size_large = True
        else:
            image = pygame.transform.scale(image, (char_width, char_height))
            size_large = False
        images.append((image, size_large))
        if slow:
            images.append((image, size_large))

    return images


def draw_grid():
    for line in range(0, 40):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
    for line in range(0, 60):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


def read_level_data(file):  # top 6 rows all 0
    data = []
    with open(file, "r") as file:
        for line in file:
            row = line.split(",")
            row[-1] = row[-1].strip()
            ints = [int(item) for item in row]
            data.append(ints)
    file.close()
    return data

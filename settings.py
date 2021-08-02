import pygame


pygame.init()
title_font = pygame.font.SysFont("Calibri", 35)
button_font = pygame.font.SysFont("Calibri", 20)
#text = mmfont.render("quit", True, (255, 255, 255))
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
blockID = {1: "Images/Blocks/grass_block.jpg", 2: "Images/Blocks/dirt_block.jpg", 3: "Images/Blocks/stone_brick1.png",
           4: "Images/Blocks/stone_brick2.png", 5: "Images/Blocks/stone_brick3.png"}
pygame.display.set_caption("Platform game")
icon = pygame.image.load("Images/sword_icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("Images/Backgrounds/background_forest.jpg")
clock = pygame.time.Clock()


def load_animations(name, frames, action, slow):
    images = []
    for num in range(0, frames):
        image = pygame.image.load(f"Images/{name}/{action}/{name}_{action}_{num}.png")
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
            row = []
            for char in line:
                if char != "," and char != "\n":
                    row.append(int(char))
            data.append(row)
    file.close()
    return data

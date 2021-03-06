from PythonFiles.player import *
from PythonFiles.level import *
from PythonFiles.enemy import *


def draw_text(text, font, colour, surface, x, y):
    text = font.render(text, 1, colour)
    textrect = text.get_rect()
    textrect.midtop = (x, y)
    surface.blit(text, textrect)


def main_menu():  # main menu
    running = True
    while running:
        click = False
        screen.blit(background, (0, 0))
        draw_text("Ninja Adventure", title_font, (0, 0, 0), screen, screen_width // 2, 150)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(screen_width // 2 - button_width//2, 300, button_width, button_height)
        button_2 = pygame.Rect(screen_width // 2 - button_width // 2, 400, button_width, button_height)
        button_3 = pygame.Rect(screen_width // 2 - button_width // 2, 500, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        # button 1
        pygame.draw.rect(screen, (0, 70, 0), button_1, border_radius=10)
        if button_1.collidepoint((mx, my)):
            pygame.draw.rect(screen, (0, 100, 0), button_1, border_radius=10)
            if click:
                click = False
                run_game()
        draw_text("Start", button_font, (255, 255, 255), screen, screen_width // 2, 300 + 15)
        # button 2
        pygame.draw.rect(screen, (0, 70, 0), button_2, border_radius=10)
        if button_2.collidepoint((mx, my)):
            pygame.draw.rect(screen, (0, 100, 0), button_2, border_radius=10)
            if click:
                click = False
                pass
        draw_text("Options", button_font, (255, 255, 255), screen, screen_width // 2, 400 + 15)
        # button 3
        pygame.draw.rect(screen, (0, 70, 0), button_3, border_radius=10)
        if button_3.collidepoint((mx, my)):
            pygame.draw.rect(screen, (0, 100, 0), button_3, border_radius=10)
            if click:
                click = False
                running = False
        draw_text("Quit", button_font, (255, 255, 255), screen, screen_width // 2, 500 + 15)

        pygame.display.update()
        clock.tick(60)


def run_game():
    playing = True
    level1a = Level(read_level_data("../LevelTileMaps/level1"), 0, -55)  # level offset by block
    current_level = level1a
    player = Player(600, 300, current_level)
    while playing:
        screen.blit(background, (0, 0))
        current_level.draw(player.xscreen_scroll, player.yscreen_scroll)
        player.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # click once key binds
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player.jump_counter <= 1:
                    player.jump_counter += 1
                    player.y_velocity = -20  # jump height
                    player.jumped = True
                    player.falling = False
                    player.running = False
        pygame.display.update()
        clock.tick(60)


main_menu()

pygame.quit()

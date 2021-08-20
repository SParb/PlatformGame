from settings import *


class Player:
    def __init__(self, x, y, current_level):
        # (number of frames, name, # half speed?)
        self.name = "Player"
        self.current_level = current_level
        self.idle = load_animations(self.name, 4, "Idle", True)
        self.run = load_animations(self.name, 8, "Run", False)
        self.jump = load_animations(self.name, 2, "Jump", True)
        self.fall = load_animations(self.name, 2, "Fall", True)
        self.attack1 = load_animations(self.name, 5, "Attack1", False)
        self.attack2 = load_animations(self.name, 5, "Attack2", False)

        # hitboxes and movement
        self.index = 0
        self.counter = 0
        self.imageID = self.idle[self.index]
        self.image = self.idle[self.index][0]
        self.width = char_width
        self.height = char_height
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # hitbox
        self.rect.x = x
        self.rect.y = y
        self.sword_zone1 = self.rect.inflate(self.width // 3, self.height // 4)  # sword zone infront player
        self.sword_zone1.x = self.rect.x + self.width
        self.sword_zone1.y = self.rect.y - self.height // 4
        self.sword_zone2 = pygame.Rect(0, 0, self.width, self.height * 1 // 4)  # sword zone in player (temp)
        self.sword_zone2.x = self.rect.x
        self.sword_zone2.y = self.rect.y - self.height // 4
        self.y_velocity = 0
        self.look_right = True
        self.jumped = True
        self.jump_counter = 2
        self.falling = True
        self.running = False
        self.attacking = False
        self.attack_first_style = True
        self.start = True
        self.xscreen_scroll = 0
        self.yscreen_scroll = 0

    def next_animation(self):
        if self.attacking:
            if self.attack_first_style:
                self.update_attack_image(self.attack1)
            else:
                self.update_attack_image(self.attack2)
        elif self.falling:
            self.update_image(self.fall)
        elif self.jumped:
            self.update_image(self.jump)
        elif self.running:
            self.update_image(self.run)
        else:
            self.update_image(self.idle)

    def update_image(self, new_image):
        if self.look_right:
            if self.index >= len(new_image):
                self.index = 0
            self.image = new_image[self.index][0]
            self.imageID = new_image[self.index]
        else:
            if self.index >= len(new_image):
                self.index = 0
            self.image = pygame.transform.flip(new_image[self.index][0], True, False)
            self.imageID = new_image[self.index]

    def update_attack_image(self, new_image):
        self.update_image(new_image)
        if self.index >= len(new_image) - 1:
            self.attacking = False
            if self.attack_first_style:
                self.attack_first_style = False
            else:
                self.attack_first_style = True
            self.index = 0

    def update(self):
        dx = 0
        dy = 0
        left, middle, right = pygame.mouse.get_pressed(num_buttons=3)
        self.running = False
        # key presses
        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            dx -= 5
            if not (self.attacking and self.look_right):
                self.look_right = False
                self.sword_zone1.x = self.rect.x - self.width * (4 / 3)
            if not self.jumped and not self.attacking:
                self.running = True

        if key[pygame.K_d]:
            dx += 5
            if not (self.attacking and not self.look_right):
                self.look_right = True
                self.sword_zone1.x = self.rect.x + self.width
            if not self.jumped and not self.attacking:
                self.running = True

        # if key[pygame.K_s]:

        if left and not self.attacking and self.start is False:
            self.index = 0
            self.attacking = True

        if right:
            pass
        if middle:
            pass

        # update animations
        self.counter += 1
        if self.counter > animation_cooldown:
            self.counter = 0
            self.next_animation()
            self.index += 1

        # gravity
        self.y_velocity += 1
        if self.y_velocity > 8:  # gravity strength
            self.y_velocity = 8  # gravity strength
            self.falling = True
        dy += self.y_velocity
        # check collision
        for tile in self.current_level.tile_list:
            # check x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #  check up or down
                if self.y_velocity < 0:  # up
                    dy = tile[1].bottom - self.rect.top
                    self.y_velocity = 0
                elif self.y_velocity >= 0:  # down
                    dy = tile[1].top - self.rect.bottom
                    self.y_velocity = 0
                    self.jumped = False
                    self.falling = False
                    self.jump_counter = 0
                    self.start = False  # Stop any buffered attacks

        # update player position
        self.rect.x += dx
        self.rect.y += dy
        self.sword_zone1.x += dx
        self.sword_zone1.y += dy
        self.sword_zone2.x += dx
        self.sword_zone2.y += dy

        if self.name == "Player":  # scrolling effect
            if self.rect.right > screen_width - x_scroll_thresh or self.rect.left < x_scroll_thresh:
                self.rect.x -= dx
                self.sword_zone1.x -= dx
                self.sword_zone2.x -= dx
                self.xscreen_scroll = -dx
            else:
                self.xscreen_scroll = 0
            if self.rect.bottom > screen_height - y_scroll_thresh or self.rect.top < y_scroll_thresh :
                self.rect.y -= dy
                self.sword_zone1.y -= dy
                self.sword_zone2.y -= dy
                self.yscreen_scroll = -dy
            else:
                self.yscreen_scroll = 0
        #  place image on screen
        if self.imageID[1]:
            if self.look_right:
                screen.blit(self.image, self.sword_zone2)
            else:
                screen.blit(self.image, self.sword_zone1)
        else:
            screen.blit(self.image, self.rect)

        self.hitbox_grid()

    def hitbox_grid(self):
        pygame.draw.rect(screen, (255, 255, 0), self.sword_zone1, 2)
        pygame.draw.rect(screen, (255, 255, 0), self.sword_zone2, 2)
        pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)  # player hit box

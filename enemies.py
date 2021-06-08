import pygame
import random

screen_width = 800
screen_height = 576

# colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

pygame.init()
# block class
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # calls parent class constructor
        pygame.sprite.Sprite.__init__(self)
        # set background color transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
        #draw ellipse
        pygame.draw.ellipse(self.image, color, [0,0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# powerup class
class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        pygame.sprite.Sprite.__init__(self)
        # set the direction
        self.change_x = change_x
        self.change_y = change_y
        # load image for powerup
        self.image = pygame.image.load("powerup_actual.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# enemy class
class Slime(pygame.sprite.Sprite):
    explosion = False
    pygame.display.set_mode((screen_width, screen_height))

    def __init__(self, x, y, change_x, change_y):
        pygame.sprite.Sprite.__init__(self)
        # set the direction
        self.change_x = change_x
        self.change_y = change_y
        # load image for enemy
        self.image = pygame.image.load("slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    # update function for enemies
    def update(self, horizontal_blocks, vertical_blocks):
        if not self.explosion:
            self.rect.x += self.change_x
            self.rect.y += self.change_y
            if self.rect.right < 0:
                self.rect.left = screen_width
            elif self.rect.left > screen_width:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = screen_height
            elif self.rect.top > screen_height:
                self.rect.bottom = 0

            if self.rect.topleft in self.get_intersection_position():
                direction = random.choice(("left", "right", "up", "down"))
                if direction == "left" and self.change_x == 0:
                    self.change_x = -2
                    self.change_y = 0
                elif direction == "right" and self.change_x == 0:
                    self.change_x = 2
                    self.change_y = 0
                elif direction == "up" and self.change_y == 0:
                    self.change_x = 0
                    self.change_y = -2
                elif direction == "down" and self.change_y == 0:
                    self.change_x = 0
                    self.change_y = 2
        # else, enemy has been hit so make the enemy dissapear
        else:
            self.kill()


    def get_intersection_position(self):
        # working with rows in map
        items = []
        for i, row in enumerate(environment()):
            for j,item in enumerate(row):
                if item == 3:
                    items.append((j*32, i*32))
        return items

    # changes the enemy image once pacman picks up a powerup
    def changeImage(self):
        global alt_image
        global rect
        alt_image = pygame.image.load("slime.png").convert_alpha()
        rect = alt_image.get_rect()


# creating game environment
def environment():
    grid = ((0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0))

    return grid


# draws the environment
def draw_environment(screen):
    for i, row in enumerate(environment()):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, blue, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
                pygame.draw.line(screen, blue, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)
            elif item == 2:
                pygame.draw.line(screen, blue, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                pygame.draw.line(screen, blue, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)

# draws the environment when powerup is active
def draw_environmentActive(screen):
    for i, row in enumerate(environment()):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, red, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
                pygame.draw.line(screen, red, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)
            elif item == 2:
                pygame.draw.line(screen, red, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                pygame.draw.line(screen, red, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)
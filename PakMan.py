import sys
import random
import pygame
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Размеры игрового поля
WIDTH = 480
HEIGHT = 360
CELL_SIZE = 24

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pac-Man")

# Загрузка изображений
pacman_image = pygame.image.load("pacman.png").convert_alpha()
ghost_image = pygame.image.load("ghost.png").convert_alpha()
dot_image = pygame.image.load("dot.png").convert_alpha()

# Классы объектов
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pacman_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.speed = CELL_SIZE

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed

        # Ограничиваем перемещение внутри экрана
        self.rect.clamp_ip(screen.get_rect())

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ghost_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice([K_LEFT, K_RIGHT, K_UP, K_DOWN])

    def update(self):
        if self.direction == K_LEFT and self.rect.left > 0:
            self.rect.x -= CELL_SIZE
        elif self.direction == K_RIGHT and self.rect.right < WIDTH:
            self.rect.x += CELL_SIZE
        elif self.direction == K_UP and self.rect.top > 0:
            self.rect.y -= CELL_SIZE
        elif self.direction == K_DOWN and self.rect.bottom < HEIGHT:
            self.rect.y += CELL_SIZE
        else:
            self.direction = random.choice([K_LEFT, K_RIGHT, K_UP, K_DOWN])

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = dot_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Спрайты
player = Player()
ghosts = [
    Ghost(random.randint(0, WIDTH - CELL_SIZE), random.randint(0, HEIGHT - CELL_SIZE)),
    Ghost(random.randint(0, WIDTH - CELL_SIZE), random.randint(0, HEIGHT - CELL_SIZE)),
    Ghost(random.randint(0, WIDTH - CELL_SIZE), random.randint(0, HEIGHT - CELL_SIZE))
]
dots = [
    Dot(x, y) for x in range(0, WIDTH, CELL_SIZE) for y in range(0, HEIGHT, CELL_SIZE)
]

all_sprites = pygame.sprite.Group(player, *ghosts, *dots)

# Основная игра
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Проверка столкновений
    eaten_dots = pygame.sprite.spritecollide(player, dots, True)
    if eaten_dots:
        print(f"Осталось точек: {len(dots)}")

    collisions = pygame.sprite.spritecollideany(player, ghosts)
    if collisions:
        print("Вы проиграли!")
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
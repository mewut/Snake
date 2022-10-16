import pygame
from pygame.math import Vector2
import time
import random
import sys

snake_speed = 20

FRAME_COLOR = (69, 139, 116)  # aquamarine4
WHITE = (240, 248, 255)  # aliceblue
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10), Vector2(2, 10)]
        self.dir = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * BLOCK_SIZE, block.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, BLACK, block_rect)

    # когда змейка ползет, она не ползет, а как бы появляется и исчезает.
    # игрок управляет только головой.
    # остальные блоки появляются и исчезают на месте головы, которая появляется с определенной скоростью.

    def move_snake(self):
        if self.new_block is True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.dir)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.dir)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Apple:
    def __init__(self):
        self.x = random.randint(0, BLOCK_NUMBER - 1)
        self.y = random.randint(0, BLOCK_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
        self.randomize()

    def draw_apple(self):
        apple_rect = pygame.Rect(self.pos.x * BLOCK_SIZE, self.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, apple_rect)

    def randomize(self):
        self.x = random.randint(0, BLOCK_NUMBER - 1)
        self.y = random.randint(0, BLOCK_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_game_over()

    def draw_all(self):
        self.apple.draw_apple()
        self.snake.draw_snake()
        self.score()

    def check_collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.apple.pos:
                self.apple.randomize()      # если яблочко появляется в теле змейки, то пусть появится еще раз))

    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < BLOCK_NUMBER or not 0 <= self.snake.body[0].y < BLOCK_NUMBER:
            self.game_over()
            # буквально: проверяем голову змейки, находится ли они между нулем и количеством клеток поля.
            # Если нет, значит, врезалась
            # У меня 50 клеточек. Но <= нельзя, иначе змейка высовывает голову за поле
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                # если блоки змейки, находящиеся после ее головы - это [1:] - как бы равняются с другими блоками змейки
                # то произошел самокусь и мы проиграли

    def game_over(self):
        score_text = len(self.snake.body) - 4
        print('Ваш счет: ' + str(score_text), True, RED)

    def score(self):
        score_text = str(len(self.snake.body) - 4)
        score_surface = font.render('Счет : ' + str(score_text), True, WHITE)
        score_x = int(BLOCK_SIZE * BLOCK_NUMBER - 60)
        score_y = int(BLOCK_SIZE * BLOCK_NUMBER - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)
        pygame.draw.rect(screen, (167, 209, 61), score_rect)
        pygame.draw.rect(screen, (56, 74, 12), score_rect, 2)


pygame.init()

BLOCK_SIZE = 15
BLOCK_NUMBER = 50
pygame.display.set_caption('Змейка')
screen = pygame.display.set_mode((BLOCK_SIZE * BLOCK_NUMBER, BLOCK_SIZE * BLOCK_NUMBER))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150) # в МИЛИСЕКУНДАХ!

main_game = Game()

while True:
    # чтобы закрывать на крестик
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
            # управление.
            # if внутри проверяет движение змейки в саму себя и не дает этому случиться
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.dir.y != 1:
                    main_game.snake.dir = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.dir.x != -1:
                    main_game.snake.dir = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.dir.y != -1:
                    main_game.snake.dir = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.dir.x != 1:
                    main_game.snake.dir = Vector2(-1, 0)

    screen.fill(FRAME_COLOR)
    main_game.draw_all()
    pygame.display.update()
    clock.tick(60)

# шпаргалка:
# v = Vector2(5, 4)               Is = [5, 4]
# v.x -> 5                        Is[0] -> 5
# v.y -> 4                        Is[1] -> 4

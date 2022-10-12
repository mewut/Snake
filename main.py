import pygame
from pygame.math import Vector2
import time
import random
import sys
from enum import Enum

snake_speed = 20

FRAME_COLOR = (69, 139, 116)  # aquamarine4
WHITE = (240, 248, 255)  # aliceblue
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class SnakeDirection(Enum):
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    DOWN = 'DOWN'
    UP = 'UP'


class Snake:
    def __init__(self):
        # количество блоков в змейке
        # выделить голову цветом
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10), Vector2(2, 10)]
        self.dir = Vector2(0, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * BLOCK_SIZE, block.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, BLACK, block_rect)

    # когда змейка ползет, она не ползет, а как бы появляется и исчезает.
    # игрок управляет только головой.
    # остальные блоки появляются и исчезают на месте головы, которая появляется с определенной скоростью.

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.dir)
        self.body = body_copy[:]


class Apple:
    def __init__(self):
        self.randomize()

    def draw_apple(self):
        apple_rect = pygame.Rect(self.pos.x * BLOCK_SIZE, self.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, apple_rect)

    def randomize(self):
        self.x = random.randint(0, BLOCK_NUMBER - 1)
        self.y = random.randint(0, BLOCK_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


pygame.init()


BLOCK_SIZE = 15
BLOCK_NUMBER = 50

pygame.display.set_caption('Змейка')
screen = pygame.display.set_mode((BLOCK_SIZE * BLOCK_NUMBER, BLOCK_SIZE * BLOCK_NUMBER))
clock = pygame.time.Clock()

apple = Apple()
snake = Snake()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150) # в МИЛИСЕКУНДАХ!

while True:
    # чтобы закрывать на крестик
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
            # управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.dir = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                snake.dir = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                snake.dir = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                snake.dir = Vector2(-1, 0)

    screen.fill(FRAME_COLOR)
    apple.draw_apple()
    snake.draw_snake()
    pygame.display.update()
    clock.tick(60)

score = 0

# это пока не работает
class Score:
    def __init__(self, color, font, size) -> None:
        # считаем
        score_font = pygame.font.SysFont(font, size)
        # показываем
        # ДОДЕЛАТЬ! А то не показываем
        score_surface = score_font.render('Счет : ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        screen.blit(score_surface, score_rect)
        pygame.draw.rect(screen, (167, 209, 61), score_rect)
        pygame.draw.rect(screen, (56, 74, 12), score_rect, 2)

    # и это
    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render(
            'Ваш счет: ' + str(score), True, RED)

        game_over_rect = game_over_surface.get_rect()

        # расположение текста
        game_over_rect.midtop = ((200, 50))
        screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        time.sleep(2)
        pygame.quit()
        quit()




#             # старое управление
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 snake.turn_up()
#             if event.key == pygame.K_DOWN:
#                 snake.turn_down()
#             if event.key == pygame.K_LEFT:
#                 snake.turn_left()
#             if event.key == pygame.K_RIGHT:
#                 snake.turn_right()
#
#     # проверка на диагональное движение
#     if change_to == 'UP' and direction != 'DOWN':
#         direction = 'UP'
#     if change_to == 'DOWN' and direction != 'UP':
#         direction = 'DOWN'
#     if change_to == 'LEFT' and direction != 'RIGHT':
#         direction = 'LEFT'
#     if change_to == 'RIGHT' and direction != 'LEFT':
#         direction = 'RIGHT'
#
#     # позлем!
#     if direction == 'UP':
#         snake_position[1] -= 10
#     if direction == 'DOWN':
#         snake_position[1] += 10
#     if direction == 'LEFT':
#         snake_position[0] -= 10
#     if direction == 'RIGHT':
#         snake_position[0] += 10
#         # TO DO
#     # тело змейки удлинняется, когда она ест. Очки начисляются за яблочки
#     snake_body.insert(0, list(snake_position))
#     if snake_position[0] == apple.x and snake_position[1] == apple.y:
#         score += 10
#         apple.respawn()
#     else:
#         snake_body.pop()
#
#
#


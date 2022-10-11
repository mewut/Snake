import pygame
import time
import random

from enum import Enum

snake_speed = 10

BLOCK_SIZE = 10
SIZE_BLOCK = 20  # размер квадратиков внутри
COUNT_BLOCK = 29    # рисуем поле
FRAME_COLOR = (69, 139, 116)  # aquamarine4
WHITE = (240, 248, 255)  # aliceblue
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# размер экрана
x = 800
y = 600
screen = [800, 600]

pygame.init()

pygame.display.set_caption('Змейка')
game = pygame.display.set_mode(screen)

fps = pygame.time.Clock()

# чтобы змейка спавнилась слева в центре. Она сразу начинает ползти. А если спавн будет здесь, то игрок успеет сориентироваться
snake_position = [50, 300]
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]

apple_colour = RED
direction = 'RIGHT'
change_to = direction

score = 0


class SnakeDirection(Enum):
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    DOWN = 'DOWN'
    UP = 'UP'


class Snake:
    SNAKE_COLOR: str = BLACK
    HEAD_COLOR: str = RED

    @property
    def moving_right(self):
        return self.moving_direction == SnakeDirection.RIGHT

    @property
    def moving_left(self):
        return self.moving_direction == SnakeDirection.LEFT
    
    @property
    def moving_down(self):
        return self.moving_direction == SnakeDirection.DOWN

    @property
    def moving_up(self):
        return self.moving_direction == SnakeDirection.UP

    def __init__(self, speed: int) -> None:
        # количество блоко в змейке не считая головы
        self.blocks_count = 4
        self.x = x // 2
        self.y = y // 2
        self.velocity = speed
        self.moving_direction = SnakeDirection.UP
    
    def draw(self):
        pygame.draw.rect(game, self.HEAD_COLOR, pygame.Rect(self.x, self.y, 10, 10))

        for i in range(self.blocks_count):
            blocks_delta = i + 1
            
            if self.moving_right:
                pygame.draw.rect(game, self.SNAKE_COLOR, pygame.Rect(
                    self.x - BLOCK_SIZE * blocks_delta,
                    self.y,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                ))
            elif self.moving_left:
                pygame.draw.rect(game, self.SNAKE_COLOR, pygame.Rect(
                    self.x + BLOCK_SIZE * blocks_delta,
                    self.y,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                ))
            elif self.moving_down:
                pygame.draw.rect(game, self.SNAKE_COLOR, pygame.Rect(
                    self.x,
                    self.y - BLOCK_SIZE * blocks_delta,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                ))
            elif self.moving_up:
                pygame.draw.rect(game, self.SNAKE_COLOR, pygame.Rect(
                    self.x,
                    self.y + BLOCK_SIZE * blocks_delta,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                ))

    def move_right(self):
        self.x += self.velocity
    
    def move_left(self):
        self.x -= self.velocity
    
    def move_up(self):
        self.y -= self.velocity

    def move_down(self):
        self.y += self.velocity

    def move(self):
        if self.moving_down:
            self.move_down()
        elif self.moving_up:
            self.move_up()
        elif self.moving_left:
            self.move_left()
        elif self.moving_right:
            self.move_right()

    def turn_right(self):
        self.moving_direction = SnakeDirection.RIGHT
    
    def turn_left(self):
        self.moving_direction = SnakeDirection.LEFT
    
    def turn_down(self):
        self.moving_direction = SnakeDirection.DOWN
    
    def turn_up(self):
        self.moving_direction = SnakeDirection.UP
        

class Apple:
    APPLE_COLOR: str = RED

    def __init__(self):
        self.x = 50
        self.y = 50
    
    def respawn(self):
        self.x = random.randint(0, x)
        self.y = random.randint(0, y)
    
    def draw(self):
        pygame.draw.rect(game, self.APPLE_COLOR, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))


def show_score(choice, color, font, size):
    # считаем
    score_font = pygame.font.SysFont(font, size)
    # показываем
    score_surface = score_font.render('Счет : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game.blit(score_surface, score_rect)


def game_over():
    # еще сюда красоты
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(
        'Ваш счет: ' + str(score), True, RED)

    game_over_rect = game_over_surface.get_rect()

    # расположение текста
    game_over_rect.midtop = (x / 2, y / 4)
    game.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(2)
    pygame.quit()
    quit()


apple = Apple()
snake = Snake(snake_speed)


while True:
    # чтобы закрывать на крестик

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
        # управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.turn_up()
            if event.key == pygame.K_DOWN:
                snake.turn_down()
            if event.key == pygame.K_LEFT:
                snake.turn_left()
            if event.key == pygame.K_RIGHT:
                snake.turn_right()

    # проверка на диагональное движение
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # позлем!
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
        # TO DO
    # тело змейки удлинняется, когда она ест. Очки начисляются за яблочки
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == apple.x and snake_position[1] == apple.y:
        score += 10
        apple.respawn()
    else:
        snake_body.pop()

    apple_spawn = True
    game.fill(FRAME_COLOR)

    # Поле
    for row in range(COUNT_BLOCK):
        for column in range(COUNT_BLOCK):
            pygame.draw.rect(game, WHITE, [10 + column * SIZE_BLOCK, 10 + row * SIZE_BLOCK, SIZE_BLOCK, SIZE_BLOCK])

    apple.draw()
    snake.draw()
    snake.move()

    # показываем очки, пока едим
    show_score(1, WHITE, 'times new roman', 20)
    pygame.display.update()
    fps.tick(snake_speed)








# ФАК


# # размеры экрана
# res = 700
# res = res // size // 2 * 2 * size      # чтобы нормально спавнилась в центре
#
# clock = pygame.time.Clock()
# screen = pygame.display.set_mode((res, res))
#
# snake_start = res // 2 - half_size
# length = 4
# dir_x, dir_y = 0, size    # движение змейки по двум осям
# snake = [(snake_start, snake_start)]
# apple = (random.randrange(0, res - size, size), random.randrange(0, res - size, size))
#
#
#
#     [pygame.draw.rect(screen, (0, 160, 0), (x, y, size, size)) for x, y in snake]
#     pygame.draw.circle(screen, (160, 0, 0), (apple[0] + half_size, apple[1] + half_size), half_size)
#
#     body_x = snake[-1][0] + dir_x
#     body_y = snake[-1][0] + dir_y
#     snake.append((body_x, body_y))
#
#     key = pygame.key.get_pressed()
#     if key[pygame.K_w]:
#         dir_x, dir_y = 0, -size
#     elif key[pygame.K_a]:
#         dir_x, dir_y = -size, 0
#     elif key[pygame.K_s]:
#         dir_x, dir_y = 0, size
#     elif key[pygame.K_d]:
#         dir_x, dir_y = size, 0
#
#     clock.tick(12)
#     pygame.display.flip()

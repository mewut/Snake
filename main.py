import pygame
import time
import random

snake_speed = 15

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
              [70, 50]
              ]

apple_position = [random.randrange(1, (x // 10)) * 10,
                  random.randrange(1, (y // 10)) * 10]

apple_spawn = True
apple_colour = RED


direction = 'RIGHT'
change_to = direction

score = 0


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


while True:
    # чтобы закрывать на крестик
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
        # управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

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
    if snake_position[0] == apple_position[0] and snake_position[1] == apple_position[1]:
        score += 10
        apple_spawn = False   # может, убрать?
    else:
        snake_body.pop()

    if not apple_spawn:
        apple_position = [random.randrange(1, (x // 10)) * 10,
                          random.randrange(1, (y // 10)) * 10]

    apple_spawn = True
    game.fill(FRAME_COLOR)

    for row in range(COUNT_BLOCK):
        for column in range(COUNT_BLOCK):
            pygame.draw.rect(game, WHITE, [10 + column * SIZE_BLOCK, 10 + row * SIZE_BLOCK, SIZE_BLOCK, SIZE_BLOCK])

    for pos in snake_body:
        pygame.draw.rect(game, BLACK,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game, RED, pygame.Rect(
        snake_position[0], snake_position[1], 10, 10))

    # Game Over
    if snake_position[0] < 0 or snake_position[0] > x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > y - 10:
        game_over()

    # когда змейка кусает себя
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

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

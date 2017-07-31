import pygame
import sys
import random
from pygame.locals import *

FPS = 15

BOARD_WIDTH = 25
BOARD_HEIGHT = 35
CELL_SIZE = 20
GAP_SIZE = 1
BORDER_SIZE = 5
WINDOW_WIDTH = (BORDER_SIZE * 2) + (BOARD_WIDTH * (CELL_SIZE + GAP_SIZE))
WINDOW_HEIGHT = (BORDER_SIZE * 2) + (BOARD_HEIGHT * (CELL_SIZE + GAP_SIZE))
SNAKE_START_SIZE = 5
assert SNAKE_START_SIZE <= BOARD_HEIGHT // 2, "The snake won't fit on the board"
SNAKE_START_ROW = BOARD_HEIGHT // 2
SNAKE_START_CELL = BOARD_WIDTH // 2

BORDER = (
    (0, 0, WINDOW_WIDTH, BORDER_SIZE),
    (0, 0, BORDER_SIZE, WINDOW_HEIGHT),
    (0, WINDOW_HEIGHT - BORDER_SIZE, WINDOW_WIDTH, BORDER_SIZE),
    (WINDOW_WIDTH - BORDER_SIZE, 0, BORDER_SIZE, WINDOW_HEIGHT)
)

WRAP = False

CELL_LOCATION_GRID = [
    [((x * (GAP_SIZE + CELL_SIZE)) + BORDER_SIZE, (y * (GAP_SIZE + CELL_SIZE)) + BORDER_SIZE)
     for x in range(BOARD_WIDTH)]
    for y in range(BOARD_HEIGHT)
]

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_COLOR = BLACK
BORDER_COLOR = GRAY
SNAKE_COLOR = GREEN
PELLET_COLOR = RED


def main():
    global DISPLAY_SURFACE, FPS_CLOCK
    pygame.init()

    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")

    direction = UP
    snake = []
    for i in range(SNAKE_START_SIZE):
        snake.append((SNAKE_START_ROW + i, SNAKE_START_CELL))

    pellet = get_random_unoccupied_cell(snake)

    while True:

        DISPLAY_SURFACE.fill(BG_COLOR)

        # Draw the border
        for side in BORDER:
            pygame.draw.rect(DISPLAY_SURFACE, BORDER_COLOR, side)
        # Draw the pellet
        pygame.draw.circle(
            DISPLAY_SURFACE, RED,
            (CELL_LOCATION_GRID[pellet[0]][pellet[1]][0] + CELL_SIZE // 2,
             CELL_LOCATION_GRID[pellet[0]][pellet[1]][1] + CELL_SIZE // 2,),
            CELL_SIZE // 2
        )
        # Draw the snake
        for row, cell in snake:
            cell_rect = CELL_LOCATION_GRID[row][cell] + (CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(DISPLAY_SURFACE, SNAKE_COLOR, cell_rect)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[K_UP] or keys[K_w]) and direction != DOWN:
            direction = UP
        elif (keys[K_DOWN] or keys[K_s]) and direction != UP:
            direction = DOWN
        elif (keys[K_LEFT] or keys[K_a]) and direction != RIGHT:
            direction = LEFT
        elif (keys[K_RIGHT] or keys[K_d]) and direction != LEFT:
            direction = RIGHT

        snake = move_snake(snake, direction)
        snake_head = snake[0]
        if snake_head == pellet:
            pellet = get_random_unoccupied_cell(snake)
        else:
            del snake[len(snake) - 1]
        # print('pellet', pellet)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def move_snake(snake, direction):
    """Moves the snake in the specified direction."""
    ROW = 0
    COLUMN = 1

    TOP_ROW = 0
    BOTTOM_ROW = BOARD_HEIGHT - 1
    LEFT_COLUMN = 0
    RIGHT_COLUMN = BOARD_WIDTH - 1

    snake_head = snake[0]
    snake_body = snake[1:]
    if direction == UP:
        if snake_head[ROW] == TOP_ROW:
            return die()
        else:
            snake.insert(0, (snake_head[ROW] - 1, snake_head[COLUMN]))
    elif direction == DOWN:
        if snake_head[ROW] == BOTTOM_ROW:
            return die()
        else:
            snake.insert(0, (snake_head[ROW] + 1, snake_head[COLUMN]))
    elif direction == LEFT:
        if snake_head[COLUMN] == LEFT_COLUMN:
            return die()
        else:
            snake.insert(0, (snake_head[ROW], snake_head[COLUMN] - 1))
    elif direction == RIGHT:
        if snake_head[COLUMN] == RIGHT_COLUMN:
            return die()
        else:
            snake.insert(0, (snake_head[ROW], snake_head[COLUMN] + 1))
    if snake_head in snake_body:
        return die()

    return snake


def die():
    # restart game for now
    snake = []
    for i in range(SNAKE_START_SIZE):
        snake.append((SNAKE_START_ROW + i, SNAKE_START_CELL))
    return snake


def get_random_unoccupied_cell(snake):
    board = [list(range(BOARD_WIDTH)) for row in range(BOARD_HEIGHT)]
    for row, cell in snake:
        index = board[row].index(cell)
        del board[row][index]
    # collapse board into a 1-dimensional list
    board = [(row, cell) for row in range(len(board)) for cell in board[row]]
    return random.choice(board)


if __name__ == "__main__":
    main()

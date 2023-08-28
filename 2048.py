# 2048
# Aleksis Vanags
# 23/08/2023 - 25/08/2023

import pygame
from random import randint as r

pygame.init()
pygame.font.init()

WIDTH = 400
HEIGHT = 400
ROWS = 4
COLS = 4
SQUARE_SIZE = HEIGHT//ROWS
WHITE = (255, 255, 255)
OFFWHITE = (250,240,230)
BLACK = (0, 0, 0)
COLOUR_2 = (255, 109, 0)
COLOUR_4 = (255, 121, 0)
COLOUR_8 = (255, 133, 0)
COLOUR_16 = (255, 145, 0)
COLOUR_32 = (255, 158, 0)
COLOUR_64 = (36, 0, 70)
COLOUR_128 = (60, 9, 108)
COLOUR_256 = (90, 24, 154)
COLOUR_512 = (123, 44, 191)
COLOUR_1024 = (157, 78, 221)
COLOUR_2048 = (255,215,0)
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("2048")

font = pygame.font.SysFont("Consolas", 32, False, False)
smallFont = pygame.font.SysFont("Consolas", 24, False, False)
grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]


def DrawSquares(win):
    win.fill(BLACK)

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 0:
                COLOUR = WHITE
            elif grid[r][c] == 2:
                COLOUR = COLOUR_2
            elif grid[r][c] == 4:
                COLOUR = COLOUR_4
            elif grid[r][c] == 8:
                COLOUR = COLOUR_8
            elif grid[r][c] == 16:
                COLOUR = COLOUR_16
            elif grid[r][c] == 32:
                COLOUR = COLOUR_32
            elif grid[r][c] == 64:
                COLOUR = COLOUR_64
            elif grid[r][c] == 128:
                COLOUR = COLOUR_128
            elif grid[r][c] == 256:
                COLOUR = COLOUR_256
            elif grid[r][c] == 512:
                COLOUR = COLOUR_512
            elif grid[r][c] == 1024:
                COLOUR = COLOUR_1024
            else:
                COLOUR = COLOUR_2048

            pygame.draw.rect(win, COLOUR, (r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            text = font.render(str(grid[r][c]), True, WHITE, COLOUR)
            textRect = text.get_rect()
            textRect.center = ((r * SQUARE_SIZE) + (SQUARE_SIZE // 2), (c * SQUARE_SIZE) + (SQUARE_SIZE // 2))

            pygame.draw.rect(win, OFFWHITE, ((r * SQUARE_SIZE) - 1, 0, 2, HEIGHT))
            pygame.draw.rect(win, OFFWHITE, (0, (c * SQUARE_SIZE) - 1, WIDTH, 2))

            win.blit(text, textRect)


def ClearGrid():
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = 0

    return grid


def RandomCell():
    rRow = r(0, ROWS - 1)
    rCol = r(0, COLS - 1)

    try:
        if grid[rRow][rCol] != 0:
            RandomCell()
        else:
            rInt = r(0, 9)

            if rInt == 0:
                grid[rRow][rCol] = 4
            else:
                grid[rRow][rCol] = 2
    except RecursionError:
        pass


def Compress(direction):
    if direction == "a":
        for r in range(ROWS - 1, 0, -1):
            for c in range(0, COLS):
                if grid[r][c] != 0 and grid[r-1][c] == 0:
                    grid[r-1][c] = grid[r][c]
                    grid[r][c] = 0
    elif direction == "w":
        for r in range(0, ROWS):
            for c in range(COLS - 1, 0, -1):
                if grid[r][c] != 0 and grid[r][c-1] == 0:
                    grid[r][c-1] = grid[r][c]
                    grid[r][c] = 0
    elif direction == "d":
        for r in range(0, ROWS - 1):
            for c in range(0, COLS):
                if grid[r][c] != 0 and grid[r+1][c] == 0:
                    grid[r+1][c] = grid[r][c]
                    grid[r][c] = 0
    elif direction == "s":
        for r in range(0, ROWS):
            for c in range(0, COLS - 1):
                if grid[r][c] != 0 and grid[r][c+1] == 0:
                    grid[r][c+1] = grid[r][c]
                    grid[r][c] = 0


def Combine(direction):
    if direction == "a":
        for r in range(1, ROWS):
            for c in range(0, COLS):
                if grid[r][c] != 0 and grid[r][c] == grid[r-1][c]:
                    grid[r-1][c] *= 2
                    grid[r][c] = 0
    elif direction == "w":
        for r in range(0, ROWS):
            for c in range(1, COLS):
                if grid[r][c] != 0 and grid[r][c] == grid[r][c-1]:
                    grid[r][c-1] *= 2
                    grid[r][c] = 0
    elif direction == "d":
        for r in range(ROWS - 2, -1, -1):
            for c in range(0, COLS):
                if grid[r][c] != 0 and grid[r][c] == grid[r+1][c]:
                    grid[r+1][c] *= 2
                    grid[r][c] = 0
    elif direction == "s":
        for r in range(0, ROWS):
            for c in range(COLS - 2, -1, -1):
                if grid[r][c] != 0 and grid[r][c] == grid[r][c+1]:
                    grid[r][c+1] *= 2
                    grid[r][c] = 0


def Turn(direction, tried):
    tempGrid = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

    for r in range(ROWS):
        for c in range(COLS):
            tempGrid[r][c] = grid[r][c]

    for _ in range(3):
        Compress(direction)

    Combine(direction)
    Compress(direction)

    if grid == tempGrid:
        if direction == "a":
            tried[0] = 1
        elif direction == "w":
            tried[1] = 1
        elif direction == "d":
            tried[2] = 1
        else:
            tried[3] = 1
    else:
        tried = [0, 0, 0, 0]

        RandomCell()

    return tried


def main():
    run = True
    clock = pygame.time.Clock()
    grid = ClearGrid()
    tried = [0, 0, 0, 0]

    for _ in range(2):
        RandomCell()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    tried = Turn("w", tried)
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    tried = Turn("a", tried)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    tried = Turn("s", tried)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    tried = Turn("d", tried)
                elif event.key == pygame.K_r:
                    main()

        DrawSquares(WIN)

        if tried == [1, 1, 1, 1]:
            score = 0
            for r in range(ROWS):
                for c in range(COLS):
                    score += grid[r][c]

            gameOverText = font.render("GAME OVER", True, BLACK, WHITE)
            scoreText = smallFont.render("Score: " + str(score), True, BLACK, WHITE)
            resetText = font.render("Press 'r' to Reset", True, BLACK, WHITE)
            gameOverTextRect = gameOverText.get_rect()
            scoreTextRect = scoreText.get_rect()
            resetTextRect = resetText.get_rect()
            gameOverTextRect.center = (WIDTH // 2, HEIGHT // 3)
            scoreTextRect.center = (WIDTH // 2, HEIGHT // 2)
            resetTextRect.center = (WIDTH // 2, HEIGHT // (3 / 2))
            gameOverScreenFade = pygame.Surface((WIDTH, HEIGHT))

            gameOverScreenFade.fill((255, 255, 255))
            gameOverScreenFade.set_alpha(160)
            gameOverScreenFade.blit(gameOverText, gameOverTextRect)
            gameOverScreenFade.blit(scoreText, scoreTextRect)
            gameOverScreenFade.blit(resetText, resetTextRect)
            WIN.blit(gameOverScreenFade, (0, 0))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

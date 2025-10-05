import pygame
import sys

pygame.init()

# --- Налаштування ---
WIDTH, HEIGHT = 400, 500
LINE_WIDTH = 5
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 10
SPACE = 40
BG_COLOR = (245, 245, 245)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (66, 135, 245)
CROSS_COLOR = (239, 83, 80)

# --- Екран ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.SysFont(None, 40)

# --- Звуки ---
try:
    click_sound = pygame.mixer.Sound("click.wav")
    win_sound = pygame.mixer.Sound("win.wav")
except:
    click_sound = None
    win_sound = None

# --- Змінні ---
board = [[None for _ in range(COLS)] for _ in range(ROWS)]
player = "X"
score_X = 0
score_O = 0
game_over = False

# --- Функції ---
def draw_lines():
    screen.fill(BG_COLOR)
    # Вертикальні
    for col in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 100), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # Горизонтальні
    for row in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, 100 + row * SQUARE_SIZE), (WIDTH, 100 + row * SQUARE_SIZE), LINE_WIDTH)

def draw_score():
    score_text = font.render(f"X: {score_X}  |  O: {score_O}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 30))

def animate_X(row, col):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = 100 + row * SQUARE_SIZE + SQUARE_SIZE // 2
    for i in range(0, SQUARE_SIZE//2, 8):
        pygame.draw.line(screen, CROSS_COLOR, (x - i, y - i), (x + i, y + i), CROSS_WIDTH)
        pygame.display.update()
        pygame.time.delay(20)
    for i in range(0, SQUARE_SIZE//2, 8):
        pygame.draw.line(screen, CROSS_COLOR, (x - i, y + i), (x + i, y - i), CROSS_WIDTH)
        pygame.display.update()
        pygame.time.delay(20)

def animate_O(row, col):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = 100 + row * SQUARE_SIZE + SQUARE_SIZE // 2
    for r in range(10, CIRCLE_RADIUS + 1, 5):
        pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), r, CIRCLE_WIDTH)
        pygame.display.update()
        pygame.time.delay(20)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    100 + row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = 100 + row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(screen, CROSS_COLOR, (x - SPACE, y - SPACE), (x + SPACE, y + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (x - SPACE, y + SPACE), (x + SPACE, y - SPACE), CROSS_WIDTH)

def check_win(player):
    # Рядки
    for row in board:
        if row.count(player) == COLS:
            return True
    # Колонки
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return True
    # Діагоналі
    if all(board[i][i] == player for i in range(COLS)) or all(board[i][COLS - i - 1] == player for i in range(COLS)):
        return True
    return False

def restart():
    global board, player, game_over
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    player = "X"
    game_over = False
    draw_lines()
    draw_score()

# --- Основний цикл ---
draw_lines()
draw_score()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            if mouseY > 100:
                clicked_row = (mouseY - 100) // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    if click_sound: click_sound.play()

                    # Анімація
                    if player == "X":
                        animate_X(clicked_row, clicked_col)
                    else:
                        animate_O(clicked_row, clicked_col)

                    if check_win(player):
                        if win_sound: win_sound.play()
                        if player == "X":
                            score_X += 1
                        else:
                            score_O += 1
                        game_over = True

                    player = "O" if player == "X" else "X"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    pygame.display.update()

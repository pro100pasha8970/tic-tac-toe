import pygame
import sys
import random
import time

pygame.init()

# --- Налаштування ---
WIDTH, HEIGHT = 600, 700
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Кольори
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
TEXT_COLOR = (255, 255, 255)
WIN_LINE_COLOR = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

font = pygame.font.SysFont("comicsans", 50)
small_font = pygame.font.SysFont("comicsans", 30)

# --- Логіка гри ---
board = [[0]*BOARD_COLS for _ in range(BOARD_ROWS)]
player = 1
game_over = False
winner_player = None
mode = None  # 1: PvP, 2: PvE, 3: EvP, 4: EvE
score = {"X": 0, "O": 0}
win_line = None

# --- Функції ---
def draw_lines():
    screen.fill(BG_COLOR)
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i*SQUARE_SIZE), (WIDTH, i*SQUARE_SIZE), LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, WIDTH), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE//2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return all(board[row][col] != 0 for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def check_win(player):
    global win_line
    # Колонки
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            win_line = ((col*SQUARE_SIZE + SQUARE_SIZE//2, 0), (col*SQUARE_SIZE + SQUARE_SIZE//2, WIDTH))
            return True
    # Рядки
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            win_line = ((0, row*SQUARE_SIZE + SQUARE_SIZE//2), (WIDTH, row*SQUARE_SIZE + SQUARE_SIZE//2))
            return True
    # Діагоналі
    if board[0][0] == board[1][1] == board[2][2] == player:
        win_line = ((0, 0), (WIDTH, WIDTH))
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        win_line = ((0, WIDTH), (WIDTH, 0))
        return True
    return False

def draw_win_line():
    if win_line:
        pygame.draw.line(screen, WIN_LINE_COLOR, win_line[0], win_line[1], 10)

def restart():
    global board, player, game_over, win_line, winner_player
    board = [[0]*BOARD_COLS for _ in range(BOARD_ROWS)]
    player = 1
    game_over = False
    winner_player = None
    win_line = None
    draw_lines()

def ai_move():
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        mark_square(r, c, player)
        return r, c
    return None

def draw_text_center(text, size, y, color=TEXT_COLOR):
    font_ = pygame.font.SysFont("comicsans", size)
    render = font_.render(text, True, color)
    rect = render.get_rect(center=(WIDTH//2, y))
    screen.blit(render, rect)

def draw_menu():
    screen.fill(BG_COLOR)
    draw_text_center("TIC TAC TOE", 70, 100)
    modes = ["1. Player vs Player", "2. Player vs Bot", "3. Bot vs Player", "4. Bot vs Bot"]
    buttons = []
    for i, text in enumerate(modes):
        rect = pygame.Rect(WIDTH//2 - 200, 200 + i*100, 400, 60)
        pygame.draw.rect(screen, LINE_COLOR, rect, border_radius=15)
        txt = small_font.render(text, True, TEXT_COLOR)
        screen.blit(txt, (rect.x + 50, rect.y + 15))
        buttons.append((rect, i+1))
    pygame.display.update()
    return buttons

def draw_score():
    text = small_font.render(f"Score  X: {score['X']}  |  O: {score['O']}", True, TEXT_COLOR)
    screen.blit(text, (20, WIDTH + 20))

# --- Головний цикл ---
menu_buttons = draw_menu()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if mode is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, m in menu_buttons:
                    if rect.collidepoint(pos):
                        mode = m
                        restart()
        else:
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if mouseY < WIDTH:
                        clicked_row = int(mouseY // SQUARE_SIZE)
                        clicked_col = int(mouseX // SQUARE_SIZE)
                        if available_square(clicked_row, clicked_col):
                            if (mode == 1) or \
                               (mode == 2 and player == 1) or \
                               (mode == 3 and player == 2):
                                mark_square(clicked_row, clicked_col, player)
                                if check_win(player):
                                    game_over = True
                                    winner_player = player
                                    score["X" if player == 1 else "O"] += 1
                                elif is_board_full():  # --- ДОДАНО НІЧИЮ ---
                                    game_over = True
                                    winner_player = 0
                                player = player % 2 + 1

    # Ходи бота
    if mode and not game_over:
        if (mode == 2 and player == 2) or \
           (mode == 3 and player == 1) or \
           (mode == 4):
            pygame.display.update()
            time.sleep(0.5)
            move = ai_move()
            if move and check_win(player):
                game_over = True
                winner_player = player
                score["X" if player == 1 else "O"] += 1
            elif is_board_full():  # --- ДОДАНО НІЧИЮ ---
                game_over = True
                winner_player = 0
            player = player % 2 + 1

    if mode:
        draw_lines()
        draw_figures()
        draw_score()

        if game_over:
            if winner_player == 0:
                draw_text_center("НІЧИЯ!", 60, HEIGHT//2)
            else:
                if mode == 1:
                    winner_name = "Гравець X" if winner_player == 1 else "Гравець O"
                elif mode == 2:
                    winner_name = "Гравець" if winner_player == 1 else "Бот"
                elif mode == 3:
                    winner_name = "Бот" if winner_player == 1 else "Гравець"
                elif mode == 4:
                    winner_name = "Бот X" if winner_player == 1 else "Бот O"
                draw_win_line()
                draw_text_center(f"{winner_name} виграв!", 50, HEIGHT//2)


            draw_text_center("Press SPACE to Restart", 30, HEIGHT//2 + 60)
            draw_text_center("Press ESC for Menu", 25, HEIGHT - 40)

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if game_over and keys[pygame.K_SPACE]:
            restart()
        if keys[pygame.K_ESCAPE]:
            mode = None
            menu_buttons = draw_menu()

    clock.tick(30)

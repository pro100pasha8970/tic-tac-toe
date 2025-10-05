import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 3
MARGIN = 40
BOARD_TOP = 100
CELL_SIZE = (WIDTH - 2 * MARGIN) // BOARD_SIZE

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Хрестики-нулики")

# Colors
BG = (28, 28, 30)
LINE = (200, 200, 200)
X_COLOR = (220, 50, 50)
O_COLOR = (50, 180, 220)
HIGHLIGHT = (120, 200, 120)
TEXT_COLOR = (230, 230, 230)

FONT = pygame.font.SysFont(None, 40)
BIG_FONT = pygame.font.SysFont(None, 56)

clock = pygame.time.Clock()

# Game state
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = "X"  # X goes first
winner = None
winning_cells = []  # list of (r,c) in winning line
game_over = False

def reset_game():
    global board, current_player, winner, winning_cells, game_over
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = "X"
    winner = None
    winning_cells = []
    game_over = False

def draw_board():
    SCREEN.fill(BG)
    # Title
    title = BIG_FONT.render("Хрестики-нулики", True, TEXT_COLOR)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    # Draw grid
    for i in range(BOARD_SIZE + 1):
        # vertical
        start_x = MARGIN + i * CELL_SIZE
        pygame.draw.line(SCREEN, LINE, (start_x, BOARD_TOP), (start_x, BOARD_TOP + CELL_SIZE * BOARD_SIZE), 4)
        # horizontal
        start_y = BOARD_TOP + i * CELL_SIZE
        pygame.draw.line(SCREEN, LINE, (MARGIN, start_y), (MARGIN + CELL_SIZE * BOARD_SIZE, start_y), 4)

    # Draw marks
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            val = board[r][c]
            cx = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2
            if val == "X":
                draw_x(cx, cy, CELL_SIZE // 2 - 20)
            elif val == "O":
                draw_o(cx, cy, CELL_SIZE // 2 - 20)

    # Highlight winning cells if any
    if winning_cells:
        for (r, c) in winning_cells:
            rect = pygame.Rect(MARGIN + c*CELL_SIZE + 2, BOARD_TOP + r*CELL_SIZE + 2, CELL_SIZE-4, CELL_SIZE-4)
            pygame.draw.rect(SCREEN, (HIGHLIGHT[0], HIGHLIGHT[1], HIGHLIGHT[2], 60), rect, border_radius=8)
            # Draw a translucent overlay
            s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            s.fill((HIGHLIGHT[0], HIGHLIGHT[1], HIGHLIGHT[2], 100))
            SCREEN.blit(s, (rect.x, rect.y))

    # Bottom info
    if not game_over:
        info = FONT.render(f"Хід: {current_player}    (Натисни R щоб перезапустити)", True, TEXT_COLOR)
    else:
        if winner is None:
            info = FONT.render("Нічия! Натисни R щоб грати ще.", True, TEXT_COLOR)
        else:
            info = FONT.render(f"Переміг: {winner}! Натисни R щоб грати ще.", True, TEXT_COLOR)
    SCREEN.blit(info, (20, HEIGHT - 50))

def draw_x(cx, cy, half):
    # two lines
    start1 = (cx - half, cy - half)
    end1 = (cx + half, cy + half)
    start2 = (cx - half, cy + half)
    end2 = (cx + half, cy - half)
    pygame.draw.line(SCREEN, X_COLOR, start1, end1, 10)
    pygame.draw.line(SCREEN, X_COLOR, start2, end2, 10)

def draw_o(cx, cy, radius):
    pygame.draw.circle(SCREEN, O_COLOR, (cx, cy), radius, 10)

def pos_to_cell(pos):
    x, y = pos
    if x < MARGIN or x > MARGIN + CELL_SIZE*BOARD_SIZE or y < BOARD_TOP or y > BOARD_TOP + CELL_SIZE*BOARD_SIZE:
        return None
    c = (x - MARGIN) // CELL_SIZE
    r = (y - BOARD_TOP) // CELL_SIZE
    return (int(r), int(c))

def check_winner():
    # rows
    for r in range(BOARD_SIZE):
        if board[r][0] is not None and all(board[r][c] == board[r][0] for c in range(BOARD_SIZE)):
            return board[r][0], [(r, c) for c in range(BOARD_SIZE)]
    # cols
    for c in range(BOARD_SIZE):
        if board[0][c] is not None and all(board[r][c] == board[0][c] for r in range(BOARD_SIZE)):
            return board[0][c], [(r, c) for r in range(BOARD_SIZE)]
    # diag TL-BR
    if board[0][0] is not None and all(board[i][i] == board[0][0] for i in range(BOARD_SIZE)):
        return board[0][0], [(i, i) for i in range(BOARD_SIZE)]
    # diag TR-BL
    if board[0][BOARD_SIZE-1] is not None and all(board[i][BOARD_SIZE-1-i] == board[0][BOARD_SIZE-1] for i in range(BOARD_SIZE)):
        return board[0][BOARD_SIZE-1], [(i, BOARD_SIZE-1-i) for i in range(BOARD_SIZE)]
    # draw?
    if all(board[r][c] is not None for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        return None, []
    return None, []

# Main loop
reset_game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            cell = pos_to_cell(event.pos)
            if cell:
                r, c = cell
                if board[r][c] is None:
                    board[r][c] = current_player
                    w, cells = check_winner()
                    if w is not None:
                        winner = w
                        winning_cells = cells
                        game_over = True
                    else:
                        if all(board[i][j] is not None for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
                            winner = None
                            winning_cells = []
                            game_over = True
                        else:
                            current_player = "O" if current_player == "X" else "X"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    draw_board()
    pygame.display.flip()
    clock.tick(60)

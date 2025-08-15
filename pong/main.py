import pygame
import sys
import os

# === Constants ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10

PADDLE_SPEED = 7
BALL_SPEED_X = 6
BALL_SPEED_Y = 6

WINNING_SCORE = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT_NAME = "freesansbold.ttf"

# === Game States ===
STATE_START = "start"
STATE_NAME_ENTRY_1 = "name_entry_1"
STATE_NAME_ENTRY_2 = "name_entry_2"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

# === Helper Classes ===
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0

    def move(self, dy):
        self.rect.y += dy
        self.rect.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BALL_SIZE // 2,
            SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE, BALL_SIZE
        )
        self.reset()

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.vx = BALL_SPEED_X if pygame.time.get_ticks() % 2 == 0 else -BALL_SPEED_X
        self.vy = BALL_SPEED_Y if pygame.time.get_ticks() % 2 == 0 else -BALL_SPEED_Y

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

# === Score Saving/Updating ===
def save_or_update_scores(filename, name1, score1, name2, score2):
    scores = {}
    # Read existing scores
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                if ":" in line:
                    name, score = line.strip().split(":", 1)
                    scores[name.strip()] = int(score.strip())
    # Update or add new scores
    scores[name1] = score1
    scores[name2] = score2
    # Write back all scores
    with open(filename, "w") as f:
        for name, score in scores.items():
            f.write(f"{name}: {score}\n")

# === Main Game Function ===
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Game")
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(FONT_NAME, 48)
    font_medium = pygame.font.Font(FONT_NAME, 32)
    font_small = pygame.font.Font(FONT_NAME, 24)

    # Game state
    state = STATE_START
    player1_name = ""
    player2_name = ""
    player1_score = 0
    player2_score = 0
    winner = None
    name_entry_buffer = ""

    # Entities
    paddle1 = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- State: Start Screen ---
            if state == STATE_START:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        state = STATE_NAME_ENTRY_1
                        name_entry_buffer = ""
            # --- State: Player 1 Name Entry ---
            elif state == STATE_NAME_ENTRY_1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name_entry_buffer.strip():
                        player1_name = name_entry_buffer.strip()
                        name_entry_buffer = ""
                        state = STATE_NAME_ENTRY_2
                    elif event.key == pygame.K_BACKSPACE:
                        name_entry_buffer = name_entry_buffer[:-1]
                    elif event.key <= 127 and len(name_entry_buffer) < 12:
                        name_entry_buffer += event.unicode
            # --- State: Player 2 Name Entry ---
            elif state == STATE_NAME_ENTRY_2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name_entry_buffer.strip():
                        player2_name = name_entry_buffer.strip()
                        state = STATE_PLAYING
                        player1_score = 0
                        player2_score = 0
                        winner = None
                        ball.reset()
                        paddle1.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
                        paddle2.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
                        name_entry_buffer = ""
                    elif event.key == pygame.K_BACKSPACE:
                        name_entry_buffer = name_entry_buffer[:-1]
                    elif event.key <= 127 and len(name_entry_buffer) < 12:
                        name_entry_buffer += event.unicode
            # --- State: Game Over ---
            elif state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = STATE_START

        # --- State Rendering and Logic ---
        if state == STATE_START:
            title = font_large.render("PONG", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
            msg = font_medium.render("Press SPACE to Start", True, WHITE)
            screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
            controls = [
                "Controls:",
                "Player 1: W (up), S (down)",
                "Player 2: UP (up), DOWN (down)"
            ]
            for i, line in enumerate(controls):
                txt = font_small.render(line, True, WHITE)
                screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 300 + i * 30))
        elif state == STATE_NAME_ENTRY_1:
            prompt = font_medium.render("Enter Player 1 Name:", True, WHITE)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))
            entry = font_large.render(name_entry_buffer + "|", True, WHITE)
            screen.blit(entry, (SCREEN_WIDTH // 2 - entry.get_width() // 2, 270))
            instr = font_small.render("Press ENTER to confirm", True, WHITE)
            screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, 350))
        elif state == STATE_NAME_ENTRY_2:
            prompt = font_medium.render("Enter Player 2 Name:", True, WHITE)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))
            entry = font_large.render(name_entry_buffer + "|", True, WHITE)
            screen.blit(entry, (SCREEN_WIDTH // 2 - entry.get_width() // 2, 270))
            instr = font_small.render("Press ENTER to confirm", True, WHITE)
            screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, 350))
        elif state == STATE_PLAYING:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                paddle1.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                paddle1.move(PADDLE_SPEED)
            if keys[pygame.K_UP]:
                paddle2.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                paddle2.move(PADDLE_SPEED)

            # Ball movement
            ball.move()

            # Ball collision with top/bottom
            if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
                ball.vy *= -1

            # Ball collision with paddles
            if ball.rect.colliderect(paddle1.rect):
                ball.vx = abs(ball.vx)
            if ball.rect.colliderect(paddle2.rect):
                ball.vx = -abs(ball.vx)

            # Ball out of bounds (score)
            if ball.rect.left <= 0:
                player2_score += 1
                ball.reset()
            elif ball.rect.right >= SCREEN_WIDTH:
                player1_score += 1
                ball.reset()

            # Draw paddles and ball
            paddle1.draw(screen)
            paddle2.draw(screen)
            ball.draw(screen)

            # Draw center line
            for y in range(0, SCREEN_HEIGHT, 20):
                pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, y), (SCREEN_WIDTH // 2, y + 10), 2)

            # Draw scores
            score_text = font_large.render(f"{player1_score}   {player2_score}", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 30))

            # Draw player names
            name1 = font_small.render(player1_name, True, WHITE)
            name2 = font_small.render(player2_name, True, WHITE)
            screen.blit(name1, (SCREEN_WIDTH // 4 - name1.get_width() // 2, 10))
            screen.blit(name2, (3 * SCREEN_WIDTH // 4 - name2.get_width() // 2, 10))

            # Check for winner
            if player1_score >= WINNING_SCORE:
                winner = player1_name or "Player 1"
                # Save or update both player scores
                save_or_update_scores("scores.txt", player1_name or "Player 1", player1_score, player2_name or "Player 2", player2_score)
                state = STATE_GAME_OVER
            elif player2_score >= WINNING_SCORE:
                winner = player2_name or "Player 2"
                save_or_update_scores("scores.txt", player1_name or "Player 1", player1_score, player2_name or "Player 2", player2_score)
                state = STATE_GAME_OVER

        elif state == STATE_GAME_OVER:
            msg = font_large.render(f"{winner} Wins!", True, WHITE)
            screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
            instr = font_medium.render("Press R to Restart", True, WHITE)
            screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, 300))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
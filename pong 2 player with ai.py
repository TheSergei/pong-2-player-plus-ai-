import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [5, 5]
paddle_speed = 5
player1_pos = [50, HEIGHT // 2 - 50]
player2_pos = [WIDTH - 50, HEIGHT // 2 - 50]
paddle_width = 10
paddle_height = 100
score_player1 = 0
score_player2 = 0
vs_ai = False

# Menu variables
font = pygame.font.Font(None, 36)
menu_text1 = font.render("Press '1' for 1 Player vs AI", True, WHITE)
menu_text2 = font.render("Press '2' for 2 Players", True, WHITE)
menu_rect = menu_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
menu_rect2 = menu_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Main loop
clock = pygame.time.Clock()
menu = True
running = True
while menu:
    screen.fill(BLACK)
    screen.blit(menu_text1, menu_rect)
    screen.blit(menu_text2, menu_rect2)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                vs_ai = True
                menu = False
            if event.key == pygame.K_2:
                vs_ai = False
                menu = False

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if not vs_ai:
        if keys[pygame.K_w] and player1_pos[1] > 0:
            player1_pos[1] -= paddle_speed
        if keys[pygame.K_s] and player1_pos[1] < HEIGHT - paddle_height:
            player1_pos[1] += paddle_speed
        if keys[pygame.K_UP] and player2_pos[1] > 0:
            player2_pos[1] -= paddle_speed
        if keys[pygame.K_DOWN] and player2_pos[1] < HEIGHT - paddle_height:
            player2_pos[1] += paddle_speed
    else:
        if keys[pygame.K_w] and player1_pos[1] > 0:
            player1_pos[1] -= paddle_speed
        if keys[pygame.K_s] and player1_pos[1] < HEIGHT - paddle_height:
            player1_pos[1] += paddle_speed

    # AI for opponent's paddle
    if vs_ai:
        if ball_speed[0] > 0:
            if ball_pos[1] < player2_pos[1] + paddle_height // 2:
                player2_pos[1] -= paddle_speed
            elif ball_pos[1] > player2_pos[1] + paddle_height // 2:
                player2_pos[1] += paddle_speed

    # Ball movement
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Ball collision with walls
    if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT:
        ball_speed[1] *= -1

    # Ball collision with paddles
    if ball_pos[0] <= player1_pos[0] + paddle_width and player1_pos[1] <= ball_pos[1] <= player1_pos[1] + paddle_height:
        ball_speed[0] *= -1
    if ball_pos[0] >= player2_pos[0] - paddle_width and player2_pos[1] <= ball_pos[1] <= player2_pos[1] + paddle_height:
        ball_speed[0] *= -1

    # Ball out of bounds
    if ball_pos[0] <= 0:
        score_player2 += 1
        ball_pos = [WIDTH // 2, HEIGHT // 2]
    elif ball_pos[0] >= WIDTH:
        score_player1 += 1
        ball_pos = [WIDTH // 2, HEIGHT // 2]

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (player1_pos[0], player1_pos[1], paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (player2_pos[0], player2_pos[1], paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_pos[0] - 10, ball_pos[1] - 10, 20, 20))

    # Display scores
    player1_score_text = font.render(str(score_player1), True, WHITE)
    player2_score_text = font.render(str(score_player2), True, WHITE)
    screen.blit(player1_score_text, (WIDTH // 2 - 50, 20))
    screen.blit(player2_score_text, (WIDTH // 2 + 30, 20))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

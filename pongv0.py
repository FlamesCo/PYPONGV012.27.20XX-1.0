import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ball dimensions
BALL_WIDTH = 15
BALL_HEIGHT = 15

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

# Game variables
ball_vel_x = 7 * random.choice((1, -1))
ball_vel_y = 7 * random.choice((1, -1))
paddle_speed = 5

# Score
player_score = 0
opponent_score = 0

# Font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Ball setup
ball = pygame.Rect(SCREEN_WIDTH / 2 - BALL_WIDTH / 2, SCREEN_HEIGHT / 2 - BALL_HEIGHT / 2, BALL_WIDTH, BALL_HEIGHT)

# Paddles setup
player_paddle = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH - 20, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(20, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Function to draw the ball
def draw_ball():
    pygame.draw.ellipse(screen, WHITE, ball)

# Function to draw the paddles
def draw_paddles():
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)

# Function to update the ball's position
def update_ball():
    global ball_vel_x, ball_vel_y, player_score, opponent_score

    ball.x += ball_vel_x
    ball.y += ball_vel_y

    # Ball collision with top and bottom of screen
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_vel_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_vel_x *= -1

    # Scoring
    if ball.left <= 0:
        player_score += 1
        reset_ball()
    if ball.right >= SCREEN_WIDTH:
        opponent_score += 1
        reset_ball()

# Function to reset the ball
def reset_ball():
    global ball_vel_x, ball_vel_y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball_vel_x *= random.choice((1, -1))
    ball_vel_y *= random.choice((1, -1))

# Function to handle paddle movement
def handle_paddle_movement(keys, paddle):
    if keys[pygame.K_UP] and paddle.top > 0:
        paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle.bottom < SCREEN_HEIGHT:
        paddle.y += paddle_speed

# Function to handle opponent AI movement
def opponent_ai():
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += paddle_speed
    else:
        opponent_paddle.y -= paddle_speed

# Function to draw the score
def draw_score():
    player_score_text = font.render(str(player_score), True, WHITE)
    opponent_score_text = font.render(str(opponent_score), True, WHITE)

    screen.blit(player_score_text, (SCREEN_WIDTH / 2 + 20, 20))
    screen.blit(opponent_score_text, (SCREEN_WIDTH / 2 - 40, 20))

# Main game loop
while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    handle_paddle_movement(keys, player_paddle)
    opponent_ai()

    # Updating the game
    update_ball()

    # Drawing everything
    screen.fill(BLACK)
    draw_ball()
    draw_paddles()
    draw_score()

    # Updating the window
    pygame.display.flip()
    pygame.time.Clock().tick(60)

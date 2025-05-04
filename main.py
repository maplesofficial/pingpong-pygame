# /// script
# dependencies = [
#   "pygame-ce"
# ]
# ///

import sys, asyncio
import os
if sys.platform == "emscripten":
    import asyncio
    import platform
    platform.window.canvas.style.imageRendering = "pixelated"
    ASSET_PATH = "assets"
else:
    ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets")
    
import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

TABLE = pygame.image.load(os.path.join(ASSET_PATH, "pingpong_table.png"))
BALL_COLOR = (255, 255, 255)      
L_PADDLE_COLOR = (30, 30, 30)       
R_PADDLE_COLOR = (160, 40, 50)  


# Set the size and speed for both the paddles and the ball
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 120
PADDLE_SPEED = 15

BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 6, 6


# position of the paddle = the left and right edges of the screen
L_PADDLE = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                       PADDLE_WIDTH, PADDLE_HEIGHT)
R_PADDLE = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                       PADDLE_WIDTH, PADDLE_HEIGHT)

# position of the ball = center of the screen
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                       HEIGHT // 2 - BALL_SIZE // 2,
                       BALL_SIZE, BALL_SIZE)
clock = pygame.time.Clock()

# Handle the move

def move_paddles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and L_PADDLE.top > 0:
        L_PADDLE.y -= PADDLE_SPEED
    if keys[pygame.K_x] and L_PADDLE.bottom < HEIGHT:
        L_PADDLE.y += PADDLE_SPEED
    if keys[pygame.K_UP] and R_PADDLE.top > 0:
        R_PADDLE.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and R_PADDLE.bottom < HEIGHT:
            R_PADDLE.y += PADDLE_SPEED

def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
    if ball.colliderect(L_PADDLE) or ball.colliderect(R_PADDLE):
        BALL_SPEED_X *= -1

async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move_paddles()
        move_ball()
            
        screen.blit(TABLE, (0, 0))


        pygame.draw.rect(screen, L_PADDLE_COLOR, L_PADDLE)
        pygame.draw.rect(screen, R_PADDLE_COLOR, R_PADDLE)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
        await asyncio.sleep(0)


asyncio.run(main())



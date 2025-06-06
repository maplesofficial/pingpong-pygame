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
    # platform.window.canvas.style.imageRendering = "pixelated"
    ASSET_PATH = "assets"
else:
    ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets")
    
import pygame
pygame.init()

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

FPS = 60

TABLE = pygame.image.load(os.path.join(ASSET_PATH, "pingpong_table.png"))
BALL_COLOR = (255, 165, 0)      
L_COLOR = (30, 30, 30)       
R_COLOR = (160, 40, 50)  
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 10

SCORE_FONT = pygame.font.SysFont("impact", 60)
WINNING_SCORE = 11


class Paddle:
    VEL = 5

    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 6
    COLOR = BALL_COLOR


    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.blit(TABLE, (0, 0))

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, (255,255,255))
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, (255,255,255))
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 40))
    win.blit(right_score_text, (WIDTH * (3/4)  - right_score_text.get_width() // 2, 40))

    for paddle in paddles:
        paddle.draw(win)
    
    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up = True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up = False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up = False)

async def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(L_COLOR, 10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(R_COLOR, WIDTH - 25, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1 
            ball.reset()

        won = False 

        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        
        if won:
            text = SCORE_FONT.render(win_text, 1, (255, 255, 255))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

        await asyncio.sleep(0)
        
   
    pygame.quit()

if __name__ == '__main__':
    asyncio.run(main())



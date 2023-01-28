import os, pygame
import numpy as np

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
size = width, height = 500, 1000

board = np.zeros(size, dtype=np.int8)
speed = np.array([0, 1])
hor_move = np.array([111, 0])
black = 0, 0, 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

ball = pygame.image.load("intro_ball.gif")
past_ballrects = []
ballrect = ball.get_rect()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if ballrect.right+hor_move[0] < width:
                    ballrect = ballrect.move(hor_move)

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if ballrect.right-hor_move[0] > 0:
                    ballrect = ballrect.move(-hor_move)

    ballrect = ballrect.move(speed)

    screen.fill(black)
    if ballrect.top < 0 or ballrect.bottom > height or pygame.Rect.collidelist(ballrect, past_ballrects) != -1:
        past_ballrects.append(ballrect)
        ballrect = ball.get_rect()
        # print(past_ballrects)
        # print(board)

    screen.blit(ball, ballrect)
    for ballrect_draw in past_ballrects:
        screen.blit(ball, ballrect_draw)
    pygame.display.flip()

pygame.quit()
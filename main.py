import os, pygame
import numpy as np
from spritesheet import spritesheet
from string import ascii_uppercase as letters
from collections import deque
from words import WORDS_SET, LETTER_DIST

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
size = width, depth = 500, 1000

sq_img_size = 100

BOARD = np.zeros((1000, 500), dtype=np.int8)
black = 0, 0, 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# get letter images from all_letters, store in dict in format "letter: image"
ss = spritesheet('all_letters.png')
ss_small = spritesheet('all_letters_small.png')
letter_image_dict = {}
letter_image_small_dict = {}
for i, letter in enumerate(letters):
    letter_image = ss.image_at((0, sq_img_size*i, sq_img_size, sq_img_size))
    letter_image_dict[letter] = letter_image
    letter_image_small = ss_small.image_at((0, sq_img_size//2*i, sq_img_size//2, sq_img_size//2))
    letter_image_small_dict[letter] = letter_image_small


HOR_MOVE = np.array([sq_img_size, 0])
VERT_MOVE = np.array([0, 3])

def rand_letter(letter_set: list):
    return LETTER_DIST[np.random.randint(0, len(letter_set))]

def random_letter_sprite():
    random_letter = LETTER_DIST[np.random.randint(0, 98)]
    return random_letter, letter_image_dict[random_letter]

def make_new(object, topleft=(200, 0)):
    return object.get_rect(topleft=topleft)


past_letter_rects = []
next_letters = deque([rand_letter(LETTER_DIST) for _ in range(3)])
current_letter = rand_letter(LETTER_DIST)
letter_sprite = letter_image_dict[current_letter]


    # print(i*50, 0, next_letter)

letter_rect = make_new(letter_sprite)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # check left side of screen and new left coordinate is not already taken
                new_left_coordinate = letter_rect.left + HOR_MOVE[0]
                if new_left_coordinate < width and BOARD[letter_rect.bottom, new_left_coordinate] == 0:
                    letter_rect = letter_rect.move(HOR_MOVE)

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # check left side of screen and new left coordinate is not already taken
                new_left_coordinate = letter_rect.left - HOR_MOVE[0]
                if new_left_coordinate >= 0 and BOARD[letter_rect.bottom, new_left_coordinate] == 0:
                    letter_rect = letter_rect.move(-HOR_MOVE)

    letter_rect = letter_rect.move(VERT_MOVE)
    screen.fill(black)

    # next letters logic
    for i, next_letter in enumerate(next_letters):
        next_letter_sprite = letter_image_small_dict[next_letter]
        next_letter_rect = next_letter_sprite.get_rect(topleft=(i*(sq_img_size//2 + 10), 0))
        screen.blit(next_letter_sprite, next_letter_rect)

    # if bottom is at edge of screen or bottom left overlaps with square (bottom is exclusive, so haven't moved there)
    if letter_rect.bottom >= depth or BOARD[letter_rect.bottom, letter_rect.left] == 1:
        past_letter_rects.append((letter_sprite, letter_rect))
        BOARD[letter_rect.top: letter_rect.bottom, letter_rect.left: letter_rect.right] = 1
        # print(BOARD)  # for debugging
        # print((letter_rect.top, letter_rect.left), (letter_rect.top, letter_rect.left))
        # current_letter, letter_sprite = random_letter_sprite()
        current_letter = next_letters.pop()
        letter_sprite = letter_image_dict[current_letter]
        letter_rect = make_new(letter_sprite)

        next_letters.appendleft(rand_letter(LETTER_DIST))

        # if screen fills, end game
        if BOARD[letter_rect.bottom, letter_rect.left] == 1:
            running = False
            break

    screen.blit(letter_sprite, letter_rect)
    for past_letter_sprite, past_letter_rect in past_letter_rects:
        screen.blit(past_letter_sprite, past_letter_rect)
    pygame.display.flip()

pygame.quit()

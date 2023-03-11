import os, pygame
import numpy as np
from spritesheet import spritesheet
from string import ascii_uppercase as letters

os.environ['SDL_VIDEO_CENTERED'] = '1'
scrab_letters = 'AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ'
scrab_letters = list(scrab_letters)
pygame.init()
size = width, depth = 500, 1000

sq_img_size = 100

BOARD = np.zeros((1000, 500), dtype=np.int8)
black = 0, 0, 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# get letter images from all_letters, store in dict in format "letter: image"
ss = spritesheet('all_letters.png')
letter_image_dict = {}
for i, letter in enumerate(letters):
    letter_image = ss.image_at((0, sq_img_size*i, sq_img_size, sq_img_size))
    letter_image_dict[letter] = letter_image


HOR_MOVE = np.array([sq_img_size, 0])
VERT_MOVE = np.array([0, 3])

def random_letter_sprite():
    random_letter = scrab_letters[np.random.randint(0, 98)]
    return random_letter, letter_image_dict[random_letter]

def make_new(object, topleft=(200, 0)):
    return object.get_rect(topleft=topleft)


past_letter_rects = []
current_letter, letter_sprite = random_letter_sprite()
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

    # if bottom is at edge of screen or bottom left overlaps with square (bottom is exclusive, so haven't moved there)
    if letter_rect.bottom >= depth or BOARD[letter_rect.bottom, letter_rect.left] == 1:
        past_letter_rects.append((letter_sprite, letter_rect))
        BOARD[letter_rect.top: letter_rect.bottom, letter_rect.left: letter_rect.right] = 1
        # print(BOARD)  # for debugging
        # print((letter_rect.top, letter_rect.left), (letter_rect.top, letter_rect.left))
        current_letter, letter_sprite = random_letter_sprite()
        letter_rect = make_new(letter_sprite)

        # if screen fills, end game
        if BOARD[letter_rect.bottom, letter_rect.left] == 1:
            running = False
            break

    screen.blit(letter_sprite, letter_rect)
    for past_letter_sprite, past_letter_rect in past_letter_rects:
        screen.blit(past_letter_sprite, past_letter_rect)
    pygame.display.flip()

pygame.quit()

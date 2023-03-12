import os, pygame
import numpy as np
from spritesheet import spritesheet
from string import ascii_uppercase as letters
from words import WORDS_SET, LETTER_DIST

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

SIZE = WIDTH, DEPTH = 500, 1000
SQ_IMG_SIZE = 100

BOARD_PIXEL = np.zeros((1000, 500), dtype=np.int8)
BOARD_GAME = np.zeros((10, 5), dtype=np.int8)
BOARD_LETTER = np.empty((10, 5), dtype='<U1')
BOARD_RECT = np.empty((10, 5), dtype=object)
BOARD_INDICIES = list(np.ndindex(10, 5))

HOR_MOVE = np.array([SQ_IMG_SIZE, 0])
VERT_MOVE = np.array([0, 2])

SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()

BLACK = (0, 0, 0)

WORD_SIZE = 5

# get letter images from all_letters, store in dict in format "letter: image"
ss = spritesheet('all_letters.png')
ss_small = spritesheet('all_letters_small.png')
SPRITES_LETTER = {}
SPRITES_LETTER_SMALL = {}
for i, letter in enumerate(letters):
    letter_image = ss.image_at((0, SQ_IMG_SIZE*i, SQ_IMG_SIZE, SQ_IMG_SIZE))
    letter_image_small = ss_small.image_at((0, SQ_IMG_SIZE//2*i, SQ_IMG_SIZE//2, SQ_IMG_SIZE//2))

    SPRITES_LETTER[letter] = letter_image
    SPRITES_LETTER_SMALL[letter] = letter_image_small


def rand_letter(letter_set: list):
    return LETTER_DIST[np.random.randint(0, len(letter_set))]


def make_new(object, topleft=(200, 50)):
    return object.get_rect(topleft=topleft)


past_letter_rects = []
NEXT_LETTERS = [rand_letter(LETTER_DIST) for _ in range(6)]
CURRENT_LETTER = NEXT_LETTERS[-1]
CURRENT_LETTER_SPRITE = SPRITES_LETTER[CURRENT_LETTER]
CURRENT_LETTER_RECT = make_new(CURRENT_LETTER_SPRITE)

running = True
while running:
    CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # check right side of SCREEN and new left coordinate is not already taken
                new_left_coordinate = CURRENT_LETTER_RECT.left + HOR_MOVE[0]
                if new_left_coordinate < WIDTH and BOARD_PIXEL[CURRENT_LETTER_RECT.bottom, new_left_coordinate] == 0:
                    CURRENT_LETTER_RECT = CURRENT_LETTER_RECT.move(HOR_MOVE)

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # check left side of SCREEN and new left coordinate is not already taken
                new_left_coordinate = CURRENT_LETTER_RECT.left - HOR_MOVE[0]
                if new_left_coordinate >= 0 and BOARD_PIXEL[CURRENT_LETTER_RECT.bottom, new_left_coordinate] == 0:
                    CURRENT_LETTER_RECT = CURRENT_LETTER_RECT.move(-HOR_MOVE)

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # check left side of SCREEN and new left coordinate is not already taken
                new_bottom_coordinate = CURRENT_LETTER_RECT.bottom + VERT_MOVE[1]
                while CURRENT_LETTER_RECT.bottom + VERT_MOVE[1] < DEPTH and BOARD_PIXEL[CURRENT_LETTER_RECT.bottom + VERT_MOVE[1], CURRENT_LETTER_RECT.left] == 0:
                    # print('true')
                    CURRENT_LETTER_RECT = CURRENT_LETTER_RECT.move(VERT_MOVE)

            elif event.key == pygame.K_SPACE or event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                # rotate current letter
                current_topleft = CURRENT_LETTER_RECT.topleft
                NEXT_LETTERS.insert(0, NEXT_LETTERS.pop())
                CURRENT_LETTER = NEXT_LETTERS[-1]
                CURRENT_LETTER_SPRITE = SPRITES_LETTER[CURRENT_LETTER]
                CURRENT_LETTER_RECT = make_new(CURRENT_LETTER_SPRITE, topleft=current_topleft)

    CURRENT_LETTER_RECT = CURRENT_LETTER_RECT.move(VERT_MOVE)
    SCREEN.fill(BLACK)

    # next letters logic
    for i, next_letter in enumerate(NEXT_LETTERS[:-1]):
        next_current_letter_sprite = SPRITES_LETTER_SMALL[next_letter]
        next_letter_rect = next_current_letter_sprite.get_rect(topleft=(i*(SQ_IMG_SIZE//2 + 10), 0))
        SCREEN.blit(next_current_letter_sprite, next_letter_rect)

    # if bottom is at edge of SCREEN or bottom left overlaps with square (bottom is exclusive, so haven't moved there)
    if CURRENT_LETTER_RECT.bottom >= DEPTH or BOARD_PIXEL[CURRENT_LETTER_RECT.bottom, CURRENT_LETTER_RECT.left] == 1:
        past_letter_rects.append((CURRENT_LETTER_SPRITE, CURRENT_LETTER_RECT))

        # round to nearest 100 b/c speed is not necessarily 1
        CURRENT_LETTER_RECT.top = (CURRENT_LETTER_RECT.top//100)*100
        CURRENT_LETTER_RECT.bottom = (CURRENT_LETTER_RECT.bottom//100)*100
        CURRENT_LETTER_RECT.left = (CURRENT_LETTER_RECT.left//100)*100
        CURRENT_LETTER_RECT.right = (CURRENT_LETTER_RECT.right//100)*100

        # convert to small board coordinates
        x_board = CURRENT_LETTER_RECT.left//100
        y_board = CURRENT_LETTER_RECT.top//100

        # store appropriate board values
        BOARD_PIXEL[
            CURRENT_LETTER_RECT.top: CURRENT_LETTER_RECT.bottom,
            CURRENT_LETTER_RECT.left: CURRENT_LETTER_RECT.right
        ] = 1
        BOARD_GAME[y_board, x_board] = 1
        BOARD_LETTER[y_board, x_board] = CURRENT_LETTER
        BOARD_RECT[y_board, x_board] = CURRENT_LETTER_RECT

        # print(BOARD_PIXEL)  # for debugging
        # print(CURRENT_LETTER_RECT.top, CURRENT_LETTER_RECT.left, CURRENT_LETTER_RECT.top, CURRENT_LETTER_RECT.left)
        NEXT_LETTERS.pop()
        CURRENT_LETTER = NEXT_LETTERS[-1]
        CURRENT_LETTER_SPRITE = SPRITES_LETTER[CURRENT_LETTER]
        CURRENT_LETTER_RECT = make_new(CURRENT_LETTER_SPRITE)

        NEXT_LETTERS.insert(0, rand_letter(LETTER_DIST))

    SCREEN.blit(CURRENT_LETTER_SPRITE, CURRENT_LETTER_RECT)

    # Check for row/column goals/endgame criteria
    col_sums = np.sum(BOARD_GAME, axis=0)
    row_sums = np.sum(BOARD_GAME, axis=1)

    # if any columns have 5 or more letters, check for words
    if np.any(col_sums >= 5):
        col_nums = np.where(col_sums >= 5)[0]
        for col_num in col_nums:
            # col = BOARD_LETTER[:, col_num]
            col = np.where(BOARD_GAME[:, col_num] == 1)[0]
            # iterate over all the different words that could be in column
            word_start_indicies = col[:-4]
            for word_start_index in word_start_indicies:

                # may allow to do forward and backward words in columns
                potential_word_letters = BOARD_LETTER[word_start_index:word_start_index+WORD_SIZE, col_num]
                potential_word = ''.join(potential_word_letters)

                if potential_word in WORDS_SET:
                # if True:  # for debugging
                    # print('COL WINNER!!!')

                    # clear word in col
                    BOARD_GAME[word_start_index:word_start_index+WORD_SIZE, col_num] = 0
                    BOARD_LETTER[word_start_index:word_start_index+WORD_SIZE, col_num] = ''
                    BOARD_RECT[word_start_index:word_start_index+WORD_SIZE, col_num] = None
                    BOARD_PIXEL[word_start_index*100:(word_start_index+WORD_SIZE)*100, col_num*100:(col_num+1)*100] = 0

                    # move part of column above word down (very rare case but could happen if row win leads to col win with stuff above it) I also haven't tested this yet
                    BOARD_GAME[word_start_index:2*word_start_index, col_num] = BOARD_GAME[0:word_start_index, col_num]
                    BOARD_LETTER[word_start_index:2*word_start_index, col_num] = BOARD_LETTER[0:word_start_index, col_num]
                    BOARD_RECT[word_start_index:2*word_start_index, col_num] = BOARD_RECT[0:word_start_index, col_num]
                    BOARD_PIXEL[word_start_index*100:2*word_start_index*100, col_num * 100:(col_num + 1) * 100] = BOARD_PIXEL[:word_start_index*100, col_num * 100:(col_num + 1) * 100]

    # if any rows have 5 or more letters, check for words
    if np.any(row_sums >= 5):
        row_nums = np.where(row_sums >= 5)[0]
        for row_num in row_nums:
            potential_word = ''.join(BOARD_LETTER[row_num, :])

            if potential_word in WORDS_SET:
            # if True:  # for debugging
                # print('ROW WINNER!!!')

                # clear row
                BOARD_GAME[row_num, :] = 0
                BOARD_LETTER[row_num, :] = ''
                BOARD_RECT[row_num, :] = None
                BOARD_PIXEL[row_num*100:(row_num+1)*100, :] = 0

                # move whatever is above row down
                BOARD_GAME[1:row_num+1, :] = BOARD_GAME[0:row_num, :]
                BOARD_LETTER[1:row_num+1, :] = BOARD_LETTER[0:row_num, :]
                BOARD_RECT[1:row_num+1, :] = BOARD_RECT[0:row_num, :]
                BOARD_PIXEL[100:(row_num+1)*100, :] = BOARD_PIXEL[0:row_num*100, :]

    # if any columns have 9 or more letters, end game
    if np.any(col_sums >= 9):
        running = False
        break


    for board_index in BOARD_INDICIES:
        if BOARD_GAME[board_index] == 1:
            past_letter = BOARD_LETTER[board_index]
            past_letter_rect = BOARD_RECT[board_index]

            # update rect location from updated board position
            past_letter_rect.top = board_index[0]*100
            past_letter_rect.left = board_index[1]*100

            past_letter_sprite = SPRITES_LETTER[past_letter]
            SCREEN.blit(past_letter_sprite, past_letter_rect)

    pygame.display.flip()

pygame.quit()

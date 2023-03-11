from PIL import Image, ImageFont, ImageDraw
import numpy as np
from string import ascii_uppercase as letters

if __name__ == '__main__':
    # image = Image.open('intro_ball.gif')
    # new_image = image.resize((100, 100))
    letter_images = []
    font = ImageFont.truetype("Verdana.ttf", 50)
    for letter in letters:
        new_image = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8) * 255)
        image_editable = ImageDraw.Draw(new_image)
        image_editable.text((50, 50), letter, (0, 0, 0), font=font, anchor='mm')
        letter_images.append(np.array(new_image))
    new_image = Image.fromarray(np.vstack(letter_images))
    new_image.save('all_letters.png')

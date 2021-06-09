import os

from PIL import Image, ImageDraw, ImageFont


def pil_to_real(x, y):
    x = x / 3
    y = -y / 3
    return x, y


def real_to_pil(x, y):
    x = x * 3
    y = -y * 3
    return x, y


def intersects(circle, rect):
    circle_distance = {}
    circle_distance['x'] = abs(circle['x'] - rect['x'])
    circle_distance['y'] = abs(circle['y'] - rect['y'])

    if circle_distance['x'] > (rect['width']/2 + circle['r']):
        return False
    if circle_distance['y'] > (rect['height']/2 + circle['r']):
        return False

    if circle_distance['x'] <= (rect['width']/2):
        return True
    if circle_distance['y'] <= (rect['height']/2):
        return True

    corner_distance_sq = (circle_distance['x'] - rect['width']/2)**2 + (circle_distance['y'] - rect['height']/2)**2

    return corner_distance_sq <= (circle['r']**2)


def draw_text(pointer, text, d, circles):
    status = 'end'
    if pointer['y'] + TEXT_HEIGHT > IMAGE_HEIGHT:
        return status
    text_width = font.getsize(text)[0]

    text_rect = {'x': pointer['x'] + text_width / 2,
                 'y': pointer['y'] + TEXT_HEIGHT / 2,
                 'width': text_width + INDENT * 2,
                 'height': TEXT_HEIGHT + INDENT * 2
                 }

    for circle in circles:
        if intersects({'x': circle[0], 'y': circle[1], 'r': circle[2]}, text_rect):
            status = 'circle'
            break
    else:
        if text_width + pointer['x'] < IMAGE_WIDTH:
            d.text((pointer['x'], pointer['y']), text, font=font, fill='black')
            pointer['x'] += text_width + SPACE_SIZE
            status = 'success'
            return status

    if text_width + pointer['x'] >= IMAGE_WIDTH:
        status = 'wall'

    return status


CIRCLES = ((100, 200, 50), (50, 100, 40), (200, 700, 10), (400, 600, 50))
TEXT = 'Мама мыла раму'
current_dir = os.getcwd()
os.chdir(__file__.removesuffix('wrap.py'))
font = ImageFont.truetype('Roboto-Light.ttf', size=20)
os.chdir(current_dir)
SPACE_SIZE, TEXT_HEIGHT = font.getsize(' ')
IMAGE_WIDTH, IMAGE_HEIGHT = 600, 900
INDENT = 20


def get_image(circles: list[tuple[int, int, int]] = CIRCLES, text: str = TEXT):
    # create an image
    out = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))
    # get a drawing context
    d = ImageDraw.Draw(out)
    pointer = {'x': 0, 'y': 0}
    while True:
        result = draw_text(pointer, text, d, circles)
        if result == 'success':
            continue
        elif result == 'end':
            break
        elif result == 'wall' or result == 'circle':
            words = text.split()
            word_i = 0
            while word_i < len(words):
                result = draw_text(pointer, words[word_i], d, circles)
                if result == 'success':
                    word_i += 1
                elif result == 'end':
                    break
                elif result == 'circle':
                    pointer['x'] += SPACE_SIZE
                elif result == 'wall':
                    pointer['y'] += TEXT_HEIGHT
                    pointer['x'] = 0
    # for circle in circles:
    #     d.ellipse([circle[0] - circle[2], circle[1] - circle[2], circle[0] + circle[2], circle[1] + circle[2]],
    #               outline='black')
    return out

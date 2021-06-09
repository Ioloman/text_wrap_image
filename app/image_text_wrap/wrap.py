import os
from PIL import Image, ImageDraw, ImageFont


def intersects(circle: dict[str, int], rect: dict[str, int]) -> bool:
    """
    Определяет пересекается ли окружности и прямоугольник или находится внутри или нет
    :param circle: окружность
    :param rect:
    :return: True если пересекается или находится внутри
    """
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


def draw_text(pointer: dict[str, int], text: str, d: ImageDraw, circles: list[tuple[int, int, int]]) -> str:
    """
    Создает изображение
    :param pointer: положение на изображении
    :param text: надпись для печати
    :param d: контекст рисования
    :param circles: список окружностей
    :return: статус
    """
    status = 'end'
    # условия конца картинки
    if pointer['y'] + TEXT_HEIGHT > IMAGE_HEIGHT:
        return status
    # ширина надписи
    text_width = font.getsize(text)[0]
    # определение бокса вокруг текста  + отступ
    text_rect = {'x': pointer['x'] + text_width / 2,
                 'y': pointer['y'] + TEXT_HEIGHT / 2,
                 'width': text_width + INDENT * 2,
                 'height': TEXT_HEIGHT + INDENT * 2
                 }
    # определяем есть ли пересечение бокса с кругами, если да статус circle
    for circle in circles:
        if intersects({'x': circle[0], 'y': circle[1], 'r': circle[2]}, text_rect):
            status = 'circle'
            break
    else:
        # если нет, то рисуем текст, успешно
        if text_width + pointer['x'] < IMAGE_WIDTH:
            d.text((pointer['x'], pointer['y']), text, font=font, fill='black')
            pointer['x'] += text_width + SPACE_SIZE
            status = 'success'
            return status

    # если встретили правый край, то статус wall
    if text_width + pointer['x'] >= IMAGE_WIDTH:
        status = 'wall'

    return status


# дефолтные окружности
CIRCLES = ((100, 200, 50), (50, 100, 40), (200, 700, 10), (400, 600, 50))
# считываем шрифт
current_dir = os.getcwd()
os.chdir(__file__.removesuffix('wrap.py'))
font = ImageFont.truetype('Roboto-Light.ttf', size=20)
os.chdir(current_dir)
SPACE_SIZE, TEXT_HEIGHT = font.getsize(' ')
IMAGE_WIDTH, IMAGE_HEIGHT = 600, 900
INDENT = 20  # отступ вокруг надписи в пикселях


def get_image(circles: list[tuple[int, int, int]] = CIRCLES, text: str = 'Мама мыла раму'):
    out = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))
    d = ImageDraw.Draw(out)
    # положение на картинке
    pointer = {'x': 0, 'y': 0}
    while True:
        result = draw_text(pointer, text, d, circles)
        # если успешно продолжаем
        if result == 'success':
            continue
        # если конец, то выходим
        elif result == 'end':
            break
        # если встретили правый край или пересечение с кругом
        elif result == 'wall' or result == 'circle':
            # разделяем текст на слова
            words = text.split()
            word_i = 0
            # делаем все что выше, но для каждого слова
            while word_i < len(words):
                result = draw_text(pointer, words[word_i], d, circles)
                if result == 'success':
                    word_i += 1
                elif result == 'end':
                    break
                # если пересечение с кругом, то продвигаемся правее
                elif result == 'circle':
                    pointer['x'] += SPACE_SIZE
                # если встретили стену, то идем ниже и в левый конец
                elif result == 'wall':
                    pointer['y'] += TEXT_HEIGHT
                    pointer['x'] = 0
    # для прорисовки кругов
    # for circle in circles:
    #     d.ellipse([circle[0] - circle[2], circle[1] - circle[2], circle[0] + circle[2], circle[1] + circle[2]],
    #               outline='black')
    return out

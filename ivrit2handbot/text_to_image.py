from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def hebrew_to_image(text, output_path="output.png"):
    # Подготовка текста
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)

    # Создаём изображение
    img = Image.new('RGB', (600, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Используем стандартный шрифт (можно заменить на рукописный позже)
    font = ImageFont.truetype("arial.ttf", 32)

    # Отображаем текст
    draw.text((10, 30), bidi_text, font=font, fill=(0, 0, 0))

    # Сохраняем
    img.save(output_path)
    return output_path

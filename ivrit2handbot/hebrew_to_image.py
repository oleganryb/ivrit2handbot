from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import os

def create_hebrew_image(text, output_path="output.png"):
    # Подготовка ивритского текста
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)

    # Настройки
    font_path = os.path.join(os.path.dirname(__file__), "KtavYadCLM-MediumItalic.otf")
    font_size = 48
    max_width = 1000
    padding = 50
    spacing = 10

    font = ImageFont.truetype(font_path, font_size)

    # Временный холст для замеров
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    # Разбивка на строки вручную
    words = bidi_text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        w = draw.textlength(test_line, font=font)
        if w <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    # Размер изображения
    line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines]
    text_height = sum(line_heights) + spacing * (len(lines) - 1)
    width = max_width + padding * 2
    height = text_height + padding * 2

    # Создание изображения
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Отрисовка текста справа налево
    y = padding
    for line in lines:
        line_width = draw.textlength(line, font=font)
        x = width - padding - line_width
        draw.text((x, y), line, fill="black", font=font)
        y += font_size + spacing

    image.save(output_path)
    print(f"✅ Изображение сохранено как: {output_path}")

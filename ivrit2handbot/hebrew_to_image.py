from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display


def create_hebrew_image(text, output_path="output.png"):
    # Подготовка ивритского текста
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)

    # Настройки
    import os
    font_path = os.path.join(os.path.dirname(__file__),
                             "KtavYadCLM-MediumItalic.otf")
    font_size = 48
    max_width = 1000  # Максимальная ширина изображения
    padding = 50

    font = ImageFont.truetype(font_path, font_size)

    # Создаем временный объект для замера
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    # Перенос строк вручную
    words = bidi_text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    # Итоговый текст
    final_text = "\n".join(lines[::-1])

    # Размер итогового изображения
    bbox = draw.multiline_textbbox((0, 0), final_text, font=font, spacing=10)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    width = text_width + padding * 2
    height = text_height + padding * 2

    # Создание картинки
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.multiline_text((padding, padding),
                        final_text,
                        fill="black",
                        font=font,
                        align="right",
                        spacing=10)

    image.save(output_path)
    print(f"✅ Изображение сохранено как: {output_path}")



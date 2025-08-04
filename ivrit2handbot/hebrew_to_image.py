import os
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

def create_hebrew_image(text, output_path="output.png"):
    # Обработка ивритского текста (RTL)
    bidi_text = get_display(text)[::-1]  # reshape НЕ нужен для иврита

    # Путь к шрифту — надёжный (относительно этого файла)
    font_path = os.path.join(os.path.dirname(__file__), "KtavYadCLM-MediumItalic.otf")
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"❌ Шрифт не найден: {font_path}")

    font_size = 48
    max_width = 1000
    padding = 50
    font = ImageFont.truetype(font_path, font_size)

    # Создание "чернового" объекта для измерений
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    # Перенос строк вручную
    words = bidi_text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        w = draw.textbbox((0, 0), test_line, font=font)[2]
        if w <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    # Собираем текст
    final_text = "\n".join(lines[::-1])  # строки RTL сверху вниз

    # Размер итогового изображения
    bbox = draw.multiline_textbbox((0, 0), final_text, font=font, spacing=10)
    width, height = bbox[2] + padding * 2, bbox[3] + padding * 2

    # Создание финального изображения
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.multiline_text((padding, padding), final_text, fill="black",
                        font=font, align="right", spacing=10)

    image.save(output_path)
    print(f"✅ Сохранено как: {output_path}")


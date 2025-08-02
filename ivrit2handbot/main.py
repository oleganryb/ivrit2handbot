import os
from dotenv import load_dotenv
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (ApplicationBuilder, MessageHandler, filters,
                          CommandHandler, ContextTypes, ConversationHandler)
from openai import OpenAI
from hebrew_to_image import create_hebrew_image

# Загрузка переменных окружения
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_API_TOKEN")

# Инициализация OpenAI
client = OpenAI(api_key=openai_api_key)

# Состояния для ConversationHandler
CHOOSING_MODE, TRANSLATING = range(2)

# Клавиатура выбора режима
mode_keyboard = [["🇮🇱 Иврит → рукописный"],
                 ["🇷🇺 Русский → иврит → рукописный"]]
mode_markup = ReplyKeyboardMarkup(mode_keyboard, resize_keyboard=True)


# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Выбери режим перевода:",
                                    reply_markup=mode_markup)
    return CHOOSING_MODE


# Обработка выбора режима
async def choose_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = update.message.text
    context.user_data["mode"] = mode
    await update.message.reply_text("Отправь мне текст для обработки.",
                                    reply_markup=ReplyKeyboardMarkup(
                                        [["🔄 Сменить режим"]],
                                        resize_keyboard=True))
    return TRANSLATING


# Обработка текста пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔄 Сменить режим":
        await update.message.reply_text("Выбери режим заново:",
                                        reply_markup=mode_markup)
        return CHOOSING_MODE

    mode = context.user_data.get("mode")
    output_path = "hebrew_output.png"

    if mode == "🇮🇱 Иврит → рукописный":
        create_hebrew_image(text, output_path)

    elif mode == "🇷🇺 Русский → иврит → рукописный":
        # Переводим русский текст в иврит через OpenAI
        prompt = f"Переведи следующий русский текст на современный иврит:\n\n{text}"
        response = client.chat.completions.create(model="gpt-4",
                                                  messages=[{
                                                      "role": "user",
                                                      "content": prompt
                                                  }])
        hebrew_translation = response.choices[0].message.content.strip()
        create_hebrew_image(hebrew_translation, output_path)

    else:
        await update.message.reply_text(
            "Пожалуйста, сначала выбери режим с помощью /start.")
        return CHOOSING_MODE

    # Отправляем картинку
    with open(output_path, "rb") as img:
        await update.message.reply_photo(photo=img)
    return TRANSLATING


# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ок, пока!",
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# Запуск приложения
app = ApplicationBuilder().token(telegram_token).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING_MODE:
        [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_mode)],
        TRANSLATING:
        [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

print("🤖 Бот запущен и ждёт сообщений...")

from keep_alive import keep_alive
import threading
import os

if name == "__main__":
    # Запуск Flask-сервера для аптайма
    threading.Thread(target=keep_alive).start()

    print("🤖 Бот запущен и ждёт сообщений...")
    app.run_polling()

import asyncio
import os
import logging
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- 1. RENDER UCHUN KICHIK FLASK SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run_flask():
    # Render taqdim etgan PORT bo'yicha tinglaydi
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- 2. BOT QISMI ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "BU_YERGA_TOKEN_YOKI_ENV_O'ZGARUVCHISI")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Bot xizmatingizda.")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Render portni topishi uchun Flask-ni alohida potokda ishga tushiramiz
    keep_alive()
    
    # Telegram botni polling rejimida ishga tushiramiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

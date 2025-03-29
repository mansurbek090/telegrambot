import asyncio
import logging
import re  # Matndan ma'lumot ajratish uchun

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = "7995252330:AAE6I_spf1CiEmpYDl0HlrAUPlyLVkOw1AY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

kino_baza = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("✅ Xush kelibsiz! 🎬 Kino kodini kiriting.")

@dp.message(F.video)
async def receive_video(message: Message):
    file_id = message.video.file_id
    duration = message.video.duration  
    caption = message.caption if message.caption else "Noma'lum"

    def get_info(regex, text):
        match = re.search(regex, text, re.IGNORECASE)
        return match.group(1).strip() if match else "Noma'lum"

    kino_data = {
        "file_id": file_id,
        "name": get_info(r"Nomi:\s*(.+)", caption),
        "country": get_info(r"Davlati:\s*(.+)", caption),
        "format": get_info(r"Formati:\s*(.+)", caption),
        "genre": get_info(r"Janri:\s*(.+)", caption),
        "year": get_info(r"Sanasi:\s*(.+)", caption),
        "duration_text": get_info(r"Davomiyligi:\s*(.+)", caption) if "Davomiyligi:" in caption else f"{duration // 60} min"
    }

    kino_code = str(len(kino_baza) + 1)
    kino_baza[kino_code] = kino_data

    await message.answer(
        f"✅ Kino saqlandi!\n"
        f"🎬 Kino nomi: {kino_data['name']}\n"
        f"🌎 Davlati: {kino_data['country']}\n"
        f"💽 Formati: {kino_data['format']}\n"
        f"🎭 Janri: {kino_data['genre']}\n"
        f"📅 Sana: {kino_data['year']}\n"
        f"⏳ Davomiyligi: {kino_data['duration_text']}\n"
        f"🆔 Kino kodi: `{kino_code}`\n\n"
        f"🤖 Bizning bot: @tarjima_uztvbot"
        f"Bu kodni yozsangiz, kinoni yuklab olishingiz mumkin."
    )

@dp.message(F.text)
async def send_video(message: Message):
    kod = message.text.strip()

    if kod in kino_baza:
        kino = kino_baza[kod]
        await message.answer_video(
            video=kino["file_id"],
            caption=f"🎬 Kino nomi: {kino['name']}\n"
                    f"🌎 Davlat: {kino['country']}\n"
                    f"💽 Format: {kino['format']}\n"
                    f"🎭 Janr: {kino['genre']}\n"
                    f"📅 Sana: {kino['year']}\n"
                    f"⏳ Davomiyligi: {kino['duration_text']}\n"
                    f"🆔 Kino kodi: `{kod}`\n\n"
                    f"🤖 Bizning bot: @tarjima_uztvbot"
                    f"📽️ Yaxshi tomosha qiling! 🍿"
        )
    else:
        await message.answer("⚠️ Bunday kod topilmadi. To‘g‘ri kod kiriting.")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

BOT_TOKEN = "7995252330:AAE6I_spf1CiEmpYDl0HlrAUPlyLVkOw1AY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

kino_baza = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("✅ Xush kelibsiz! Kino ko'dini yuboring")

@dp.message(Command("settings"))
async def cmd_settings(message: Message):
    if not kino_baza:
        await message.answer("🎬 Hozircha hech qanday kino saqlanmagan.")
        return

    buttons = []
    for code, data in kino_baza.items():
        buttons.append(
            [InlineKeyboardButton(text=f"❌ {data['name']}", callback_data=f"delete_{code}")]
        )
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("🗂 Kinolar ro'yxati (o'chirish uchun bos):", reply_markup=markup)

@dp.callback_query(F.data.startswith("delete_"))
async def delete_kino(callback: CallbackQuery):
    code = callback.data.split("_")[1]
    if code in kino_baza:
        del kino_baza[code]
        await callback.answer("🗑 O‘chirildi!")
        await callback.message.edit_text("✅ Kino o‘chirildi.")
    else:
        await callback.answer("⚠️ Bunday kod topilmadi.")

@dp.message(F.video)
async def receive_video(message: Message):
    file_id = message.video.file_id
    caption = message.caption if message.caption else "Noma'lum"

    name = caption.splitlines()[0] if caption else "Noma'lum"

    kino_data = {
        "file_id": file_id,
        "name": name,
    }

    kino_code = str(len(kino_baza) + 1)
    kino_baza[kino_code] = kino_data

    await message.answer(
        f"✅ Kino saqlandi!\n"
        f"🎬 Nomi: {name}\n"
        f"🆔 Kod: `{kino_code}`\n\n"
        f"🤖 Bot: @tarjima_uztvbot\n"
        f"📥 Kodni yuborsangiz kinoni yuklab olasiz."
    )

@dp.message(F.text)
async def send_video(message: Message):
    kod = message.text.strip()
    if kod in kino_baza:
        kino = kino_baza[kod]
        await message.answer_video(
            video=kino["file_id"],
            caption=f"🎬 Nomi: {kino['name']}\n🆔 Kod: {kod}\n\n📽️ Yaxshi tomosha qiling!"
        )
    else:
        await message.answer("⚠️ Bunday kod topilmadi.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

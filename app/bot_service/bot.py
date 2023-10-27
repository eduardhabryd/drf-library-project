import os

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


async def borrowing_creation_handler(borrowing) -> None:
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    text = (
        f"User {borrowing.user} took {hbold(borrowing.book.title)} book\n"
        + f"Expected return date: {borrowing.expected_return_date}\n"
        + f"{borrowing.book.inventory} books left"
    )
    await bot.send_message(chat_id=CHAT_ID, text=text)
    await bot.session.close()


async def send_telegram_notification(text):
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.send_message(chat_id=CHAT_ID, text=text)
    await bot.session.close()

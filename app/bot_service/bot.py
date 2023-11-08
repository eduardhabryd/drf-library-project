import os
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

from borrowings.models import Borrowing

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


async def successful_notification_handler(borrowing) -> None:
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    text = (
        f"User {borrowing.user} successfully paid for book "
        f"{hbold(borrowing.book.title)}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=text)
    await bot.session.close()


async def borrowing_overdue_notification_handler() -> None:
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

    text = ""

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=datetime.now() + timedelta(days=1),
        actual_return_date=None,
    )

    if not overdue_borrowings.exists():
        text = "No borrowings overdue today!"
        await bot.send_message(chat_id=CHAT_ID, text=text)
    else:
        for borrowing in overdue_borrowings:
            text += f"User {borrowing.user} took {hbold(borrowing.book.title)} book\n"
            text += f"Expected return date: {borrowing.expected_return_date}\n"
            text += f"{borrowing.book.inventory} books left\n\n"
            await bot.send_message(chat_id=CHAT_ID, text=text)

    await bot.session.close()


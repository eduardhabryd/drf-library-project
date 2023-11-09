import asyncio
from datetime import datetime, timedelta

from celery import shared_task
from aiogram.utils.markdown import hbold

from app.bot_service.bot import borrowing_overdue_notification_handler
from borrowings.models import Borrowing


@shared_task
def check_borrowing_overdue():
    text = ""

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=datetime.now() + timedelta(days=1),
        actual_return_date=None,
    )

    if not overdue_borrowings.exists():
        text = "No borrowings overdue today!"
        asyncio.run(borrowing_overdue_notification_handler(text))
    else:
        for borrowing in overdue_borrowings:
            text += (
                f"User {borrowing.user} overdue book: "
                f"{hbold(borrowing.book.title)}\n"
            )
            text += f"Expected return date: {borrowing.expected_return_date}\n"
            text += f"{borrowing.book.inventory} books left\n\n"
            text += (
                f"{borrowing.user} please return the book! "
                f"Or we will find you!"
            )
            asyncio.run(borrowing_overdue_notification_handler(text))

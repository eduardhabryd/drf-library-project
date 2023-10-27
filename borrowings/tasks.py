from django.utils import timezone
from .models import Borrowing
from app.bot_service.bot import send_telegram_notification
from aiogram.utils.markdown import hbold


def check_overdue_borrowings():
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow,
        actual_return_date__isnull=True
    )

    if overdue_borrowings.exists():
        for borrowing in overdue_borrowings:
            text = (
                f"User {borrowing.user} took {hbold(borrowing.book.title)} book\n"
                + f"Expected return date: {borrowing.expected_return_date}\n"
                + f"{borrowing.book.inventory} books left"
            )
            send_telegram_notification(text)
    else:
        send_telegram_notification("No borrowings overdue today!")

import asyncio

from celery import shared_task

from app.bot_service.bot import borrowing_overdue_notification_handler


@shared_task
def check_borrowing_overdue():
    asyncio.run(borrowing_overdue_notification_handler())

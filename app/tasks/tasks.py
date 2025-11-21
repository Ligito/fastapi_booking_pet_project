import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_config import celery
from PIL import Image
from pathlib import Path
from time import sleep


from app.tasks.email_templates import create_booking_confirmation_template
from app.tasks.telegram_templates import format_booking_message, send_message_to_telegram


@celery.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    # im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
    # im_resized_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")

@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    # заменяем email_to на email_to_mock т.к. в БД почта тестовая и сейчас использую свою (в реальном прокте нужно указывать email_to)
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


# CHAT_ID захардкожен на мой что бы не обновлять БС(возможная доработка)
@celery.task
def send_booking_confirmation_telegram(
        booking: dict,
        chat_id: str
):
    """
    Celery-задача для отправки уведомления о бронировании в Telegram.
    """
    message = format_booking_message(booking)
    send_message_to_telegram(message, chat_id)

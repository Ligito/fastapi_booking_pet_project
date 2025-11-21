from app.config import settings
import requests


def send_message_to_telegram(text: str, chat_id: str):
    """
    Отправляет сообщение в Telegram с использованием Bot API.
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'  # Поддержка HTML-разметки: <b>, <i>, и т.д.
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to send message to Telegram: {response.text}")

def format_booking_message(booking: dict):
    """
    Формирует HTML-подобное сообщение для Telegram (с поддержкой тегов <b>, <i> и т.п.)
    Аналогичная логика, как в create_booking_confirmation_template, но для Telegram.
    """
    message = f"""
✅ Подтверждение бронирования:
<b>ID брони:</b> {booking.get('id', 'N/A')}
<b>Комната:</b> {booking.get('room_id', 'N/A')}
<b>Пользователь:</b> {booking.get('user_id', 'N/A')}
<b>Дата заезда:</b> {booking.get('date_from', 'N/A')}
<b>Дата выезда:</b> {booking.get('date_to', 'N/A')}
<b>Общая стоимость:</b> {booking.get('total_cost', 'N/A')} руб.
    """.strip()
    return message
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from bot.models import BotUserToken
from bot.utils import generate_bot_token
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '7216315903:AAEJkrIL0_YTCsGg7oPWiLbjHHDVqumkXwk'

bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()

async def authenticate_user(token):
    try:
        bot_user = await BotUserToken.objects.aget(token=token, is_active=True)
        return bot_user.user
    except BotUserToken.DoesNotExist:
        return None

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Login", callback_data='login')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please login:', reply_markup=reply_markup)
    logger.info("Login button sent.")

async def login(update: Update, context: CallbackContext) -> None:
    logger.info("Login callback received.")
    query = update.callback_query
    await query.answer()

    user = query.from_user
    token = generate_bot_token(user)
    await query.edit_message_text(text=f"Your login token is: {token}")
    logger.info(f"Login token sent to user {user.id}.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    user = await authenticate_user(text)
    if user:
        await update.message.reply_text("Authenticated successfully!")
        logger.info(f"User {user.id} authenticated successfully.")
    else:
        await update.message.reply_text("Authentication failed.")
        logger.info(f"Authentication failed for token: {text}")

application.add_handler(CommandHandler('start', start))
application.add_handler(CallbackQueryHandler(login, pattern='login'))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

def send_order_notification(order):
    bot_users = BotUserToken.objects.filter(is_active=True)
    for bot_user in bot_users:
        user_chat_id = bot_user.user.profile.chat_id
        if user_chat_id:
            message = (
                f"Нове замовлення №{order.id}\n"
                f"Клієнт: {order.first_name} {order.last_name}\n"
                f"Сума: {order.total_price} грн\n"
                f"Статус: {order.status}\n"
                f"Спосіб доставки: {order.get_delivery_method_display()}\n"
                f"Спосіб оплати: {order.get_payment_method_display()}\n"
                f"Контактний телефон: {order.contact_number}\n"
                f"Адреса доставки: {order.delivery_address}\n"
                f"Коментар: {order.comment}\n"
            )
            bot.send_message(chat_id=user_chat_id, text=message)

async def main():
    logger.info("Bot is starting...")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

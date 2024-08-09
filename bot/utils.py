# bot/utils.py
import secrets
from bot.models import BotUserToken

def generate_bot_token(user):
    token = secrets.token_urlsafe(32)
    bot_token, created = BotUserToken.objects.get_or_create(user=user)
    bot_token.token = token
    bot_token.save()
    return token

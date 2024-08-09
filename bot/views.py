# bot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from bot.bot import send_order_notification

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        update = Update.de_json(request.body, bot)
        # Обробка оновлення
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request method'})

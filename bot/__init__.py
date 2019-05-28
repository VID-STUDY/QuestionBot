from flask import Blueprint, request, abort
import os
from config import Config
from telebot.types import Update
from application import telegram_bot


bp = Blueprint('bot', __name__)

if 'PRODUCTION' in os.environ:
    @bp.route(Config.WEBHOOK_URL_PATH, methods=['POST'])
    def receive_update():
        if request.headers.get('Content-Type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = Update.de_json(json_string)
            telegram_bot.process_new_updates([update])
            return '', 200
        else:
            abort(400)

    telegram_bot.remove_webhook()
    telegram_bot.set_webhook(Config.WEBHOOK_URL_BASE + Config.WEBHOOK_URL_PATH)

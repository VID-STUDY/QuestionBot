"""
Main application package. The app initialize here
"""
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sslify import SSLify
from flask_cors import CORS
from telebot import TeleBot, logger
from application.resources import strings
import os
import logging

telegram_bot = TeleBot(Config.API_TOKEN, threaded=False)

app = Flask(__name__)
if 'PRODUCTION' in os.environ:
    # if app starts in production, give it ssl-certificate
    sslify = SSLify(app)
else:
    cors = CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

loginManager = LoginManager(app)
loginManager.login_view = 'auth.login'
loginManager.login_message = strings.get_string('authentication.required')
loginManager.login_message_category = 'error'

import application.core.models

# from application.bot import bp as bot_bp
# app.register_blueprint(bot_bp)
from application.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

if 'ADMIN_DEV' not in os.environ and 'PRODUCTION' not in os.environ:
    # When bot needs to be developed or tested, this configuration starts with long polling
    logger.setLevel(logging.DEBUG)
    telegram_bot.remove_webhook()
    telegram_bot.polling(none_stop=True)

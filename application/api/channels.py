from application import telegram_bot
from application.api import bp
from application import telegram_bot
from application.core.models import Channel
from application.utils import api as apiutils
import re
from flask import jsonify, request
from telebot.apihelper import ApiException


@bp.route('/channels', methods=['POST'])
def add_channel():
    channel_name = request.get_json()['channelName']
    url_re = r'https?:\/\/(t(elegram)?\.me|telegram\.org)\/([a-z0-9\_]){5,32}'
    if re.match(url_re, channel_name):
        channel_name = '@' + channel_name[channel_name.rfind('/')+1:]
    if Channel.query.filter(Channel.channel_name == channel_name[1:]).count() > 0:
        error = apiutils.error_message(400, 'Такой канал уже добавлен')
        return jsonify(error), 400
    try:
        channel = telegram_bot.get_chat(channel_name)
    except ApiException:
        error = apiutils.error_message(400, 'Указанный канал отсутствует, либо является привытаным')
        return jsonify(error), 400
    if channel.type != 'channel':
        error = apiutils.error_message(400, 'Указанный юзернейм не является каналом')
        return jsonify(error), 400
    try:
        sent_message = telegram_bot.send_message(channel_name, 'Test', disable_notification=True)
        telegram_bot.delete_message(sent_message.chat.id, sent_message.message_id)
    except ApiException:
        error = apiutils.error_message(400, 'Бот не имеет доступа к отправке и удалению сообщений')
        return jsonify(error), 400
    new_channel = Channel.add(channel.username, channel.title, sent_message.chat.id)
    return jsonify(new_channel.to_dict()), 200


@bp.route('/channels', methods=['GET'])
def list_channels():
    channels = Channel.query.all()
    response = [c.to_dict() for c in channels]
    return jsonify(response), 200

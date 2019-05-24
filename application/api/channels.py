from application.api import bp
from application import telegram_bot
from application.core.models import Channel
from application.utils import api as apiutils
import re
from flask import jsonify, request
from telebot.apihelper import ApiException


@bp.route('/channels/', methods=['POST'])
def add_channel():
    channel_name = request.get_json()['channelName']
    url_re = r'https?:\/\/(t(elegram)?\.me|telegram\.org)\/([a-z0-9\_]){5,32}'
    if re.match(url_re, channel_name):
        channel_name = '@' + channel_name[channel_name.rfind('/')+1:]
    try:
        channel = telegram_bot.get_chat(channel_name)
    except ApiException:
        error = apiutils.error_message(400, 'Указанный канал отсутствует, либо является привытаным')
        return jsonify(error), 400
    if channel.type != 'channel':
        error = apiutils.error_message(400, 'Указанный юзернейм не является каналом')
        return jsonify(error), 400
    new_channel = Channel.add(channel.username, channel.title)
    return jsonify(new_channel.to_dict()), 200

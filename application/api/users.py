from . import bp
from flask import jsonify
from flask_login import current_user
from application.core.models import Channel, BotUser
from application.utils import api as apiutils


@bp.route('/channels/<string:channel_name>/users', methods=['GET'])
def get_channel_members(channel_name):
    channel = Channel.get_by_name(channel_name)
    if not channel:
        error = apiutils.error_message(404, 'Такой канал не зарегистрирован')
        return jsonify(error), 404
    members = channel.members.all()
    return jsonify([m.to_dict() for m in members]), 200


@bp.route('/channels/<string:channel_name>/users/<int:user_id>', methods=['GET'])
def user(channel_name: str, user_id: int):
    channel, user = BotUser.get_by_id_and_channel_name(channel_name, user_id)
    if not user:
        error = apiutils.error_message(404, 'Такой пользователь не принимал участия в опросах')
        return jsonify(error), 404
    return jsonify(user.to_dict(include_answers=True)), 200


@bp.route('/users/authenticated', methods=['GET'])
def get_authenticated_user():
    return {
        'email': current_user.email
    }

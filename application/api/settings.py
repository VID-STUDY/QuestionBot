from . import bp
from flask import jsonify, request
from application.core import schedule
import settings


@bp.route('/settings', methods=['GET'])
def get_settings():
    return jsonify({
        'rightAnswerPoints': settings.get_right_answer_points()
    }), 200


@bp.route('/settings', methods=['POST'])
def set_settings():
    data = request.get_json()
    settings.set_right_answer_points(data['rightAnswerPoints'])
    return '', 201


@bp.route('/settings/stopBot', methods=['PUT'])
def stop_bot():
    schedule.stop_all_jobs()
    settings.set_bot_state(settings.BotStates.STOPPED)
    return jsonify({'state': settings.BotStates.STOPPED}), 200


@bp.route('settings/startBot', methods=['PUT'])
def start_bot():
    if settings.get_bot_state() == settings.BotStates.PAUSED:
        schedule.resume_scheduler()
    settings.set_bot_state(settings.BotStates.WORK)
    return jsonify({'state': settings.BotStates.WORK}), 200


@bp.route('settings/pauseBot', methods=['PUT'])
def pause_bot():
    schedule.pause_scheduler()
    settings.set_bot_state(settings.BotStates.PAUSED)
    return jsonify({'state': settings.BotStates.PAUSED}), 200

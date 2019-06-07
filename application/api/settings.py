from . import bp
from flask import jsonify, request
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

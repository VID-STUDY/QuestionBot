from application.api import bp
from application.core.models import Quiz, Channel
from application.utils import api as apiutils
from flask import jsonify, request


@bp.route('/channels/<string:channel_name>/quizzes', methods=['GET'])
def get_channel_quizzes(channel_name: str):
    quizzes = Channel.get_quizzes_by_channel_name(channel_name)
    if quizzes is None:
        error = apiutils.error_message(400, 'Такой канал не зарегистрирован')
        return jsonify(error), 400
    return jsonify([q.to_dict() for q in quizzes]), 200


@bp.route('/channels/<string:channel_name>/quizzes', methods=['POST'])
def create_quiz(channel_name: str):
    data = request.get_json()
    channel = Channel.get_by_name(channel_name)
    new_quiz = Quiz.create(data, channel)
    return jsonify(new_quiz.to_dict()), 200


@bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def remove_quiz(quiz_id: int):
    Quiz.remove(quiz_id)
    return '', 201


@bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz_by_id(quiz_id: int):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz:
        error = apiutils.error_message(404, "Викторина не найдена")
        return jsonify(error), 404
    return jsonify(quiz.to_dict()), 200


@bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id: int):
    data = request.get_json()
    quiz = Quiz.update(quiz_id, data)
    return jsonify(quiz.to_dict()), 200

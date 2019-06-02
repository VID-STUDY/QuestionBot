from application.api import bp
from application.core.models import Test, Quiz
from application.utils import api as apiutils
from flask import jsonify, request


@bp.route('/quizzes/<int:quiz_id>/tests', methods=['GET'])
def get_channel_tests(quiz_id: str):
    tests = Quiz.get_tests_by_quiz_id(quiz_id)
    if tests is None:
        error = apiutils.error_message(404, 'Викторина не найдена')
        return jsonify(error), 404
    return jsonify([test.to_dict() for test in tests]), 200


@bp.route('/quizzes/<int:quiz_id>/tests', methods=['POST'])
def create_test(quiz_id: str):
    data = request.get_json()
    quiz = Quiz.get_by_id(quiz_id)
    new_test = Test.create(data, quiz)
    return jsonify(new_test.to_dict()), 200

@bp.route('/tests/<int:test_id>', methods=['PUT'])
def update_test(test_id: int):
    data = request.get_json()
    test = Test.update(test_id, data)
    return jsonify(test.to_dict()), 200


@bp.route('/tests/<int:test_id>', methods=['GET'])
def get_test_by_id(test_id: int):
    test = Test.get_by_id(test_id)
    if not test:
        error = apiutils.error_message(404, 'Такой тест не найден')
        return jsonify(error), 404
    return jsonify(test.to_dict()), 200


@bp.route('/tests/<int:test_id>', methods=['DELETE'])
def remove_test(test_id: int):
    Test.remove(test_id)
    return '', 201

from application.api import bp
from application.core.models import Test, Quiz
from application.utils import api as apiutils
from flask import jsonify, request
from application.core import schedule


@bp.route('/tests', methods=['POST'])
def create_test():
    data = request.get_json()
    new_test = Test.create(data)
    schedule.add_test_to_publish(new_test.id, new_test.publish_date)
    return jsonify(new_test.to_dict()), 200


@bp.route('/tests/<int:test_id>', methods=['PUT'])
def update_test(test_id: int):
    data = request.get_json()
    test = Test.update(test_id, data)
    schedule.update_test_date_publish(test.id, test.publish_date)
    return jsonify(test.to_dict()), 200


@bp.route('/tests/<int:test_id>/file', methods=['POST'])
def save_test_file(test_id: int):
    if 'file' not in request.files:
        error = apiutils.error_message(400, 'Файл не выбран')
        return jsonify(error)
    file = request.files['file']
    if file.filename != '':
        Test.save_file(test_id, file)
        return '', 201
    error = apiutils.error_message(400, 'Файл не выбран')
    return jsonify(error), 400


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
    schedule.remove_test_from_publishing(test_id)
    return '', 201

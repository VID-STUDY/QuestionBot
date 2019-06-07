from . import bp
from flask import jsonify
from application.utils import api as apiutils
from application.core.models import Channel


def _sort_tests(tests: list):
    tests.sort(key=lambda t: t.answers.count(), reverse=True)


@bp.route('/channels/<int:channel_name>/rating', methods=['GET'])
def channel_ratings(channel_name: str):
    quizzes = Channel.get_quizzes_by_channel_name(channel_name)
    if quizzes is None:
        error = apiutils.error_message(404, 'Такой канал не зарегистрирован')
        return jsonify(error), 404
    return jsonify([q.to_dict(include_tests=True, sortcallback=_sort_tests) for q in quizzes]), 200

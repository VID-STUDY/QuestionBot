import json
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

_strings = json.loads(open(os.path.join(_basedir, 'strings.json'), 'r').read())


def get_string(key: str) -> str:
    return _strings.get(key, 'no_string')


def from_test(test) -> str:
    test_content = '<b>Вопрос:</b>\n'
    test_content += test.question
    return test_content

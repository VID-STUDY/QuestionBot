import json
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

_strings = json.loads(open(os.path.join(_basedir, 'strings.json'), 'r').read())


def get_string(key: str) -> str:
    return _strings.get(key, 'no_string')

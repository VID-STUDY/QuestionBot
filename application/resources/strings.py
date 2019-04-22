"""
String manager.
Use get_string method to get string by key
"""

import os
import json

_basedir = os.path.abspath(os.path.dirname(__file__))

# load strings from json
strings_json = open(os.path.join(_basedir, 'strings.json'), 'r', encoding='utf8').read()
_strings = json.loads(strings_json, encoding='utf8')


def get_string(key: str) -> str:
    """
    Get string by key
    :param key: str
    :return: str
    """
    return _strings.get(key, 'no_string')

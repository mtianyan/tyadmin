import json
import re

import django
import sys
import os
import math

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_react_tyadmin.settings")

django.setup()
from rule.models import Rule


def _name_convert_to_snake(name: str) -> str:
    """驼峰转下划线"""
    if '_' not in name:
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    else:
        raise ValueError(f'{name}字符中包含下划线，无法转换')
    return name.lower()


with open('rule.json') as fr:
    data = json.loads(fr.read())
    print(data['data'])

    for one in data['data']:
        one_data = {}
        for key, value in one.items():
            one_data[_name_convert_to_snake(key)] = value
        pp = Rule(**one_data)
        pp.save()

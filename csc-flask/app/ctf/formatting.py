# formatting.py
# Rohan Weeden
# Created: July 7, 2017

# Turns models into JSON

from collections import OrderedDict


def flag_to_dict(flag):
    d = OrderedDict([
        ("id", flag.id),
        ("name", flag.name),
        ("key", flag.key),
        ("points", flag.points),
        ("description", flag.description),
        ("hint", flag.hint)
    ])
    return d

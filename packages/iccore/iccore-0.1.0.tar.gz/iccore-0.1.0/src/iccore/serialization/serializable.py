"""
This module is for objects that can be serialized, i.e. converted into
string-like representations.
"""

import json


class Serializable:
    """
    Subclasses can implement 'serialize' to return a dict,
    which allows for a json string representation
    """

    def serialize(self) -> dict:
        return {}

    def __str__(self) -> str:
        return json.dumps(self.serialize(), indent=4)

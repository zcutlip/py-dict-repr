import os
import sys
from pprint import pprint
import json
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from py_dict_repr import DictRepr, KeyTuple  # noqa: E402


class MyArbitraryClass(DictRepr):

    _keys = [
        KeyTuple("uppercase verion", "uppercase"),
        KeyTuple("string length", "length"),
        # KeyTuple may be mixed with regular key strings
        "lowercase"
    ]

    def __init__(self, value: str):
        self._value = value

    @property
    def uppercase(self):
        return self._value.upper()

    @property
    def lowercase(self):
        return self._value.lower()

    @property
    def length(self):
        return len(self._value)

    def keys(self):
        keys = self._keys
        return keys


if __name__ == "__main__":
    myobj = MyArbitraryClass("Hello World")
    mydict = dict(myobj)
    print("mydict type: {}".format(type(mydict)))
    print("---------------------------")
    print("pretty-print:")
    print("")
    pprint(mydict, sort_dicts=False)
    print("")
    print("---------------------------")
    print("JSON:")
    print("")
    print(json.dumps(mydict, indent=2))
    print("")
    print("---------------------------")
    print("done")

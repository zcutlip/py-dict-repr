import os
import sys
from pprint import pprint

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from py_dict_repr import DictRepr  # noqa: E401


class MyArbitraryClass(DictRepr):

    _keys = ["uppercase", "length"]

    def __init__(self, value: str):
        self._value = value

    @property
    def uppercase(self):
        return self._value.upper()

    @property
    def length(self):
        return len(self._value)

    def keys(self):
        return self._keys


if __name__ == "__main__":
    myobj = MyArbitraryClass("Hello World")
    mydict = dict(myobj)
    print("mydict type: {}".format(type(mydict)))
    pprint(mydict)

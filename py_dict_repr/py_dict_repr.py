from abc import ABC, abstractmethod
from collections import OrderedDict


class KeyTuple(str):

    def __new__(cls, key, attr_name):
        return str.__new__(cls, key)

    def __init__(self, key, attr_name):
        self.attr_name = attr_name
        self.key = key


def _hooked_dict(*args, **kwargs):
    obj = _orig_dict.__new__(_orig_dict)
    try:
        iter(args)
        for arg in args:
            if hasattr(arg, "_dr_new_root"):
                arg._dr_new_root = obj
    except TypeError:
        pass
    obj.__init__(*args, **kwargs)
    # print("custom dict")
    return obj


class DictRepr(ABC):

    def __new__(cls, *args, **kwargs):
        import inspect
        inspect.currentframe().f_globals['__builtins__']['dict'] = _hooked_dict
        obj = super().__new__(cls)
        obj._dr_new_root = None
        return obj

    class _DictIterator:
        def __init__(self, obj):
            self._obj = obj
            self.idx = 0

        def __iter__(self):
            return self

        def __next__(self):
            ret = None
            if self.idx < len(self._obj.keys()):
                key = self._obj.keys()[self.idx]
                val = self._obj[key]
                ret = (key, val)
                self.idx += 1
            else:
                self.idx = 0
                raise StopIteration

            return ret

    def __iter__(self):
        return self._DictIterator(self)

    def __getitem__(self, item):
        if isinstance(item, KeyTuple):
            item = item.attr_name
        try:
            thing = getattr(self, item)
        except AttributeError as ae:
            raise KeyError(item) from ae

        return self._convert(thing)

    def _convert(self, obj):
        if isinstance(obj, DictRepr):
            converted = dict(obj)
        elif isinstance(obj, dict):
            converted = self._convert_dict(obj)
        elif isinstance(obj, (list, tuple, set)):
            converted = self._convert_sequence(obj)
        else:
            converted = obj
        return converted

    def _convert_dict(self, obj):
        if isinstance(obj, OrderedDict):
            converted = OrderedDict()
        else:
            converted = dict()

        for k, v in obj.items():
            converted[k] = self._convert(v)

        return converted

    def _convert_sequence(self, obj):
        if isinstance(obj, list):
            converted = []
            for thing in obj:
                thing = self._convert(thing)
                converted.append(thing)
        elif isinstance(obj, tuple):
            converted = []
            for thing in obj:
                thing = self._convert(thing)
                converted.append(thing)
            converted = tuple(converted)
        elif isinstance(obj, set):
            _list = list(obj)
            converted = []
            for thing in _list:
                thing = self._convert(thing)
                converted.append(thing)
            converted = set(converted)
        else:
            raise TypeError("not a sequence", obj)

        return converted

    def items(self):
        return ((k, self[k]) for k in self.keys())

    @abstractmethod
    def keys(self):
        raise NotImplementedError

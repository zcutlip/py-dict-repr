import copy
from abc import ABC, abstractmethod


class GraphCycleException(Exception):
    pass


class KeyTuple(str):

    def __new__(cls, key, attr_name):
        return str.__new__(cls, key)

    def __init__(self, key, attr_name):
        self.attr_name = attr_name
        self.key = key


class DictRepr(ABC):

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

    @property
    def dr_new_root(self):
        if not hasattr(self, "_dr_new_root"):
            self._dr_new_root = None
        return self._dr_new_root

    @dr_new_root.setter
    def dr_new_root(self, root_obj):
        self.dr_new_root = root_obj

    def __iter__(self):
        return self._DictIterator(self)

    def __getitem__(self, item, memo=None, convert=True):
        """
        internal-use-only kwargs:
        memo: a memo dict that gets passed in once we've started a conversion to
              ensure we don't convert an object twice
        convert: if a conversion function is getting items, we don't need to convert them also
        """
        if isinstance(item, KeyTuple):
            item = item.attr_name
        try:
            thing = getattr(self, item)
        except AttributeError as ae:
            raise KeyError(item) from ae
        if convert:
            converted = self._convert(thing, memo)
        else:
            # we don't need to convert if the items were already being retrieved for conversion
            converted = thing

        return converted

    def _convert(self, obj, memo=None):
        if memo is None:
            if self.dr_new_root is None:
                self_convert = GraphCycleException(f"Graph cycle referencing outer-most object: {self}")
            else:
                self_convert = self.dr_new_root
            memo = {id(self): self_convert}
        try:
            converted = memo[id(obj)]

        except KeyError:
            converted = None
        if isinstance(converted, GraphCycleException):
            raise converted
        if obj is None:
            converted = obj
        elif isinstance(obj, DictRepr):
            if converted is None:
                converted = self._convert_dict_repr(obj, memo)
            else:
                print("converted")
        elif isinstance(obj, dict):
            if converted is None:
                converted = self._convert_dict(obj, memo)
        elif isinstance(obj, tuple):
            # no need to copy tuple objects becuase they don't get memoized
            converted = self._convert_tuple(obj, memo)
        elif isinstance(obj, set):
            if converted is not None:
                converted = copy.copy(converted)
            else:
                converted = self._convert_set(obj, memo)
        elif isinstance(obj, list):
            if converted is not None:
                converted = copy.copy(converted)
            else:
                converted = self._convert_list(obj, memo)
        else:
            # TODO: probably need to copy obj
            converted = obj

        return converted

    def _convert_dict_repr(self, obj, memo):
        converted = {}
        memo[id(obj)] = converted
        for k, v in obj.items(memo=memo, convert=False):
            # TODO: convert keys as well
            conv = self._convert(v, memo)
            converted[k] = conv

        return converted

    def _convert_dict(self, obj, memo):
        dict_type = type(obj)
        converted = dict_type()
        memo[id(obj)] = converted
        for k, v in obj.items():
            # TODO: convert keys as well
            converted[k] = self._convert(v, memo)

        return converted

    def _convert_set(self, obj: set, memo):
        set_type = type(obj)
        converted = set_type()
        memo[id(obj)] = converted
        for thing in obj:
            converted_thing = self._convert(thing, memo)
            converted.add(converted_thing)
        return converted

    def _convert_tuple(self, obj: tuple, memo):
        _tmp = []
        for a in obj:
            c = self._convert(a, memo)
            _tmp.append(c)

        for k, j in zip(obj, _tmp):
            if k is not j:
                # something must have been converted
                # in the self._convert list comprehension above
                # must return a new tuple obj
                converted = tuple(_tmp)
                break
        else:
            # everything in obj matched everything in _tmp
            converted = obj
        return converted

    def _convert_list(self, obj, memo):
        converted = []
        memo[id(obj)] = converted
        for thing in obj:
            thing = self._convert(thing, memo)
            converted.append(thing)

        return converted

    def items(self, memo=None, convert=True):
        """
        memo: if a convert function is iterating over our items, it'll pass us a memo dict
              to pass into __getitem__()
        convert: if a convert fucntion is about to convert the items its iterating over,
                 it'll pass a flag telling __getitem__ not to do the conversion
        """
        _tmp = []
        for k in self.keys():
            v = self.__getitem__(k, memo=memo, convert=convert)
            _tmp.append((k, v))
        _items = tuple(_tmp)
        return _items

    @abstractmethod
    def keys(self):
        raise NotImplementedError


class DictWithCycles(dict):
    def __init__(self, dict_repr: DictRepr):
        dict_repr._dr_new_root = self
        super().__init__(dict_repr)

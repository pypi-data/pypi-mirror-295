import functools
import types

__all__ = ["DataList"]


class BaseDict:

    data: dict

    @functools.wraps(dict.__contains__)
    def __contains__(self, *args, **kwargs):
        data = self.data
        ans = data.__contains__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__delitem__)
    def __delitem__(self, *args, **kwargs):
        data = self.data
        ans = data.__delitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__eq__)
    def __eq__(self, *args, **kwargs):
        data = self.data
        ans = data.__eq__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__format__)
    def __format__(self, *args, **kwargs):
        data = self.data
        ans = data.__format__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__ge__)
    def __ge__(self, *args, **kwargs):
        data = self.data
        ans = data.__ge__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__getitem__)
    def __getitem__(self, *args, **kwargs):
        data = self.data
        ans = data.__getitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__gt__)
    def __gt__(self, *args, **kwargs):
        data = self.data
        ans = data.__gt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__hash__)
    def __hash__(self, *args, **kwargs):
        data = self.data
        ans = data.__hash__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__ior__)
    def __ior__(self, *args, **kwargs):
        data = self.data
        ans = data.__ior__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__iter__)
    def __iter__(self, *args, **kwargs):
        data = self.data
        ans = data.__iter__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__le__)
    def __le__(self, *args, **kwargs):
        data = self.data
        ans = data.__le__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__len__)
    def __len__(self, *args, **kwargs):
        data = self.data
        ans = data.__len__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__lt__)
    def __lt__(self, *args, **kwargs):
        data = self.data
        ans = data.__lt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__or__)
    def __or__(self, *args, **kwargs):
        data = self.data
        ans = data.__or__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__repr__)
    def __repr__(self, *args, **kwargs):
        data = self.data
        ans = data.__repr__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__reversed__)
    def __reversed__(self, *args, **kwargs):
        data = self.data
        ans = data.__reversed__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__ror__)
    def __ror__(self, *args, **kwargs):
        data = self.data
        ans = data.__ror__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__setitem__)
    def __setitem__(self, *args, **kwargs):
        data = self.data
        ans = data.__setitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__str__)
    def __str__(self, *args, **kwargs):
        data = self.data
        ans = data.__str__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.clear)
    def clear(self, *args, **kwargs):
        data = self.data
        ans = data.clear(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.copy)
    def copy(self, *args, **kwargs):
        data = self.data
        ans = data.copy(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.get)
    def get(self, *args, **kwargs):
        data = self.data
        ans = data.get(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.items)
    def items(self, *args, **kwargs):
        data = self.data
        ans = data.items(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.keys)
    def keys(self, *args, **kwargs):
        data = self.data
        ans = data.keys(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.pop)
    def pop(self, *args, **kwargs):
        data = self.data
        ans = data.pop(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.popitem)
    def popitem(self, *args, **kwargs):
        data = self.data
        ans = data.popitem(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.setdefault)
    def setdefault(self, *args, **kwargs):
        data = self.data
        ans = data.setdefault(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.update)
    def update(self, *args, **kwargs):
        data = self.data
        ans = data.update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.values)
    def values(self, *args, **kwargs):
        data = self.data
        ans = data.values(*args, **kwargs)
        self.data = data
        return ans


class BaseList:

    data: list

    @functools.wraps(list.__add__)
    def __add__(self, *args, **kwargs):
        data = self.data
        ans = data.__add__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__contains__)
    def __contains__(self, *args, **kwargs):
        data = self.data
        ans = data.__contains__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__delitem__)
    def __delitem__(self, *args, **kwargs):
        data = self.data
        ans = data.__delitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__eq__)
    def __eq__(self, *args, **kwargs):
        data = self.data
        ans = data.__eq__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__format__)
    def __format__(self, *args, **kwargs):
        data = self.data
        ans = data.__format__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__ge__)
    def __ge__(self, *args, **kwargs):
        data = self.data
        ans = data.__ge__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__getitem__)
    def __getitem__(self, *args, **kwargs):
        data = self.data
        ans = data.__getitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__gt__)
    def __gt__(self, *args, **kwargs):
        data = self.data
        ans = data.__gt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__hash__)
    def __hash__(self, *args, **kwargs):
        data = self.data
        ans = data.__hash__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__iadd__)
    def __iadd__(self, *args, **kwargs):
        data = self.data
        ans = data.__iadd__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__imul__)
    def __imul__(self, *args, **kwargs):
        data = self.data
        ans = data.__imul__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__iter__)
    def __iter__(self, *args, **kwargs):
        data = self.data
        ans = data.__iter__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__le__)
    def __le__(self, *args, **kwargs):
        data = self.data
        ans = data.__le__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__len__)
    def __len__(self, *args, **kwargs):
        data = self.data
        ans = data.__len__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__lt__)
    def __lt__(self, *args, **kwargs):
        data = self.data
        ans = data.__lt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__mul__)
    def __mul__(self, *args, **kwargs):
        data = self.data
        ans = data.__mul__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__repr__)
    def __repr__(self, *args, **kwargs):
        data = self.data
        ans = data.__repr__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__reversed__)
    def __reversed__(self, *args, **kwargs):
        data = self.data
        ans = data.__reversed__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__rmul__)
    def __rmul__(self, *args, **kwargs):
        data = self.data
        ans = data.__rmul__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__setitem__)
    def __setitem__(self, *args, **kwargs):
        data = self.data
        ans = data.__setitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__str__)
    def __str__(self, *args, **kwargs):
        data = self.data
        ans = data.__str__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.append)
    def append(self, *args, **kwargs):
        data = self.data
        ans = data.append(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.clear)
    def clear(self, *args, **kwargs):
        data = self.data
        ans = data.clear(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.copy)
    def copy(self, *args, **kwargs):
        data = self.data
        ans = data.copy(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.count)
    def count(self, *args, **kwargs):
        data = self.data
        ans = data.count(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.extend)
    def extend(self, *args, **kwargs):
        data = self.data
        ans = data.extend(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.index)
    def index(self, *args, **kwargs):
        data = self.data
        ans = data.index(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.insert)
    def insert(self, *args, **kwargs):
        data = self.data
        ans = data.insert(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.pop)
    def pop(self, *args, **kwargs):
        data = self.data
        ans = data.pop(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.remove)
    def remove(self, *args, **kwargs):
        data = self.data
        ans = data.remove(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.reverse)
    def reverse(self, *args, **kwargs):
        data = self.data
        ans = data.reverse(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.sort)
    def sort(self, *args, **kwargs):
        data = self.data
        ans = data.sort(*args, **kwargs)
        self.data = data
        return ans


class BaseSet:

    @functools.wraps(set.__and__)
    def __and__(self, *args, **kwargs):
        data = self.data
        ans = data.__and__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__contains__)
    def __contains__(self, *args, **kwargs):
        data = self.data
        ans = data.__contains__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__eq__)
    def __eq__(self, *args, **kwargs):
        data = self.data
        ans = data.__eq__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__format__)
    def __format__(self, *args, **kwargs):
        data = self.data
        ans = data.__format__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ge__)
    def __ge__(self, *args, **kwargs):
        data = self.data
        ans = data.__ge__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__gt__)
    def __gt__(self, *args, **kwargs):
        data = self.data
        ans = data.__gt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__hash__)
    def __hash__(self, *args, **kwargs):
        data = self.data
        ans = data.__hash__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__iand__)
    def __iand__(self, *args, **kwargs):
        data = self.data
        ans = data.__iand__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ior__)
    def __ior__(self, *args, **kwargs):
        data = self.data
        ans = data.__ior__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__isub__)
    def __isub__(self, *args, **kwargs):
        data = self.data
        ans = data.__isub__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__iter__)
    def __iter__(self, *args, **kwargs):
        data = self.data
        ans = data.__iter__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ixor__)
    def __ixor__(self, *args, **kwargs):
        data = self.data
        ans = data.__ixor__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__le__)
    def __le__(self, *args, **kwargs):
        data = self.data
        ans = data.__le__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__len__)
    def __len__(self, *args, **kwargs):
        data = self.data
        ans = data.__len__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__lt__)
    def __lt__(self, *args, **kwargs):
        data = self.data
        ans = data.__lt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__or__)
    def __or__(self, *args, **kwargs):
        data = self.data
        ans = data.__or__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__rand__)
    def __rand__(self, *args, **kwargs):
        data = self.data
        ans = data.__rand__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__repr__)
    def __repr__(self, *args, **kwargs):
        data = self.data
        ans = data.__repr__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ror__)
    def __ror__(self, *args, **kwargs):
        data = self.data
        ans = data.__ror__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__rsub__)
    def __rsub__(self, *args, **kwargs):
        data = self.data
        ans = data.__rsub__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__rxor__)
    def __rxor__(self, *args, **kwargs):
        data = self.data
        ans = data.__rxor__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__str__)
    def __str__(self, *args, **kwargs):
        data = self.data
        ans = data.__str__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__sub__)
    def __sub__(self, *args, **kwargs):
        data = self.data
        ans = data.__sub__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__xor__)
    def __xor__(self, *args, **kwargs):
        data = self.data
        ans = data.__xor__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.add)
    def add(self, *args, **kwargs):
        data = self.data
        ans = data.add(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.clear)
    def clear(self, *args, **kwargs):
        data = self.data
        ans = data.clear(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.copy)
    def copy(self, *args, **kwargs):
        data = self.data
        ans = data.copy(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.difference)
    def difference(self, *args, **kwargs):
        data = self.data
        ans = data.difference(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.difference_update)
    def difference_update(self, *args, **kwargs):
        data = self.data
        ans = data.difference_update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.discard)
    def discard(self, *args, **kwargs):
        data = self.data
        ans = data.discard(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.intersection)
    def intersection(self, *args, **kwargs):
        data = self.data
        ans = data.intersection(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.intersection_update)
    def intersection_update(self, *args, **kwargs):
        data = self.data
        ans = data.intersection_update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.isdisjoint)
    def isdisjoint(self, *args, **kwargs):
        data = self.data
        ans = data.isdisjoint(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.issubset)
    def issubset(self, *args, **kwargs):
        data = self.data
        ans = data.issubset(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.issuperset)
    def issuperset(self, *args, **kwargs):
        data = self.data
        ans = data.issuperset(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.pop)
    def pop(self, *args, **kwargs):
        data = self.data
        ans = data.pop(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.remove)
    def remove(self, *args, **kwargs):
        data = self.data
        ans = data.remove(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.symmetric_difference)
    def symmetric_difference(self, *args, **kwargs):
        data = self.data
        ans = data.symmetric_difference(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.symmetric_difference_update)
    def symmetric_difference_update(self, *args, **kwargs):
        data = self.data
        ans = data.symmetric_difference_update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.union)
    def union(self, *args, **kwargs):
        data = self.data
        ans = data.union(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.update)
    def update(self, *args, **kwargs):
        data = self.data
        ans = data.update(*args, **kwargs)
        self.data = data
        return ans


class OkayList(BaseList):
    @functools.wraps(list.__eq__)
    def __eq__(self, other, /):
        if type(self) != type(other):
            return False
        return self.data == other.data

    @functools.wraps(list.__ge__)
    def __ge__(self, other, /):
        other = type(self)(other)
        return other.__le__(self)

    @functools.wraps(list.__gt__)
    def __gt__(self, other, /):
        if self.__eq__(other):
            return False
        return self.__ge__(other)

    @functools.wraps(list.__hash__)
    def __hash__(self):
        raise TypeError("unhashable type: %r" % type(self).__name__)

    @functools.wraps(list.__iadd__)
    def __iadd__(self, data, /):
        self.extend(data)

    @functools.wraps(list.__init__)
    def __init__(self, data=[]) -> None:
        self.data = data

    @functools.wraps(list.__le__)
    def __le__(self, other):
        return self.data.__le__(type(self)(other).data)

    @functools.wraps(list.__lt__)
    def __lt__(self, other, /):
        if self.__eq__(other):
            return False
        return self.__le__(other)

    @functools.wraps(list.__ne__)
    def __ne__(self, other, /):
        return not self.__eq__(other)

    def __radd__(self, other, /):
        other = type(self)(other)
        return other.__radd__(self)

    @functools.wraps(list.__repr__)
    def __repr__(self) -> str:
        return "%s(%s)" % (type(self).__name__, self)

    @functools.wraps(list.__reversed__)
    def __reversed__(self):
        ans = type(self)(self.data)
        ans.reverse()
        return ans

    @functools.wraps(list.__rmul__)
    def __rmul__(self, other, /):
        return self.__mul__(other)

    @functools.wraps(list.copy)
    def copy(self, /):
        return type(self)(self.data)

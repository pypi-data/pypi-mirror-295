import functools

__all__ = ["DataList"]


class DataList:

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

    @functools.wraps(list.__reduce__)
    def __reduce__(self, *args, **kwargs):
        data = self.data
        ans = data.__reduce__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__reduce_ex__)
    def __reduce_ex__(self, *args, **kwargs):
        data = self.data
        ans = data.__reduce_ex__(*args, **kwargs)
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

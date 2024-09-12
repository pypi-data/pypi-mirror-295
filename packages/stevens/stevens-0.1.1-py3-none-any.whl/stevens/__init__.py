import collections
import typing

import scaevola

__all__ = ["ResidueClass"]


class _calc:
    def __init__(self) -> None:
        raise NotImplementedError

    def absolute(a):
        ans = abs(a)
        if ans == a:
            return ans
        if ans == a * -1:
            return ans
        raise ValueError(a)

    def div(a, b):
        return _calc.eucdiv(a, b)[0]

    def eucdiv(a, b):
        return divmod(a, b)

    def gcd(a, b):
        while b:
            a, b = b, _calc.mod(a, b)
        return a

    def integer(a, /):
        ans = int(a)
        if ans == a:
            return ans
        raise ValueError(a)

    def inv(a, b, /):
        s, t = 1, 0
        while b:
            x, a = _calc.eucdiv(a, b)
            s += x * t * -1
            a, b = b, a
            s, t = t, s
        if a == 1:
            return s
        raise ArithmeticError("No modular multiplicative inverse.")

    def mod(a, b):
        if not b:
            return a
        return _calc.eucdiv(a, b)[1]

    def sub(a, b):
        return a + (b * -1)


class _init:
    Data = collections.namedtuple(
        "ResidueClass",
        ("r", "m"),
    )

    def __init__(self) -> None:
        raise NotImplementedError

    def get_parse(obj, args, kwargs):
        if "other" in kwargs:
            return _init.parse_other
        if "iterable" in kwargs:
            return _init.parse_iterable
        if len(kwargs) != 0:
            return _init.parse_items
        if len(args) != 1:
            return _init.parse_items
        if type(args[0]) is type(obj):
            return _init.parse_other
        return _init.parse_items

    def norm(r, m):
        m = _calc.absolute(m)
        r = _calc.mod(r, m)
        ans = _init.Data(r, m)
        return ans

    def parse_iterable(*, iterable):
        iterable = list(iterable)
        r = iterable.pop(0)
        m = 0
        z = r * -1
        for y in iterable:
            m = _calc._gcd(y + z, m)
        return _init.norm(r, m)

    def parse_other(other):
        return other._data

    def parse_items(r=0, m=0):
        return _init.norm(r, m)

    def run(obj, args, kwargs):
        parse = _init.get_parse(obj, args, kwargs)
        data = parse(*args, **kwargs)
        object.__setattr__(obj, "_data", data)


class ResidueClass(
    scaevola.Scaevola,
):
    def __add__(self, other) -> typing.Self:
        other = type(self)(other)
        r = self.r + other.r
        m = _calc.gcd(self.m, other.m)
        ans = type(self)(r, m)
        return ans

    def __and__(self, other) -> typing.Self:
        other = type(self)(other)
        g = _calc.gcd(self.m, other.m)
        d = _calc.sub(other.r, self.r)
        x, y = _calc.eucdiv(d, g)
        if y:
            raise ValueError(other)
        a = _calc.div(self.m, g)
        b = _calc.div(other.m, g)
        i = _calc.inv(a, b)
        r = self(x * i)
        m = a * other.m
        ans = type(self)(r, m)
        return ans

    def __bool__(self) -> bool:
        return bool(self.r)

    def __call__(self, other):
        return self.r + (self.m * other)

    def __contains__(self, other) -> bool:
        return self.r == _calc.mod(other, self.m)

    def __delattr__(self, name):
        return delattr(self._data, name)

    def __eq__(self, other) -> bool:
        if type(other) is not type(self):
            return False
        return self._data == other._data

    def __getattr__(self, name):
        return getattr(self._data, name)

    def __hash__(self) -> int:
        return self._data.__hash__()

    @typing.overload
    def __init__(self, r=0, m=0) -> None: ...
    @typing.overload
    def __init__(self, other: typing.Self) -> None: ...
    @typing.overload
    def __init__(self, *, iterable: typing.Iterable) -> None: ...
    def __init__(self, *args, **kwargs) -> None:
        _init.run(self, args, kwargs)

    def __le__(self, other) -> bool:
        other = type(self)(other)
        if self.r not in other:
            return False
        if _calc.mod(self.m, other.m):
            return False
        return True

    def __lt__(self, other) -> bool:
        if self == other:
            return False
        return self <= other

    def __mul__(self, other) -> typing.Self:
        other = type(self)(other)
        r = self.r * other.r
        m = _calc.gcd(self.m, other.m)
        ans = type(self)(r, m)
        return ans

    def __neg__(self):
        return self * -1

    def __or__(self, other) -> typing.Self:
        other = type(self)(other)
        m = _calc.sub(other.r, self.r)
        m = _calc.gcd(m, self.m)
        m = _calc.gcd(m, other.m)
        ans = type(self)(self.r, m)
        return ans

    def __pow__(self, other) -> typing.Self:
        other = _calc.integer(other)
        if other < 0:
            x = _calc.inv(*self._data)
        else:
            x = self.r
        other = abs(other)
        r = 1
        while other:
            other -= 1
            r *= x
        ans = type(self)(r, self.m)
        return ans

    def __repr__(self) -> str:
        return str(self._data)

    def __sub__(self, other):
        return self + (other * -1)

    def __setattr__(self, name, value) -> None:
        return setattr(self._data, name, value)

    def __truediv__(self, other):
        return self * (other**-1)

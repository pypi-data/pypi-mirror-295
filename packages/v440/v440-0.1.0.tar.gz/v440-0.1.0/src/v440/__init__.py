from __future__ import annotations

import enum
import functools
import re
import string
import typing

import packaging.version
import scaevola

__all__ = ["VersionError", "Version"]


class _parse:
    _PREDICT = dict(
        alpha="a",
        a="a",
        beta="b",
        b="b",
        preview="rc",
        pre="rc",
        c="rc",
        rc="rc",
    )

    def __init__(self) -> None:
        raise NotImplementedError

    def to_ans(x, /, *, save=True):
        if save:
            return x
        if x is None:
            return
        raise ValueError

    def to_input(x, /):
        if x is None:
            return None
        if not hasattr(x, "__iter__"):
            return _parse.to_str(x)
        if issubclass(type(x), str):
            return _parse.to_str(x)
        return _parse.to_list(x)

    def to_item(x, /):
        if type(x) is int:
            return numeral(x)
        x = _parse.to_str(x)
        if x == "":
            return x
        if x.strip(string.digits) == "":
            return int(x)
        return x

    def to_list(x, /):
        return [_parse.to_item(i) for i in x]

    def to_pre_letter(x, /):
        return _parse._PREDICT[x]

    def to_str(x, /):
        x = str(x).lower().strip()
        return x


class _Pattern(enum.StrEnum):
    EPOCH = r"(?:(?P<epoch>[0-9]+)!)?"
    RELEASE = r"(?P<release>[0-9]+(?:\.[0-9]+)*)"
    PRE = r"""
        (?P<pre>                                          
            [-_\.]?
            (?P<pre_l>alpha|a|beta|b|preview|pre|c|rc)
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?"""
    POST = r"""
        (?P<post>                                         
            (?:-(?:[0-9]+))
            |
            (?: [-_\.]? (?:post|rev|r) [-_\.]? (?:[0-9]+)? )
        )?"""
    DEV = r"""(?P<dev> [-_\.]? dev [-_\.]? (?:[0-9]+)? )?"""
    LOCAL = r"""(?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?"""
    PUBLIC = f"v? {EPOCH} {RELEASE} {PRE} {POST} {DEV}"

    @functools.cached_property
    def regex(self):
        p = self.value
        p = r"^" + p + r"$"
        ans = re.compile(p, re.VERBOSE)
        return ans


#####################

_SEGCHARS = string.ascii_lowercase + string.digits


def _doublecall(old, /):
    @functools.wraps(old)
    def new(*args, **kwargs):
        return old(*args, **kwargs)

    return new


def _index(value, /):
    ans = value.__index__()
    if type(ans) is not int:
        raise TypeError("__index__ returned non-int (type %s)" % type(ans).__name__)
    return ans


def _list(value, prefix):
    if value is None:
        return
    if not issubclass(type(value), str) and hasattr(value, "__iter__"):
        return list(value)
    value = str(value).lower()
    value = value.replace("-", ".")
    value = value.replace("_", ".")
    value = _lsub(value, prefix, error=False)
    if value == "":
        return []
    value = value.split(".")
    return value


def _lsub(value: str, *prefices):
    for p in prefices:
        if value.startswith(p):
            return p, value[len(p) :]
    raise ValueError


def _setterdeco(old, /):
    @functools.wraps(old)
    def new(self, value, /):
        try:
            old(self, value)
        except VersionError:
            raise
        except:
            e = "%r is an invalid value for %r"
            e %= (value, old.__name__)
            raise VersionError(e)

    return new


def _tofunc(old):
    @functools.wraps(old)
    def new(*args, **kwargs):
        return old(*args, **kwargs)

    return new


def literal(value, /):
    e = "%r is not a valid literal segment"
    e = VersionError(e % value)
    try:
        x = segment(value)
    except:
        raise e
    if type(x) is str:
        return x
    raise e


def numeral(value, /):
    e = "%r is not a valid numeral segment"
    e = VersionError(e % value)
    try:
        x = segment(value)
    except:
        raise e
    if type(x) is int:
        return x
    if x == "":
        return 0
    raise e


def segment(value, /):
    e = "%r is not a valid segment"
    e = VersionError(e % value)
    try:
        x = str(value).lower().strip()
    except:
        raise e
    if x.strip(_SEGCHARS):
        raise e
    try:
        return int(x)
    except:
        return x


class Local(list):
    def __add__(self, other):
        return type(self)(list(self) + list(other))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return list(self) == list(other)

    def __ge__(self, other):
        other = type(self)(other)
        return self._cmpkey() >= other._cmpkey()

    def __gt__(self, other):
        other = type(self)(other)
        return self._cmpkey() > other._cmpkey()

    def __init__(self, values=[], /):
        super().__init__()
        self.extend(values)

    def __le__(self, other):
        other = type(self)(other)
        return self._cmpkey() <= other._cmpkey()

    def __lt__(self, other):
        other = type(self)(other)
        return self._cmpkey() < other._cmpkey()

    def __mul__(self, other: typing.SupportsIndex) -> list:
        return type(self)(super().__mul__(other))

    def __radd__(self, other):
        return type(self)(list(other) + list(self))

    def __repr__(self) -> str:
        return "%s(%r)" % (type(self).__name__, str(self))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __setitem__(self, key, value):
        if type(key) is slice:
            value = [segment(x) for x in value]
        else:
            value = segment(value)
        super()[key] = value

    def __str__(self) -> str:
        return ".".join(str(x) for x in self)

    def _cmpkey(self):
        return [self._sortkey(x) for x in self]

    @staticmethod
    def _list(value):
        return [segment(x) for x in _list(value, "+")]

    @staticmethod
    def _sortkey(value):
        return type(value) is int, value

    def append(self, value: typing.Any, /) -> None:
        super().append(segment(value))

    def extend(self, values: typing.Any, /) -> None:
        super().extend(self._list(values))

    def insert(self, index, element, /):
        element = segment(element)
        super().insert(index, element)

    def sort(self, *, key=None, reverse=False):
        if key is None:
            key = self._sortkey
        super().sort(key=key, reverse=reverse)


class Pre:
    _PHASEDICT = dict(
        alpha="a",
        a="a",
        beta="b",
        b="b",
        preview="rc",
        pre="rc",
        c="rc",
        rc="rc",
    )

    def __bool__(self):
        return bool(self.phase)

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        return self.data == other.data

    def __hash__(self) -> int:
        return hash((self.phase, self.subphase))

    @typing.overload
    def __init__(self, data=None) -> None: ...
    @typing.overload
    def __init__(self, phase, subphase=0): ...
    @_doublecall
    def __init__(self, *args, **kwargs):
        if "data" in kwargs.keys():
            return self._init_data
        if kwargs:
            return self._init_items
        if len(args) > 1:
            return self._init_items
        return self._init_data

    def __repr__(self) -> str:
        return "%s(%r)" % (type(self).__name__, str(self))

    def __str__(self) -> str:
        if self:
            return self.phase + str(self.subphase)
        else:
            return ""

    def _init_data(self, data=None):
        self.data = data

    def _init_items(self, phase, subphase=0):
        self.phase = phase
        self.subphase = subphase

    def copy(self):
        return type(self)(self)

    @property
    def data(self):
        if not self.phase:
            return None
        return self.phase, self.subphase

    @data.setter
    @_setterdeco
    def data(self, value, /):
        value = _list(value, ".")
        if len(value) == 0:
            del self.data
            return
        if len(value) > 1:
            self.phase, self.subphase = value
            return
        value = value[0]
        if type(value) is int:
            raise TypeError
        for long, short in type(self)._PHASEDICT.items():
            p, value = _lsub(value, long, "")
            if p == "":
                continue
            self.phase = short
            self.subphase = value[len(long) :]
            return
        raise ValueError

    @data.deleter
    def data(self):
        del self.phase

    @property
    def phase(self):
        return self._phase

    @phase.setter
    @_setterdeco
    def phase(self, value):
        if not value:
            del self.phase
            return
        value = literal(value)
        value = type(self)._PHASEDICT[value]
        self._phase = value

    @phase.deleter
    def phase(self):
        self._phase = None
        self._subphase = 0

    @property
    def subphase(self):
        return self._subphase

    @subphase.setter
    @_setterdeco
    def subphase(self, value):
        value = numeral(value)
        if value == 0:
            del self.subphase
            return
        if self.phase:
            self._subphase = value
            return
        raise VersionError("no subphase allowed without a phase")

    @subphase.deleter
    def subphase(self):
        self._subphase = 0


class Release(list):
    def __add__(self, other):
        return type(self)(list(self) + list(other))

    def __delitem__(self, key: typing.SupportsIndex | slice) -> None:
        super().__delitem__(key)
        self._rstrip()

    def __getitem__(self, key):
        if type(key) is slice:
            return self.__getitem_slice(key)
        else:
            return self.__getitem_index(key)

    def __getitem_index(self, key):
        if len(self) <= key:
            return 0
        else:
            return super()[key]

    def __getitem_slice(self, key):
        ans = self._range(key)
        ans = [self.__getitem_index(i) for i in ans]
        return ans

    def __init__(self, data=[], /):
        super().__init__()
        self.extend(data)

    def __mul__(self, other):
        return type(self)(super().__mul__(other))

    def __radd__(self, other):
        return type(self)(list(other) + list(self))

    def __repr__(self) -> str:
        return "%s(%r)" % (type(self).__name__, str(self))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __setitem__(self, key, value):
        if type(key) is slice:
            self.__setitem_slice(key, value)
        else:
            self.__setitem_index(key, value)

    def __setitem_index(self, key, value):
        key = _index(key)
        value = numeral(value)
        if len(self) > key:
            super()[key] = value
            self._rstrip()
            return
        if not value:
            return
        super().extend([0] * (key - len(self)))
        super().append(value)

    def __setitem_slice(self, key, value):
        key = list(self._range(key))
        value = self._list(value)
        if len(key) != len(value):
            e = "attempt to assign sequence of size %s to extended slice of size %s"
            e %= (len(value), len(key))
            raise ValueError(e)
        for k, v in zip(key, value):
            self.__setitem_index(k, v)

    def __str__(self) -> str:
        return ".".join(str(x) for x in self)

    @staticmethod
    def _list(value):
        return [numeral(x) for x in value]

    def _range(self, key):
        start = key.start
        stop = key.stop
        step = key.step
        if step is None:
            step = 1
        else:
            step = _index(step)
            if step == 0:
                raise ValueError
        fwd = step > 0
        if start is None:
            start = 0 if fwd else len(self) - 1
        else:
            start = _index(start)
        if stop is None:
            stop = len(self) if fwd else -1
        else:
            stop = _index(stop)
        if start < 0:
            start += len(self)
        if start < 0:
            start = 0 if fwd else -1
        if stop < 0:
            stop += len(self)
        if stop < 0:
            stop = 0 if fwd else -1
        return range(start, stop, step)

    def _rstrip(self):
        if not self:
            return
        while x := self.pop():
            pass
        super().append(x)

    def _start(self, index, fwd):
        if index is None:
            return 0
        if index < 0:
            index += len(self)

    def append(self, element):
        element = numeral(element)
        if element:
            super().append(element)

    def bump(self, index=-1, amount=1):
        self[index] += amount
        index = int(index)
        index %= len(self)
        index += 1
        try:
            while True:
                self.pop(index)
        except IndexError:
            pass

    def copy(self):
        return list.__new__(type(self), self)

    def extend(self, data, /):
        super().extend(self._list(data))
        self._rstrip()

    def format(self, cutoff=None):
        ans = self[:cutoff]
        ans = [str(x) for x in ans]
        ans = ".".join(ans)
        return ans

    def insert(self, index, element):
        element = numeral(element)
        super().insert(index, element)
        self._rstrip()

    @property
    def major(self) -> int:
        return self[0]

    @major.setter
    @_setterdeco
    def major(self, value: typing.Any):
        self[0] = value

    @major.deleter
    def major(self):
        del self[0]

    @property
    def micro(self) -> int:
        return self[2]

    @micro.setter
    @_setterdeco
    def micro(self, value: typing.Any):
        self[2] = value

    @micro.deleter
    def micro(self):
        del self[2]

    @property
    def minor(self) -> int:
        return self[1]

    @minor.setter
    @_setterdeco
    def minor(self, value: typing.Any):
        self[1] = value

    @minor.deleter
    def minor(self):
        del self[1]

    def pop(self, index: typing.SupportsIndex = -1) -> Any:
        ans = super().pop(index)
        self._rstrip()
        return ans

    def remove(self, value: Any) -> None:
        ans = super().remove(value)
        self._rstrip()
        return ans

    def reverse(self):
        super().reverse()
        self._rstrip()

    def sort(self):
        super().sort()
        self._rstrip()


class Version(scaevola.Scaevola):
    def __eq__(self, other) -> bool:
        other = type(self)(other)
        return self._cmpkey() == other._cmpkey()

    def __hash__(self) -> int:
        return hash(self._cmpkey())

    def __init__(self, data="0", /, **kwargs) -> None:
        self.data = data
        self.update(**kwargs)

    def __le__(self, other) -> bool:
        other = type(self)(other)
        return self._cmpkey() <= other._cmpkey()

    def __lt__(self, other) -> bool:
        other = type(self)(other)
        return self._cmpkey() < other._cmpkey()

    def __repr__(self) -> str:
        return "%s(%r)" % (type(self).__name__, str(self))

    def __str__(self) -> str:
        return self.data

    def _cmpkey(self) -> tuple:
        if self.pre:
            pre = self.pre.data
        elif self.post is None and self.dev is not None:
            pre = "", -1
        else:
            pre = "z", float("inf")
        post = -1 if self.post is None else self.post
        dev = float("inf") if self.dev is None else self.dev
        return self.epoch, self.release, pre, post, dev, self.local

    @property
    def base(self) -> str:
        if self.epoch:
            return "%s!%s" % (self.epoch, self.release)
        else:
            return str(self.release)

    @base.setter
    @_setterdeco
    def base(self, v):
        v = str(v)
        if "!" in v:
            self.epoch, self.release = v.split("!")
        else:
            self.epoch, self.release = 0, v

    @base.deleter
    def base(self):
        del self.epoch
        del self.release

    def clear(self):
        del self.public
        del self.local

    def copy(self):
        return type(self)(self)

    @property
    def data(self):
        if not self.local:
            return self.public
        return "%s+%s" % (self.public, self.local)

    @data.setter
    @_setterdeco
    def data(self, x):
        x = str(x)
        if "+" in x:
            self.public, self.local = x.split("+")
        else:
            self.public, self.local = x, None

    @data.deleter
    def data(self):
        del self.public
        del self.local

    @property
    def dev(self):
        return self._dev

    @dev.setter
    @_setterdeco
    def dev(self, v):
        v = _list(v, ".")
        if len(v) > 2:
            raise ValueError
        if len(v) == 0:
            del self.dev
            return
        if len(v) == 1:
            v = v[0]
            v = _lsub(v, "dev", "")
        if v[0] != "dev":
            raise ValueError
        v = numeral(v[1])
        self._dev = v

    @dev.deleter
    def dev(self):
        self._dev = None

    @property
    def epoch(self):
        return self._epoch

    @epoch.setter
    @_setterdeco
    def epoch(self, v):
        v = str(v)
        v = _lsub(v, "v", "")[1]
        if v.endswith("!"):
            v = v[:-1]
        v = numeral(v)
        return v

    @epoch.deleter
    def epoch(self):
        self._epoch = 0

    def is_prerelease(self) -> bool:
        return self.dev is not None or self.pre is not None

    def is_postrelease(self) -> bool:
        return self.post is not None

    def is_devrelease(self) -> bool:
        return self.dev is not None

    @property
    def local(self) -> str:
        return self._local

    @local.setter
    @_setterdeco
    def local(self, v):
        self._local = Local(v)

    @local.deleter
    def local(self):
        self._local = Local()

    def packaging(self):
        return packaging.version.Version(self.data)

    @property
    def post(self):
        return self._post

    @post.setter
    @_setterdeco
    def post(self, v):
        v = _list(v, ".")
        if len(v) > 2:
            raise ValueError
        if len(v) == 0:
            del self.post
            return
        prefices = "post", "rev", "r", ""
        if len(v) == 1:
            v = _lsub(v[0], *prefices)
        elif v[0] not in prefices:
            raise ValueError
        v = numeral(v[1])
        self._post = v

    @post.deleter
    def post(self):
        self._post = None

    @property
    def pre(self):
        return self._pre

    @pre.setter
    @_setterdeco
    def pre(self, data, /):
        self._pre = Pre(data)

    @pre.deleter
    def pre(self):
        self._pre = None

    @property
    def public(self) -> str:
        ans = self.base
        ans += str(self.pre)
        if self.post is not None:
            ans += ".post%s" % self.post
        if self.dev is not None:
            ans += ".dev%s" % self.dev
        return ans

    @public.setter
    @_setterdeco
    def public(self, v):
        v = str(v).lower().strip()
        d = _Pattern.PUBLIC.regex.search(v).groupdict()
        names = "epoch release pre post dev".split()
        for n in names:
            setattr(self, n, d[n])

    @public.deleter
    def public(self):
        self.public = "0"

    @property
    def release(self) -> Release:
        return self._release

    @release.setter
    @_setterdeco
    def release(self, v):
        self._release = Release(v)

    @release.deleter
    def release(self):
        self._release = Release()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            attr = getattr(type(self), k)
            if isinstance(attr, property):
                setattr(self, k, v)
                continue
            e = "%r is not a property"
            e %= k
            e = AttributeError(e)
            raise e


class VersionError(ValueError): ...

# !/usr/bin/python
# -*- coding: utf-8 -*-

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# The MIT License (MIT)
#
# Copyright (c) 2017 Jorge A. Gomes (jorgegomes83 at hotmail dot com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import struct
import math
from collections import namedtuple as nt
from typing import Union, Sequence, Iterable, Container
from easygl.arrays.datatypes import DType


__all__ = [
    'Vec2',
    'Vec3',
    'Vec4',
    'FrozenVec4',
]

V2 = "xy yx u v uv vu".split()
V3 = ("xy xz yx yz zx zy xyz xzy yxz yzx zxy zyx "
      "r g b "
      "rg rb gr gb br bg rgb rbg grb gbr brg bgr").split()
V4 = ("xy xz xw yx yz yw zx zy zw wx wy wz "
      "xyz xyw xzy xzw xwy xwz yxz yxw yzx yzw ywx ywz zxy zxw zyx zyw zwx zwy wxy wxz wyx wyz wzx wzy "
      "xyzw xywz xzyw xzwy xwyz xwzy yxzw yxwz yzxw yzwx ywxz ywzx "
      "zxyw zxwy zyxw zywx zwxy zwyx wxyz wxzy wyxz wyzx wzxy wzyx "
      "r g b a "
      "rg rb ra gr gb ga br bg ba ar ag ab "
      "rgb rga rbg rba rag rab grb gra gbr gba gar gab brg bra bgr bga bar bag arg arb agr agb abr abg "
      "rgba rgab rbga rbag ragb rabg grba grab gbra gbar garb gabr "
      "brga brag bgra bgar barg bagr argb arbg agrb agbr abrg abgr").split()


def getargs(l, *args):
    # type: (list, ...) -> None
    for i in args:   # type: Union[int, float, Iterable]
        if isinstance(i, (int, float)):
            l.append(i)
        else:
            getargs(l, *i)


class Arithvector(Iterable, Sequence):

    def __len__(self):
        return 0

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(v + other for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(self[i] + other[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(other + v for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(other[i] + self[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, (int, float)):
            for i in range(len(self)):
                self[i] += other
            return self
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                for i in range(n):
                    self[i] += other[i]
                return self
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(v - other for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(self[i] - other[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(other - v for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(other[i] - self[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __isub__(self, other):
        if isinstance(other, (int, float)):
            for i in range(len(self)):
                self[i] -= other
            return self
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                for i in range(n):
                    self[i] -= other[i]
                return self
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(v * other for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(self[i] * other[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(other * v for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(other[i] * self[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __imul__(self, other):
        if isinstance(other, (int, float)):
            for i in range(len(self)):
                self[i] *= other
            return self
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                for i in range(n):
                    self[i] *= other[i]
                return self
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(v / other for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(self[i] / other[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(other / v for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(other[i] / self[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __itruediv__(self, other):
        if isinstance(other, (int, float)):
            for i in range(len(self)):
                self[i] /= other
            return self
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                for i in range(n):
                    self[i] /= other[i]
                return self
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __mod__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(v % other for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(self[i] % other[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __rmod__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(*(other % v for v in self))
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                return self.__class__(*(other[i] % self[i] for i in range(n)))
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __imod__(self, other):
        if isinstance(other, (int, float)):
            for i in range(len(self)):
                self[i] %= other
            return self
        else:
            try:
                n = len(self)
                if n != len(other):
                    return NotImplemented
                for i in range(n):
                    self[i] %= other[i]
                return self
            except (TypeError, ValueError, IndexError, KeyError):
                return NotImplemented

    def __eq__(self, other):
        try:
            n = len(self)
            return all(self[i] == other[i] for i in range(n)) and len(other) == n
        except (TypeError, KeyError, IndexError):
            return False


class Vec2(Arithvector):

    __slots__ = 'x', 'y'

    @classmethod
    def zero(cls):
        # type: () -> Vec2
        return cls(0., 0.)

    @classmethod
    def one(cls):
        # type: () -> Vec2
        return cls(1., 1.)

    @classmethod
    def horz(cls):
        # type: () -> Vec2
        return cls(1., 0.)

    @classmethod
    def vert(cls):
        # type: () -> Vec2
        return cls(0., 1.)

    # region - - -- ----==<[ COMMON ]>==---- -- - -

    def __init__(self, *args):
        values = []
        getargs(values, *args)
        if len(values) != len(self):
            raise ValueError("Too much or to few values: expected 2, got {}.".format(len(values)))
        self.x = float(values[0])
        self.y = float(values[1])

    def __len__(self):
        return 2

    def __getitem__(self, key):
        # type: (int) -> float
        return (self.x, self.y).__getitem__(key)

    def __setitem__(self, key, value):
        # type: (int, float) -> None
        super(Vec2, self).__setattr__({0: 'x', 1: 'y'}[key], value)

    def __iter__(self):
        return (self.x, self.y).__iter__()

    def __getattr__(self, name):
        if name[0] in 'xy':
            swz = 'xy'
        elif name[0] in 'uv':
            swz = 'uv'
        else:
            raise AttributeError("Vec2 has no '{}' attribute.".format(name))

        if len(name) == 1:
            attr = {'x': 'x', 'y': 'y', 'u': 'x', 'v': 'y'}
            return getattr(self, attr[name])
        elif len(name) not in (2, 3, 4):
            raise AttributeError("Attribute swizzling is too long ({}).".format(len(name)))
        else:
            v = {2: Vec2, 3: Vec3, 4: Vec4}[len(name)]

        i = [self.x, self.y]
        try:
            return v(*(i[swz.index(ch)] for ch in name))
        except ValueError:
            raise AttributeError("Vec2 '{}' swizzled with invalid attribute(s).".format(name))

    def __setattr__(self, name, value):
        # type: (str, Union[tuple, list, Container, Iterable, Sequence, Vec2]) -> None
        if name in V2:
            attr = {'x': 'x', 'y': 'y', 'u': 'x', 'v': 'y'}
            n = len(name)
            if n > 1:
                try:
                    if n != len(value):
                        raise ValueError("Attribute needs {} float values, not {}.".format(n, len(value)))
                except TypeError:
                    raise ValueError("Attribute needs {} float values, not 1.".format(n))
                for i, ch in enumerate(name):
                    super(Vec2, self).__setattr__(attr[ch], float(value[i]))
            else:
                super(Vec2, self).__setattr__(attr[name], float(value))
        elif name in self.__slots__:
            super(Vec2, self).__setattr__(name, float(value))
        else:
            raise AttributeError("Vec2 object has no '{}' attribute.".format(name))

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Vec2{}".format(str(self))

    # endregion

    # region - - -- ----==<[ OTHER ]>==---- -- - -

    def hypot(self):
        # type: () -> None
        return self.x ** 2 + self.y ** 2

    def dot(self, other):
        # type: (Vec2) -> float
        return ((self.x * other.x) +
                (self.y * other.y))

    def cross(self, other):
        # type: (Vec2) -> float
        return self.x * other.y - self.y * other.x

    def length(self):
        # type: () -> float
        return math.sqrt(self.hypot())

    def normalize(self):
        # type: () -> Vec2
        magnitude = self.length()
        if magnitude != 0.:
            self.x /= magnitude
            self.y /= magnitude
        else:
            self.x = self.y = 0.
        return self

    def normalized(self):
        # type: () -> Vec2
        magnitude = self.length()
        if magnitude != 0.:
            return Vec2(
                self.x / magnitude,
                self.y / magnitude,
            )
        return Vec2(0., 0.)

    # endregion

    @staticmethod
    def pack_values(*values, as_double=False):
        if as_double:
            fmt = DType.double_v2.format
        else:
            fmt = DType.float_v2.format
        return struct.pack(fmt, *values)

    def pack(self, as_double=False):
        if as_double:
            fmt = DType.double_v2.format
        else:
            fmt = DType.float_v2.format
        return struct.pack(fmt, self.x, self.y)

    def unpack(self, buffer, as_double=False):
        if as_double:
            fmt = DType.double_v2.format
        else:
            fmt = DType.float_v2.format
        self.x, self.y = struct.unpack(fmt, buffer)
        return self

    def pack_into(self, buffer, offset, as_double=False):
        if as_double:
            fmt = DType.double_v2.format
        else:
            fmt = DType.float_v2.format
        struct.pack_into(fmt, buffer, offset, self.x, self.y)

    def unpack_from(self, buffer, offset, as_double=False):
        if as_double:
            fmt = DType.double_v2.format
        else:
            fmt = DType.float_v2.format
        self.x, self.y = struct.unpack_from(fmt, buffer, offset)
        return self


class Vec3(Arithvector):

    __slots__ = 'x', 'y', 'z'

    # region - - -- ----==<[ COMMON ]>==---- -- - -

    def __init__(self, *args):
        values = []
        getargs(values, *args)
        if len(values) != len(self):
            raise ValueError("Too much or to few values: expected 3, got {}.".format(len(values)))
        self.x = float(values[0])
        self.y = float(values[1])
        self.z = float(values[2])

    def __len__(self):
        return 3

    def __getitem__(self, key):
        # type: (int) -> float
        return (self.x, self.y, self.z).__getitem__(key)

    def __setitem__(self, key, value):
        # type: (int, float) -> None
        super(Vec3, self).__setattr__({0: 'x', 1: 'y', 2: 'z'}[key], value)

    def __iter__(self):
        return (self.x, self.y, self.z).__iter__()

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "Vec3{}".format(str(self))

    def __getattr__(self, name):
        if name[0] in 'xyz':
            swz = 'xyz'
        elif name[0] in 'rgb':
            swz = 'rgb'
        else:
            raise AttributeError("Vec3 has no '{}' attribute.".format(name))

        if len(name) == 1:
            attr = {'x': 'x', 'y': 'y', 'z': 'z', 'r': 'x', 'g': 'y', 'b': 'z'}
            return getattr(self, attr[name])
        elif len(name) not in (2, 3, 4):
            raise AttributeError("Attribute swizzling is too long ({}).".format(len(name)))
        else:
            v = {2: Vec2, 3: Vec3, 4: Vec4}[len(name)]

        i = [self.x, self.y, self.z]
        try:
            return v(*(i[swz.index(ch)] for ch in name))
        except ValueError:
            raise AttributeError("Vec3 '{}' swizzled with invalid attribute(s).".format(name))

    def __setattr__(self, name, value):
        # type: (str, Union[tuple, list, Container, Iterable, Sequence, Vec3]) -> None
        if name in V3:
            attr = {'x': 'x', 'y': 'y', 'z': 'z', 'r': 'x', 'g': 'y', 'b': 'z'}
            n = len(name)
            if n > 1:
                try:
                    if n != len(value):
                        raise ValueError("Attribute needs {} float values, not {}.".format(n, len(value)))
                except TypeError:
                    raise ValueError("Attribute needs {} float values, not 1.".format(n))
                for i, ch in enumerate(name):
                    super(Vec3, self).__setattr__(attr[ch], float(value[i]))
            else:
                super(Vec3, self).__setattr__(attr[name], float(value))
        elif name in self.__slots__:
            super(Vec3, self).__setattr__(name, float(value))
        else:
            raise AttributeError("Vec3 object has no '{}' attribute.".format(name))

    # endregion

    # region - - -- ----==<[ OTHER ]>==---- -- - -

    def hypot(self):
        # type: () -> None
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def dot(self, other):
        # type: (Union[Vec3, Vec4]) -> float
        return ((self.x * other.x) +
                (self.y * other.y) +
                (self.z * other.z))

    def cross(self, other):
        # type: (Union[Vec3, Vec4]) -> Vec3
        return Vec3(self.x * other.z - self.z * other.y,
                    self.y * other.x - self.x * other.z,
                    self.z * other.y - self.y * other.x)

    def length(self):
        # type: () -> float
        return math.sqrt(self.hypot())

    def normalize(self):
        # type: () -> Vec3
        magnitude = self.length()
        if magnitude != 0.:
            self.x /= magnitude
            self.y /= magnitude
            self.z /= magnitude
        else:
            self.x = self.y = self.z = 0.
        return self

    def normalized(self):
        # type: () -> Vec3
        magnitude = self.length()
        if magnitude != 0.:
            return Vec3(
                self.x / magnitude,
                self.y / magnitude,
                self.z / magnitude
            )
        return Vec3(0., 0., 0.)

    # endregion

    @staticmethod
    def pack_values(*values, as_double=False):
        if as_double:
            fmt = DType.double_v3.format
        else:
            fmt = DType.float_v3.format
        return struct.pack(fmt, *values)

    def pack(self, as_double=False):
        if as_double:
            fmt = DType.double_v3.format
        else:
            fmt = DType.float_v3.format
        return struct.pack(fmt, self.x, self.y, self.z)

    def unpack(self, buffer, as_double=False):
        if as_double:
            fmt = DType.double_v3.format
        else:
            fmt = DType.float_v3.format
        self.x, self.y, self.z = struct.unpack(fmt, buffer)
        return self

    def pack_into(self, buffer, offset, as_double=False):
        if as_double:
            fmt = DType.double_v3.format
        else:
            fmt = DType.float_v3.format
        struct.pack_into(fmt, buffer, offset, self.x, self.y, self.z)

    def unpack_from(self, buffer, offset, as_double=False):
        if as_double:
            fmt = DType.double_v3.format
        else:
            fmt = DType.float_v3.format
        self.x, self.y, self.z = struct.unpack_from(fmt, buffer, offset)


class Vec4(Arithvector):

    __slots__ = 'x', 'y', 'z', 'w'

    # region - - -- ----==<[ COMMON ]>==---- -- - -

    def __init__(self, *args):
        values = []
        getargs(values, *args)
        if len(values) != len(self):
            raise ValueError("Too much or to few values: expected 4, got {}.".format(len(values)))
        self.x = float(values[0])
        self.y = float(values[1])
        self.z = float(values[2])
        self.w = float(values[3])

    def __len__(self):
        return 4

    def __getitem__(self, key):
        # type: (int) -> float
        return (self.x, self.y, self.z, self.w).__getitem__(key)

    def __setitem__(self, key, value):
        # type: (int, float) -> None
        super(Vec4, self).__setattr__({0: 'x', 1: 'y', 2: 'z', 3: 'w'}[key], float(value))

    def __iter__(self):
        return (self.x, self.y, self.z, self.w).__iter__()

    def __str__(self):
        return "({}, {}, {}, {})".format(self.x, self.y, self.z, self.w)

    def __repr__(self):
        return "Vec4{}".format(str(self))

    def __getattr__(self, name):
        if name[0] in 'xyzw':
            swz = 'xyzw'
        elif name[0] in 'rgba':
            swz = 'rgba'
        else:
            raise AttributeError("Vec4 has no '{}' attribute.".format(name))

        if len(name) == 1:
            attr = {'x': 'x', 'y': 'y', 'z': 'z', 'w': 'w', 'r': 'x', 'g': 'y', 'b': 'z', 'a': 'w'}
            return getattr(self, attr[name])
        elif len(name) not in (2, 3, 4):
            raise AttributeError("Attribute swizzling is too long ({}).".format(len(name)))
        else:
            v = {2: Vec2, 3: Vec3, 4: Vec4}[len(name)]

        i = [self.x, self.y, self.z, self.w]
        try:
            return v(*(i[swz.index(ch)] for ch in name))
        except ValueError:
            raise AttributeError("Vec4 '{}' swizzled with invalid attribute(s).".format(name))

    def __setattr__(self, name, value):
        # type: (str, Union[tuple, list, Container, Iterable, Sequence, Vec4]) -> None
        if name in V4:
            attr = {'x': 'x', 'y': 'y', 'z': 'z', 'w': 'w', 'r': 'x', 'g': 'y', 'b': 'z', 'a': 'w'}
            n = len(name)
            if n > 1:
                try:
                    if n != len(value):
                        raise ValueError("Attribute needs {} float values, not {}.".format(n, len(value)))

                except TypeError:
                    raise ValueError("Attribute needs {} float values, not 1.".format(n))
                for i, ch in enumerate(name):
                    super(Vec4, self).__setattr__(attr[ch], float(value[i]))

            else:
                super(Vec4, self).__setattr__(attr[name], float(value))

        elif name in self.__slots__:
            super(Vec4, self).__setattr__(name, float(value))
        else:
            raise AttributeError("Vec4 object has no '{}' attribute.".format(name))

    # endregion

    # region - - -- ----==<[ OTHER ]>==---- -- - -

    def hypot(self):
        # type: () -> None
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def dot(self, other):
        # type: (Union[Vec3, Vec4]) -> float
        return ((self.x * other.x) +
                (self.y * other.y) +
                (self.z * other.z))

    def cross(self, other):
        # type: (Union[Vec3, Vec4]) -> Vec4
        return  Vec4(self.x * other.z - self.z * other.y,
                     self.y * other.x - self.x * other.z,
                     self.z * other.y - self.y * other.x,
                     1.)

    def length(self):
        # type: () -> float
        return math.sqrt(self.hypot())

    def normalize(self):
        # type: () -> Vec4
        magnitude = self.length()
        if magnitude != 0.:
            self.x /= magnitude
            self.y /= magnitude
            self.z /= magnitude
        else:
            self.x = self.y = self.z = 0.
            self.w = 1.
        return self

    def normalized(self):
        # type: () -> Vec4
        magnitude = self.length()
        if magnitude != 0.:
            return Vec4(
                self.x / magnitude,
                self.y / magnitude,
                self.z / magnitude,
                1.
            )
        return Vec4(0., 0., 0., 1.)

    # endregion

    @staticmethod
    def pack_values(*values, as_double=False):
        if as_double:
            fmt = DType.double_v4.format
        else:
            fmt = DType.float_v4.format
        return struct.pack(fmt, *values)

    def pack(self, as_double=False):
        if as_double:
            fmt = DType.double_v4.format
        else:
            fmt = DType.float_v4.format
        return struct.pack(fmt, self.x, self.y, self.z, self.w)

    def unpack(self, buffer, as_double=False):
        if as_double:
            fmt = DType.double_v4.format
        else:
            fmt = DType.float_v4.format
        self.x, self.y, self.z, self.w = struct.unpack(fmt, buffer)
        return self

    def pack_into(self, buffer, offset, as_double=False):
        if as_double:
            fmt = DType.double_v4.format
        else:
            fmt = DType.float_v4.format
        struct.pack_into(fmt, buffer, offset, self.x, self.y, self.z, self.w)

    def unpack_from(self, buffer, offset, as_double=False):
        if as_double:
            fmt = DType.double_v4.format
        else:
            fmt = DType.float_v4.format
        self.x, self.y, self.z, self.w = struct.unpack_from(fmt, buffer, offset)


class FrozenVec4(nt('FrozenVec4', 'x y z w'), Arithvector):

    def __getattr__(self, name):
        if name[0] in 'xyzw':
            swz = 'xyzw'
        elif name[0] in 'rgba':
            swz = 'rgba'
        else:
            raise AttributeError("Vec4 has no '{}' attribute.".format(name))

        if len(name) == 1:
            attr = {'x': 'x', 'y': 'y', 'z': 'z', 'w': 'w', 'r': 'x', 'g': 'y', 'b': 'z', 'a': 'w'}
            return getattr(self, attr[name])
        elif len(name) not in (2, 3, 4):
            raise AttributeError("Attribute swizzling is too long ({}).".format(len(name)))
        else:
            v = {2: Vec2, 3: Vec3, 4: FrozenVec4}[len(name)]

        # i = [self.x, self.y, self.z, self.w]
        try:
            return v(*(self[swz.index(ch)] for ch in name))
        except ValueError:
            raise AttributeError("Vec4 '{}' swizzled with invalid attribute(s).".format(name))

    # del __iadd__, __isub__, __imul__, __itruediv__, __ifloordiv__, __imod__

    # region - - -- ----==<[ OTHER ]>==---- -- - -

    def hypot(self):
        # type: () -> None
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def dot(self, other):
        # type: (Union[Vec3, Vec4, FrozenVec4]) -> float
        return ((self.x * other.x) +
                (self.y * other.y) +
                (self.z * other.z))

    def cross(self, other):
        # type: (Union[Vec3, Vec4]) -> Vec4
        return  FrozenVec4(self.x * other.z - self.z * other.y,
                     self.y * other.x - self.x * other.z,
                     self.z * other.y - self.y * other.x,
                     1.)

    def length(self):
        # type: () -> float
        return math.sqrt(self.hypot())

    def normalized(self):
        # type: () -> FrozenVec4
        magnitude = self.length()
        if magnitude != 0.:
            return FrozenVec4(
                self.x / magnitude,
                self.y / magnitude,
                self.z / magnitude,
                1.
            )
        return FrozenVec4(0., 0., 0., 1.)

    # endregion

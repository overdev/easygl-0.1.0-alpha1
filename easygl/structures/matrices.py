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
from typing import Union, Iterable
from .vectors import *
from collections import namedtuple as nt

__all__ = [
    'Mat2',
    'Mat3',
    'Mat4',
    'FrozenMat4',
]


EPSILON = .00001


def getargs(l, *args):
    # type: (list, ...) -> None
    for i in args:   # type: Union[int, float, Iterable]
        if isinstance(i, (int, float)):
            l.append(i)
        else:
            getargs(l, *i)


class Matrix(object):

    def __init__(self, *args):
        v = []
        getargs(v, *args)
        if len(v) != len(self):
            raise ValueError("Too many or too few values: expected {}, got {}.".format(len(self), len(v)))
        self._m = list(map(float, v))

    def __len__(self):
        # type: () -> int
        return 0

    def __iter__(self):
        return self._m.__iter__()

    def __getitem__(self, key):
        if isinstance(key, slice):
            print(key)
        return self._m.__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            print(key)
        self._m.__setitem__(key, value)

    def __bytes__(self):
        # type: () -> bytes
        return struct.pack(">16f", *self)

    def _swap(self, a, b):
        # type: (int, int) -> None
        tmp = self[b]
        self[b] = self[a]
        self[a] = tmp


class Mat2(Matrix):

    __slots__ = ('_m',)

    @classmethod
    def identity(cls):
        # type: () -> Mat2
        return cls(
            1., 0.,
            0., 1.
        )

    def __len__(self):
        # type: () -> int
        return 4

    def __mul__(self, other):
        # type: (Union[list, tuple, Vec2, Mat2]) -> Union[Vec2, Mat2]
        m = self
        n = other
        if len(other) == len(self):
            return Mat2(
                m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1],
                m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3]
            )
        elif len(other) == 2:
            return Vec2(
                m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1]
            )
        else:
            return NotImplemented

    def __rmul__(self, other):
        # type: (Union[list, tuple, Vec2, Mat2]) -> Mat2
        if len(other) == len(self):
            return self.__mul__(other)
        return NotImplemented

    def __imul__(self, other):
        # type: (Union[list, tuple, Vec3, Mat3]) -> Mat2
        m = self
        n = other
        if len(self) == len(other):
            o = [
                m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1],
                m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3]
            ]
            self._m = o
            return self
        return NotImplemented

    def determinant(self):
        # type: () -> float
        return self[0] * self[3] - self[1] * self[2]

    def invert(self):
        # type: () -> Mat2
        determinant = self.determinant()
        if determinant < EPSILON:
            return self.__class__.identity()

        tmp = self[0]
        inv_det = 1. / determinant

        self[0] = inv_det * self[3]
        self[1] = -inv_det * self[1]
        self[2] = -inv_det * self[2]
        self[3] = inv_det * tmp

        return self

    def transpose(self):
        # type: () -> Mat2
        self._swap(1, 2)
        return self


class Mat3(Matrix):

    __slots__ = ('_m',)

    @classmethod
    def identity(cls):
        # type: () -> Mat3
        return cls(
            1., 0., 0.,
            0., 1., 0.,
            0., 0., 1.
        )

    @classmethod
    def transform(cls, translation, rotation, scaling):
        # type: (Vec3, float, Vec3) -> Mat3
        r = math.radians(rotation)

        tx, ty, tz = translation
        sx, sy, sz = scaling

        co = math.cos(r)
        si = math.sin(r)
        ss = -si
        return cls(
            sx * co, sx * si, 0.0,
            sy * ss, sy * co, 0.0,
            tx, ty, 1.0
        )

    def __len__(self):
        # type: () -> int
        return 9

    def __mul__(self, other):
        # type: (Union[list, tuple, Mat3]) -> Union[Mat3, Vec3]
        m = self
        n = other
        if len(self) == len(other):
            return Mat3(
                m[0] * n[0] + m[3] * n[1] + m[6] * n[2],
                m[1] * n[0] + m[4] * n[1] + m[7] * n[2],
                m[2] * n[0] + m[5] * n[1] + m[8] * n[2],
                m[0] * n[3] + m[3] * n[4] + m[6] * n[5],
                m[1] * n[3] + m[4] * n[4] + m[7] * n[5],
                m[2] * n[3] + m[5] * n[4] + m[8] * n[5],
                m[0] * n[6] + m[3] * n[7] + m[6] * n[8],
                m[1] * n[6] + m[4] * n[7] + m[7] * n[8],
                m[2] * n[6] + m[5] * n[7] + m[8] * n[8]
            )
        elif len(other) == 3:
            return Vec3(
                m[0] * n[0] + m[3] * n[1] + m[6] * n[2],
                m[1] * n[0] + m[4] * n[1] + m[7] * n[2],
                m[2] * n[0] + m[5] * n[1] + m[8] * n[2]
            )
        else:
            return NotImplemented

    def __rmul__(self, other):
        # type: (Union[list, tuple, Mat3]) -> Mat3
        if len(other) == len(self):
            return self.__mul__(other)
        return NotImplemented

    def __imul__(self, other):
        # type: (Union[list, tuple, Mat3]) -> Mat3
        m = self
        n = other
        if len(self) == len(other):
            o = [
                m[0] * n[0] + m[3] * n[1] + m[6] * n[2],
                m[1] * n[0] + m[4] * n[1] + m[7] * n[2],
                m[2] * n[0] + m[5] * n[1] + m[8] * n[2],
                m[0] * n[3] + m[3] * n[4] + m[6] * n[5],
                m[1] * n[3] + m[4] * n[4] + m[7] * n[5],
                m[2] * n[3] + m[5] * n[4] + m[8] * n[5],
                m[0] * n[6] + m[3] * n[7] + m[6] * n[8],
                m[1] * n[6] + m[4] * n[7] + m[7] * n[8],
                m[2] * n[6] + m[5] * n[7] + m[8] * n[8]
            ]
            self._m = o
            return self
        return NotImplemented

    def determinant(self):
        # type: () -> float
        m = self._m
        return (
            m[0] * (m[4] * m[8] - m[5] * [7]) -
            m[1] * (m[3] * m[8] - m[5] * [6]) +
            m[2] * (m[3] * m[7] - m[4] * [6])
        )

    def invert(self):
        # type: () -> Mat3
        tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        m = self._m

        tmp[0] = m[4] * m[8] - m[5] * m[7]
        tmp[1] = m[2] * m[7] - m[1] * m[8]
        tmp[2] = m[1] * m[5] - m[2] * m[4]
        tmp[3] = m[5] * m[6] - m[3] * m[8]
        tmp[4] = m[0] * m[8] - m[2] * m[6]
        tmp[5] = m[2] * m[3] - m[0] * m[5]
        tmp[6] = m[3] * m[7] - m[4] * m[6]
        tmp[7] = m[1] * m[6] - m[0] * m[7]
        tmp[8] = m[0] * m[4] - m[1] * m[3]

        det = m[0] * tmp[0] + m[1] * tmp[3] + m[2] * tmp[6]
        if abs(det) < EPSILON:
            return self.__class__.identity()

        inv_det = 1. / det
        m[0] = inv_det * tmp[0]
        m[1] = inv_det * tmp[1]
        m[2] = inv_det * tmp[2]
        m[3] = inv_det * tmp[3]
        m[4] = inv_det * tmp[4]
        m[5] = inv_det * tmp[5]
        m[6] = inv_det * tmp[6]
        m[7] = inv_det * tmp[7]
        m[8] = inv_det * tmp[8]

        return self

    def transpose(self):
        # type: () -> Mat3
        self._swap(1, 3)
        self._swap(2, 6)
        self._swap(5, 7)

        return self


class Mat4(Matrix):

    __slots__ = ('_m',)

    @classmethod
    def identity(cls):
        # type: () -> Mat4
        return cls(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def transform(cls, translation, rotation, scaling):
        # type: (Vec4, float, Vec4) -> Mat4
        r = math.radians(rotation)

        tx, ty, tz, tw = translation
        sx, sy, sz, sw = scaling

        co = math.cos(r)
        si = math.sin(r)
        ss = -si
        return cls(
            sx * co, sx * si, 0.0, 0.0,
            sy * ss, sy * co, 0.0, 0.0,
            0.0, 0.0, sz, 0.0,
            tx, ty, tz, 1.0,
        )

    @classmethod
    def ortho(cls, left, right, bottom, top, near, far):
        # type: (int, int, int, int, int, int) -> Mat4
        rml = float(right - left)
        rpl = float(right + left)
        tmb = float(top - bottom)
        tpb = float(top + bottom)
        fmn = float(far - near)
        fpn = float(far + near)

        return cls(
            2.0 / rml,     0.0,          0.0,         0.0,
            0.0,           2.0 / tmb,    0.0,         0.0,
            0.0,           0.0,         -2.0 / fmn,   0.0,
            -(rpl / rml), -(tpb / tmb), -(fpn / fmn), 1.0
        )

    def __len__(self):
        # type: () -> int
        return 16

    def __getitem__(self, key):
        # type: (Union[int, slice]) -> Union[float, Vec4]
        if isinstance(key, slice):
            if isinstance(key.start, int):
                if 0 <= key.start < 4:
                    i = key.start * 4
                    return Vec4(self._m[i: i + 4])
            elif isinstance(key.stop, int):
                if 0 <= key.stop < 4:
                    i = key.stop
                    m = self._m
                    return Vec4(m[i], m[i + 4], m[i + 8], m[i + 12])

        elif isinstance(key, int):
            return super(Mat4, self).__getitem__(key)

        raise IndexError("Invalid key value.")

    def __mul__(self, other):
        # type: (Union[tuple, list, Mat4, Vec4]) -> Union[Vec4, Mat4]
        m = self
        n = other
        if len(other) == len(self):
            return Mat4(
                m[0] * n[0]  + m[4] * n[1]  + m[8]  * n[2]  + m[12] * n[3],
                m[1] * n[0]  + m[5] * n[1]  + m[9]  * n[2]  + m[13] * n[3],
                m[2] * n[0]  + m[6] * n[1]  + m[10] * n[2]  + m[14] * n[3],
                m[3] * n[0]  + m[7] * n[1]  + m[11] * n[2]  + m[15] * n[3],
                m[0] * n[4]  + m[4] * n[5]  + m[8]  * n[6]  + m[12] * n[7],
                m[1] * n[4]  + m[5] * n[5]  + m[9]  * n[6]  + m[13] * n[7],
                m[2] * n[4]  + m[6] * n[5]  + m[10] * n[6]  + m[14] * n[7],
                m[3] * n[4]  + m[7] * n[5]  + m[11] * n[6]  + m[15] * n[7],
                m[0] * n[8]  + m[4] * n[9]  + m[8]  * n[10] + m[12] * n[11],
                m[1] * n[8]  + m[5] * n[9]  + m[9]  * n[10] + m[13] * n[11],
                m[2] * n[8]  + m[6] * n[9]  + m[10] * n[10] + m[14] * n[11],
                m[3] * n[8]  + m[7] * n[9]  + m[11] * n[10] + m[15] * n[11],
                m[0] * n[12] + m[4] * n[13] + m[8]  * n[14] + m[12] * n[15],
                m[1] * n[12] + m[5] * n[13] + m[9]  * n[14] + m[13] * n[15],
                m[2] * n[12] + m[6] * n[13] + m[10] * n[14] + m[14] * n[15],
                m[3] * n[12] + m[7] * n[13] + m[11] * n[14] + m[15] * n[15],
            )
        elif len(other) == 4:
            return Vec4(
                m[0] * n[0] + m[4] * n[1] + m[8]  * n[2] + m[12] * n[3],
                m[1] * n[0] + m[5] * n[1] + m[9]  * n[2] + m[13] * n[3],
                m[2] * n[0] + m[6] * n[1] + m[10] * n[2] + m[14] * n[3],
                m[3] * n[0] + m[7] * n[1] + m[11] * n[2] + m[15] * n[3]
            )
        return NotImplemented

    def __rmul__(self, other):
        # type: (Union[tuple, list, Mat4]) -> Mat4
        if len(other) == len(self):
            return self.__mul__(other)
        return NotImplemented

    def __imul__(self, other):
        # type: (Union[tuple, list, Mat4]) -> Mat4
        m = self
        n = other
        o = [
            m[0] * n[0] + m[4] * n[1] + m[8] * n[2] + m[12] * n[3],
            m[1] * n[0] + m[5] * n[1] + m[9] * n[2] + m[13] * n[3],
            m[2] * n[0] + m[6] * n[1] + m[10] * n[2] + m[14] * n[3],
            m[3] * n[0] + m[7] * n[1] + m[11] * n[2] + m[15] * n[3],
            m[0] * n[4] + m[4] * n[5] + m[8] * n[6] + m[12] * n[7],
            m[1] * n[4] + m[5] * n[5] + m[9] * n[6] + m[13] * n[7],
            m[2] * n[4] + m[6] * n[5] + m[10] * n[6] + m[14] * n[7],
            m[3] * n[4] + m[7] * n[5] + m[11] * n[6] + m[15] * n[7],
            m[0] * n[8] + m[4] * n[9] + m[8] * n[10] + m[12] * n[11],
            m[1] * n[8] + m[5] * n[9] + m[9] * n[10] + m[13] * n[11],
            m[2] * n[8] + m[6] * n[9] + m[10] * n[10] + m[14] * n[11],
            m[3] * n[8] + m[7] * n[9] + m[11] * n[10] + m[15] * n[11],
            m[0] * n[12] + m[4] * n[13] + m[8] * n[14] + m[12] * n[15],
            m[1] * n[12] + m[5] * n[13] + m[9] * n[14] + m[13] * n[15],
            m[2] * n[12] + m[6] * n[13] + m[10] * n[14] + m[14] * n[15],
            m[3] * n[12] + m[7] * n[13] + m[11] * n[14] + m[15] * n[15],
        ]
        self._m = o
        return self

    def determinat(self):
        return NotImplemented

    def invert(self):
        return NotImplemented

    def transpose(self):
        # type: () -> Mat4
        self._swap(1, 4)
        self._swap(2, 8)
        self._swap(3, 12)
        self._swap(6, 9)
        self._swap(7, 13)
        self._swap(11, 14)

        return self


class FrozenMat4(nt("FrozenMat4", "ax ay az aw bx by bz bw cx cy cz cw dx dy dz dw")):

    @classmethod
    def identity(cls):
        # type: () -> FrozenMat4
        return cls(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        )

    @classmethod
    def transform(cls, translation, rotation, scaling):
        # type: (Vec4, float, Vec4) -> FrozenMat4
        r = math.radians(rotation)

        tx, ty, tz, tw = translation
        sx, sy, sz, sw = scaling

        co = math.cos(r)
        si = math.sin(r)
        ss = -si
        return cls(
            sx * co, sx * si, 0.0, 0.0,
            sy * ss, sy * co, 0.0, 0.0,
            0.0, 0.0, sz, 0.0,
            tx, ty, tz, 1.0,
        )

    @classmethod
    def ortho(cls, left, right, bottom, top, near, far):
        # type: (int, int, int, int, int, int) -> FrozenMat4
        rml = float(right - left)
        rpl = float(right + left)
        tmb = float(top - bottom)
        tpb = float(top + bottom)
        fmn = float(far - near)
        fpn = float(far + near)

        return cls(
            2.0 / rml, 0.0, 0.0, 0.0,
            0.0, 2.0 / tmb, 0.0, 0.0,
            0.0, 0.0, -2.0 / fmn, 0.0,
            -(rpl / rml), -(tpb / tmb), -(fpn / fmn), 1.0
        )

    def __mul__(self, other):
        # type: (Union[tuple, list, Vec4, Mat4, FrozenMat4]) -> Union[Vec4, FrozenMat4]
        m = self
        n = other
        if len(other) == len(self):
            return FrozenMat4(
                m[0] * n[0] + m[4] * n[1] + m[8] * n[2] + m[12] * n[3],
                m[1] * n[0] + m[5] * n[1] + m[9] * n[2] + m[13] * n[3],
                m[2] * n[0] + m[6] * n[1] + m[10] * n[2] + m[14] * n[3],
                m[3] * n[0] + m[7] * n[1] + m[11] * n[2] + m[15] * n[3],
                m[0] * n[4] + m[4] * n[5] + m[8] * n[6] + m[12] * n[7],
                m[1] * n[4] + m[5] * n[5] + m[9] * n[6] + m[13] * n[7],
                m[2] * n[4] + m[6] * n[5] + m[10] * n[6] + m[14] * n[7],
                m[3] * n[4] + m[7] * n[5] + m[11] * n[6] + m[15] * n[7],
                m[0] * n[8] + m[4] * n[9] + m[8] * n[10] + m[12] * n[11],
                m[1] * n[8] + m[5] * n[9] + m[9] * n[10] + m[13] * n[11],
                m[2] * n[8] + m[6] * n[9] + m[10] * n[10] + m[14] * n[11],
                m[3] * n[8] + m[7] * n[9] + m[11] * n[10] + m[15] * n[11],
                m[0] * n[12] + m[4] * n[13] + m[8] * n[14] + m[12] * n[15],
                m[1] * n[12] + m[5] * n[13] + m[9] * n[14] + m[13] * n[15],
                m[2] * n[12] + m[6] * n[13] + m[10] * n[14] + m[14] * n[15],
                m[3] * n[12] + m[7] * n[13] + m[11] * n[14] + m[15] * n[15]
            )
        elif len(other) == 4:
            return Vec4(
                m[0] * n[0] + m[4] * n[1] + m[8] * n[2] + m[12] * n[3],
                m[1] * n[0] + m[5] * n[1] + m[9] * n[2] + m[13] * n[3],
                m[2] * n[0] + m[6] * n[1] + m[10] * n[2] + m[14] * n[3],
                m[3] * n[0] + m[7] * n[1] + m[11] * n[2] + m[15] * n[3]
            )
        return NotImplemented

    def __rmul__(self, other):
        # type: (Union[tuple, list, Mat4, FrozenMat4]) -> FrozenMat4
        if len(other) == len(self):
            return self.__mul__(other)
        return NotImplemented

    @property
    def a(self):
        # type: () -> Vec4
        return Vec4(self.ax, self.ay, self.az, self.aw)

    @property
    def b(self):
        # type: () -> Vec4
        return Vec4(self.bx, self.by, self.bz, self.bw)

    @property
    def c(self):
        # type: () -> Vec4
        return Vec4(self.cx, self.cy, self.cz, self.cw)

    @property
    def d(self):
        # type: () -> Vec4
        return Vec4(self.dx, self.dy, self.dz, self.dw)

    @property
    def x(self):
        # type: () -> Vec4
        return Vec4(self.ax, self.bx, self.cx, self.dx)

    @property
    def y(self):
        # type: () -> Vec4
        return Vec4(self.ay, self.by, self.cy, self.dy)

    @property
    def z(self):
        # type: () -> Vec4
        return Vec4(self.az, self.bz, self.cz, self.dz)

    @property
    def w(self):
        # type: () -> Vec4
        return Vec4(self.aw, self.bw, self.cw, self.dw)

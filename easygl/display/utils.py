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

from easygl.structures.vectors import Vec3, Vec4
import pygame as pg
import random
from collections import namedtuple as nt

__all__ = [
    'ndc',
    'rgb',
    'rgba',
    'any_rgb',
    'any_rgba',
    'Color',
]


def rgb(red, green, blue):
    # type: (int, int, int) -> Vec3
    return Vec3(
        max(0., min(red / 255., 1.)),
        max(0., min(green / 255., 1.)),
        max(0., min(blue / 255., 1.))
    )


def rgba(red, green, blue, alpha):
    # type: (int, int, int, int) -> Vec4
    return Vec4(
        max(0., min(red / 255., 1.)),
        max(0., min(green / 255., 1.)),
        max(0., min(blue / 255., 1.)),
        max(0., min(alpha / 255., 1.))
    )


def any_rgba():
    # type: () -> Vec4
    return Vec4(
        random.random(),
        random.random(),
        random.random(),
        random.random()
    )


def any_rgb():
    # type: () -> Vec4
    return Vec3(
        random.random(),
        random.random(),
        random.random()
    )


def ndc(x, y):
    # type: (float, float) -> tuple
    w, h = pg.display.get_surface().get_size()
    ox = w * 0.5
    oy = h * 0.5
    return ox + (ox * x), oy + (oy * y)


Color = nt("Color", "none black red yellow green cyan blue magenta white")(
    Vec4(0, 0, 0, 0),
    Vec4(0, 0, 0, 1),
    Vec4(1, 0, 0, 1),
    Vec4(1, 1, 0, 1),
    Vec4(0, 1, 0, 1),
    Vec4(0, 1, 1, 1),
    Vec4(0, 0, 1, 1),
    Vec4(1, 0, 1, 1),
    Vec4(1, 1, 1, 1),
)

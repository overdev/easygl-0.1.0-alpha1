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

from collections import namedtuple as nt

__all__ = [
    'CloseWindow',
    'Focus',
    'JoyAxis',
    'JoyBall',
    'JoyButtonDown',
    'JoyButtonUp',
    'JoyHat',
    'KeyDown',
    'KeyUp',
    'LeftButtonDown',
    'LeftButtonUp',
    'MiddleButtonDown',
    'MiddleButtonUp',
    'MouseMotion',
    'MouseWheelDown',
    'MouseWheelUp',
    'RightButtonDown',
    'RightButtonUp',
    'VideoExpose',
    'VideoResize',
]


class MouseMotion(nt("MouseMotion", "position motion lbutton mbutton rbutton")):

    @property
    def type(self):
        return self.__class__


class LeftButtonDown(nt("LeftButtonDown", "position x y")):

    @property
    def type(self):
        return self.__class__


class MiddleButtonDown(nt("MiddleButtonDown", "position x y")):

    @property
    def type(self):
        return self.__class__


class RightButtonDown(nt("RightButtonDown", "position x y")):

    @property
    def type(self):
        return self.__class__


class MouseWheelDown(nt("MouseWheelDown", "position x y")):

    @property
    def type(self):
        return self.__class__


class LeftButtonUp(nt("LeftButtonUp", "position x y")):

    @property
    def type(self):
        return self.__class__


class MiddleButtonUp(nt("MiddleButtonUp", "position x y")):

    @property
    def type(self):
        return self.__class__


class RightButtonUp(nt("RightButtonUp", "position x y")):

    @property
    def type(self):
        return self.__class__


class MouseWheelUp(nt("MouseWheelUp", "position x y")):

    @property
    def type(self):
        return self.__class__


class KeyDown(nt("KeyDown", "key char mod ctrl shift alt")):

    @property
    def type(self):
        return self.__class__


class KeyUp(nt("KeyUp", "key mod ctrl shift alt")):

    @property
    def type(self):
        return self.__class__


class VideoResize(nt("VideoResize", "width height size")):

    @property
    def type(self):
        return self.__class__


class VideoExpose(nt("VideoExpose", "milliseconds datetime")):

    @property
    def type(self):
        return self.__class__


class Focus(nt("MouseFocus", "mouse input milliseconds")):

    @property
    def type(self):
        return self.__class__


class CloseWindow(nt("CloseWindow", "milliseconds datetime")):

    @property
    def type(self):
        return self.__class__


class JoyAxis(nt("JoyAxis", "id axis value")):

    @property
    def type(self):
        return self.__class__


class JoyBall(nt("JoyBall", "id ball motion")):

    @property
    def type(self):
        return self.__class__


class JoyHat(nt("JoyHat", "id hat value")):

    @property
    def type(self):
        return self.__class__


class JoyButtonDown (nt("JoyButtonDown", "id button")):

    @property
    def type(self):
        return self.__class__


class JoyButtonUp (nt("JoyButtonUp", "id button")):

    @property
    def type(self):
        return self.__class__

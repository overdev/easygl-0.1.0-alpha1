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


MouseMotion = nt("MouseMotion", "position motion lbutton mbutton rbutton")

LeftButtonDown = nt("LeftButtonDown", "position x y")
MiddleButtonDown = nt("MiddleButtonDown", "position x y")
RightButtonDown = nt("RightButtonDown", "position x y")
MouseWheelDown = nt("MouseWheelDown", "position x y")
LeftButtonUp = nt("LeftButtonUp", "position x y")
MiddleButtonUp = nt("MiddleButtonUp", "position x y")
RightButtonUp = nt("RightButtonUp", "position x y")
MouseWheelUp = nt("MouseWheelUp", "position x y")

KeyDown = nt("KeyDown", "key char mod ctrl shift alt")
KeyUp = nt("KeyUp", "key mod ctrl shift alt")

VideoResize = nt("VideoResize", "width height size")
VideoExpose = nt("VideoExpose", "milliseconds datetime")
Focus = nt("MouseFocus", "mouse input milliseconds")


CloseWindow = nt("CloseWindow", "milliseconds datetime")

JoyAxis = nt("JoyAxis", "id axis value")
JoyBall = nt("JoyBall", "id ball motion")
JoyHat = nt("JoyHat", "id hat value")
JoyButtonDown = nt("JoyButtonDown", "id button")
JoyButtonUp = nt("JoyButtonUp", "id button")

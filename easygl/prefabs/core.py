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


from easygl.arrays import VertexArrayData, VertexArray, DType, vertex, vertex_copy, attribute
from easygl.shaders import ShaderProgramData, ShaderProgram


INITIALIZED_DATA = 0

SPRITE_STATIC = 1
SPRITE_ANIMATED = 1 << 1
SPRITE = SPRITE_STATIC | SPRITE_ANIMATED
CIRCLE_LINE = 1 << 2
CIRCLE_FILL = 1 << 3
CIRCLE = CIRCLE_LINE | CIRCLE_FILL
ELLIPSE_LINE = 1 << 4
ELLIPSE_FILL = 1 << 5
ELLIPSE = ELLIPSE_LINE | ELLIPSE_FILL
OVAL_LINE = 1 << 6
OVAL_FILL = 1 << 7
OVAL = OVAL_LINE | OVAL_FILL
ARC_CIRCLE = 1 << 8
ARC_ELLIPSE = 1 << 9
ARC = ARC_CIRCLE | ARC_ELLIPSE
PIE_CIRCLE_LINE = 1 << 10
PIE_CIRCLE_FILL = 1 << 11
PIE_CIRCLE = PIE_CIRCLE_LINE | PIE_CIRCLE_FILL
PIE_ELLIPSE_LINE = 1 << 12
PIE_ELLIPSE_FILL = 1 << 13
PIE_ELLIPSE = PIE_ELLIPSE_LINE | PIE_ELLIPSE_FILL
RECT_LINE = 1 << 14
RECT_FILL = 1 << 15
RECT = RECT_LINE | RECT_FILL
AABB_LINE = 1 << 16
AABB_FILL = 1 << 17
AABB = AABB_LINE | AABB_FILL
LINE_SINGLE = 1 << 18
LINE_MULTI = 1 << 19
LINE = LINE_SINGLE | LINE_MULTI

ALL = (1 << 20) - 1

MAX_PRECISION = 721

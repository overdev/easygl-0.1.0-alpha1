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
from ctypes import sizeof
import OpenGL.GL as GL

__all__ = [
    'DType',
    'DTypeInfo',
]


class DTypeInfo(nt("DTypeInfo", "name size byte_size gl_size, gl_type uniform format")):

    def load(self, *args):
        self.uniform(*args)


DType = nt(
    "DType",
    "bool byte short int ubyte ushort uint ulong "
    "bool_v2 byte_v2 short_v2 int_v2 ubyte_v2 ushort_v2 uint_v2 ulong_v2 "
    "bool_v3 byte_v3 short_v3 int_v3 ubyte_v3 ushort_v3 uint_v3 ulong_v3 "
    "bool_v4 byte_v4 short_v4 int_v4 ubyte_v4 ushort_v4 uint_v4 ulong_v4 "
    "float double "
    "float_v2 double_v2 "
    "float_v3 double_v3 "
    "float_v4 double_v4 "
    "float_m2 float_m23 float_m24 "
    "float_m3 float_m32 float_m34 "
    "float_m4 float_m42 float_m43 "
    "double_m2 double_m23 double_m24 "
    "double_m3 double_m32 double_m34 "
    "double_m4 double_m42 double_m43 "
)(
    DTypeInfo('bool',   1, sizeof(GL.GLboolean), GL.GL_BOOL,           GL.GLboolean, GL.glUniform1ui, '?'),
    DTypeInfo('byte',   1, sizeof(GL.GLbyte),    GL.GL_BYTE,           GL.GLbyte,    GL.glUniform1i,  'b'),
    DTypeInfo('short',  1, sizeof(GL.GLshort),   GL.GL_SHORT,          GL.GLshort,   GL.glUniform1i,  'h'),
    DTypeInfo('int',    1, sizeof(GL.GLint),     GL.GL_INT,            GL.GLint,     GL.glUniform1i,  'i'),
    DTypeInfo('ubyte',  1, sizeof(GL.GLubyte),   GL.GL_UNSIGNED_BYTE,  GL.GLubyte,   GL.glUniform1ui, 'B'),
    DTypeInfo('ushort', 1, sizeof(GL.GLushort),  GL.GL_UNSIGNED_SHORT, GL.GLushort,  GL.glUniform1ui, 'H'),
    DTypeInfo('uint',   1, sizeof(GL.GLuint),    GL.GL_UNSIGNED_INT,   GL.GLuint,    GL.glUniform1ui, 'I'),
    DTypeInfo('ulong',  1, sizeof(GL.GLulong),   GL.GL_UNSIGNED_INT64, GL.GLulong,   GL.glUniform1ui, 'L'),

    DTypeInfo('bool_v2',   2, 2 * sizeof(GL.GLboolean), GL.GL_BOOL,           GL.GLboolean, GL.glUniform2ui, '??'),
    DTypeInfo('byte_v2',   2, 2 * sizeof(GL.GLbyte),    GL.GL_BYTE,           GL.GLbyte,    GL.glUniform2i,  'bb'),
    DTypeInfo('short_v2',  2, 2 * sizeof(GL.GLshort),   GL.GL_SHORT,          GL.GLshort,   GL.glUniform2i,  'hh'),
    DTypeInfo('int_v2',    2, 2 * sizeof(GL.GLint),     GL.GL_INT,            GL.GLint,     GL.glUniform2i,  'ii'),
    DTypeInfo('ubyte_v2',  2, 2 * sizeof(GL.GLubyte),   GL.GL_UNSIGNED_BYTE,  GL.GLubyte,   GL.glUniform2ui, 'BB'),
    DTypeInfo('ushort_v2', 2, 2 * sizeof(GL.GLushort),  GL.GL_UNSIGNED_SHORT, GL.GLushort,  GL.glUniform2ui, 'HH'),
    DTypeInfo('uint_v2',   2, 2 * sizeof(GL.GLuint),    GL.GL_UNSIGNED_INT,   GL.GLuint,    GL.glUniform2ui, 'II'),
    DTypeInfo('ulong_v2',  2, 2 * sizeof(GL.GLulong),   GL.GL_UNSIGNED_INT64, GL.GLulong,   GL.glUniform2ui, 'LL'),

    DTypeInfo('bool_v3',   3, 3 * sizeof(GL.GLboolean), GL.GL_BOOL,           GL.GLboolean, GL.glUniform3ui, '???'),
    DTypeInfo('byte_v3',   3, 3 * sizeof(GL.GLbyte),    GL.GL_BYTE,           GL.GLbyte,    GL.glUniform3i,  'bbb'),
    DTypeInfo('short_v3',  3, 3 * sizeof(GL.GLshort),   GL.GL_SHORT,          GL.GLshort,   GL.glUniform3i,  'hhh'),
    DTypeInfo('int_v3',    3, 3 * sizeof(GL.GLint),     GL.GL_INT,            GL.GLint,     GL.glUniform3i,  'iii'),
    DTypeInfo('ubyte_v3',  3, 3 * sizeof(GL.GLubyte),   GL.GL_UNSIGNED_BYTE,  GL.GLubyte,   GL.glUniform3ui, 'BBB'),
    DTypeInfo('ushort_v3', 3, 3 * sizeof(GL.GLushort),  GL.GL_UNSIGNED_SHORT, GL.GLushort,  GL.glUniform3ui, 'HHH'),
    DTypeInfo('uint_v3',   3, 3 * sizeof(GL.GLuint),    GL.GL_UNSIGNED_INT,   GL.GLuint,    GL.glUniform3ui, 'III'),
    DTypeInfo('ulong_v3',  3, 3 * sizeof(GL.GLulong),   GL.GL_UNSIGNED_INT64, GL.GLulong,   GL.glUniform3ui, 'LLL'),

    DTypeInfo('bool_v4',   4, 4 * sizeof(GL.GLboolean), GL.GL_BOOL,           GL.GLboolean, GL.glUniform4ui, '????'),
    DTypeInfo('byte_v4',   4, 4 * sizeof(GL.GLbyte),    GL.GL_BYTE,           GL.GLbyte,    GL.glUniform4i,  'bbbb'),
    DTypeInfo('short_v4',  4, 4 * sizeof(GL.GLshort),   GL.GL_SHORT,          GL.GLshort,   GL.glUniform4i,  'hhhh'),
    DTypeInfo('int_v4',    4, 4 * sizeof(GL.GLint),     GL.GL_INT,            GL.GLint,     GL.glUniform4i,  'iiii'),
    DTypeInfo('ubyte_v4',  4, 4 * sizeof(GL.GLubyte),   GL.GL_UNSIGNED_BYTE,  GL.GLubyte,   GL.glUniform4ui, 'BBBB'),
    DTypeInfo('ushort_v4', 4, 4 * sizeof(GL.GLushort),  GL.GL_UNSIGNED_SHORT, GL.GLushort,  GL.glUniform4ui, 'HHHH'),
    DTypeInfo('uint_v4',   4, 4 * sizeof(GL.GLuint),    GL.GL_UNSIGNED_INT,   GL.GLuint,    GL.glUniform4ui, 'IIII'),
    DTypeInfo('ulong_v4',  4, 4 * sizeof(GL.GLulong),   GL.GL_UNSIGNED_INT64, GL.GLulong,   GL.glUniform4ui, 'LLLL'),

    DTypeInfo('float',   1, 1 * sizeof(GL.GLfloat),  GL.GL_FLOAT,  GL.GLfloat,  GL.glUniform1f,    'f'),
    DTypeInfo('double',  1, 1 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniform1d,    'd'),
    DTypeInfo('float_v2',   2, 2 * sizeof(GL.GLfloat),  GL.GL_FLOAT,  GL.GLfloat,  GL.glUniform2f, 'ff'),
    DTypeInfo('double_v2',  2, 2 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniform2d, 'dd'),
    DTypeInfo('float_v3',   3, 3 * sizeof(GL.GLfloat),  GL.GL_FLOAT,  GL.GLfloat,  GL.glUniform3f, 'fff'),
    DTypeInfo('double_v3',  3, 3 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniform3d, 'ddd'),
    DTypeInfo('float_v4',   4, 4 * sizeof(GL.GLfloat),  GL.GL_FLOAT,  GL.GLfloat,  GL.glUniform4f, 'ffff'),
    DTypeInfo('double_v4',  4, 4 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniform4d, 'dddd'),

    DTypeInfo('float_m2',   4,  4 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix2fv,   '4f'),
    DTypeInfo('float_m23',  6,  6 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix2x3fv, '6f'),
    DTypeInfo('float_m24',  8,  8 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix2x4fv, '8f'),
    DTypeInfo('float_m3',   9,  9 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix3fv,   '9f'),
    DTypeInfo('float_m32',  6,  6 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix3x2fv, '6f'),
    DTypeInfo('float_m34', 12, 12 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix3x4fv, '12f'),
    DTypeInfo('float_m4',  16, 16 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix4fv,   '16f'),
    DTypeInfo('float_m42',  8,  8 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix4x2fv, '8f'),
    DTypeInfo('float_m43', 12, 12 * sizeof(GL.GLfloat), GL.GL_FLOAT, GL.GLfloat, GL.glUniformMatrix4x3fv, '12f'),

    DTypeInfo('double_m2',   4,  4 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix2dv,   '4d'),
    DTypeInfo('double_m23',  6,  6 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix2x3dv, '6d'),
    DTypeInfo('double_m24',  8,  8 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix2x4dv, '8d'),
    DTypeInfo('double_m3',   9,  9 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix3dv,   '9d'),
    DTypeInfo('double_m32',  6,  6 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix3x2dv, '6d'),
    DTypeInfo('double_m34', 12, 12 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix3x4dv, '12d'),
    DTypeInfo('double_m4',  16, 16 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix4dv,   '16d'),
    DTypeInfo('double_m42',  8,  8 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix4x2dv, '8d'),
    DTypeInfo('double_m43', 12, 12 * sizeof(GL.GLdouble), GL.GL_DOUBLE, GL.GLdouble, GL.glUniformMatrix4x3dv, '12d'),
)

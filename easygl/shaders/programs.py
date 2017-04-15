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

import OpenGL.GL as GL
from ..arrays import DType, DTypeInfo
from typing import Union

__all__ = [
    'UniformData',
    'ShaderProgram',
]


class UniformData(object):
    __slots__ = 'location', 'dtype'

    def __init__(self, location, dtype):
        # type: (int, DTypeInfo) -> None
        if dtype not in DType:
            raise ValueError("'dtype' argument is not a DType member value.")
        self.location = location
        self.dtype = dtype

    def load(self, *args):
        self.dtype.load(self.location, *args)


class ShaderProgram(object):

    def __init__(self, shader_id, *uniforms):
        self._id = shader_id
        GL.glUseProgram(shader_id)
        self._uniforms = {
            name: GL.glGetUniformLocation(shader_id, name) for name in uniforms
        }
        GL.glUseProgram(0)
        self._tex_unit = 0

    def __getattr__(self, name):
        if name not in ('_id', '_uniforms'):
            if name in getattr(self, '_uniforms'):
                return getattr(self, '_uniforms')[name]
            else:
                raise AttributeError("ShaderProgram object has no '{}' attribute.".format(name))
        else:
            return getattr(self, '__dict__')[name]

    def __setattr__(self, name, value):
        if name not in ('_id', '_uniforms'):
            getattr(self, '_uniforms')[name] = value
        else:
            getattr(self, '__dict__')[name] = value

    @property
    def id(self):
        # type: () -> int
        return self._id

    def set_texture(self, name, texture_id, index=0):
        # type: (str, int, int) -> None
        GL.glActiveTexture(GL.GL_TEXTURE0 + index)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
        GL.glUniform1i(GL.glGetUniformLocation(self._id, name), index)

    def use(self):
        # type: () -> None
        GL.glUseProgram(self._id)

    def unbind(self):
        # type: () -> None
        if self._tex_unit > 0:
            for i in range(1, self._tex_unit):
                GL.glActiveTexture(GL.GL_TEXTURE0 + i)
                GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
            self._tex_unit = 0
        GL.glUseProgram(0)

    def load1f(self, name, v0):
        # type: (str, float) -> None
        GL.glUniform1f(self._uniforms[name], v0)

    def load2f(self, name, v0, v1):
        # type: (str, float, float) -> None
        GL.glUniform2f(self._uniforms[name], v0, v1)

    def load3f(self, name, v0, v1, v2):
        # type: (str, float, float, float) -> None
        GL.glUniform3f(self._uniforms[name], v0, v1, v2)

    def load4f(self, name, v0, v1, v2, v3):
        # type: (str, float, float, float, float) -> None
        GL.glUniform4f(self._uniforms[name], v0, v1, v2, v3)

    def load1d(self, name, v0):
        # type: (str, float) -> None
        GL.glUniform1d(self._uniforms[name], v0)

    def load2d(self, name, v0, v1):
        # type: (str, float, float) -> None
        GL.glUniform2d(self._uniforms[name], v0, v1)

    def load3d(self, name, v0, v1, v2):
        # type: (str, float, float, float) -> None
        GL.glUniform3d(self._uniforms[name], v0, v1, v2)

    def load4d(self, name, v0, v1, v2, v3):
        # type: (str, float, float, float, float) -> None
        GL.glUniform4d(self._uniforms[name], v0, v1, v2, v3)

    def load1ui(self, name, v0):
        # type: (str, int) -> None
        GL.glUniform1ui(self._uniforms[name], v0)

    def load2ui(self, name, v0, v1):
        # type: (str, int, int) -> None
        GL.glUniform2ui(self._uniforms[name], v0, v1)

    def load3ui(self, name, v0, v1, v2):
        # type: (str, int, int, int) -> None
        GL.glUniform3ui(self._uniforms[name], v0, v1, v2)

    def load4ui(self, name, v0, v1, v2, v3):
        # type: (str, int, int, int, int) -> None
        GL.glUniform4ui(self._uniforms[name], v0, v1, v2, v3)

    def load1i(self, name, v0):
        # type: (str, int) -> None
        GL.glUniform1i(self._uniforms[name], v0)

    def load2i(self, name, v0, v1):
        # type: (str, int, int) -> None
        GL.glUniform2i(self._uniforms[name], v0, v1)

    def load3i(self, name, v0, v1, v2):
        # type: (str, int, int, int) -> None
        GL.glUniform3i(self._uniforms[name], v0, v1, v2)

    def load4i(self, name, v0, v1, v2, v3):
        # type: (str, int, int, int, int) -> None
        GL.glUniform4i(self._uniforms[name], v0, v1, v2, v3)

    def load_matrix2f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix2fv(self._uniforms[name], count, transpose, value)

    def load_matrix2x3f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix2x3fv(self._uniforms[name], count, transpose, value)

    def load_matrix2x4f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix2x4fv(self._uniforms[name], count, transpose, value)

    def load_matrix2d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix2dv(self._uniforms[name], count, transpose, value)

    def load_matrix2x3d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix2x3dv(self._uniforms[name], count, transpose, value)

    def load_matrix2x4d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix2x4dv(self._uniforms[name], count, transpose, value)

    def load_matrix3f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix3fv(self._uniforms[name], count, transpose, value)

    def load_matrix3x2f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix3x2fv(self._uniforms[name], count, transpose, value)

    def load_matrix3x4f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix3x4fv(self._uniforms[name], count, transpose, value)

    def load_matrix3d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix3dv(self._uniforms[name], count, transpose, value)

    def load_matrix3x2d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix3x2dv(self._uniforms[name], count, transpose, value)

    def load_matrix3x4d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix3x4dv(self._uniforms[name], count, transpose, value)

    def load_matrix4f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix4fv(self._uniforms[name], count, transpose, value)

    def load_matrix4x2f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix4x2fv(self._uniforms[name], count, transpose, value)

    def load_matrix4x3f(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix4x3fv(self._uniforms[name], count, transpose, value)

    def load_matrix4d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix4dv(self._uniforms[name], count, transpose, value)

    def load_matrix4x2d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix4x2dv(self._uniforms[name], count, transpose, value)

    def load_matrix4x3d(self, name, count, transpose, value):
        # type: (str, int, bool, Union[tuple, list, bytes]) -> None
        GL.glUniformMatrix4x3dv(self._uniforms[name], count, transpose, value)

    def load_sampler2d(self, name, texture_id, texture_unit):
        # type: (str, int, int) -> None
        GL.glActiveTexture(GL.GL_TEXTURE0 + texture_unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
        GL.glUniform1i(self._uniforms[name], texture_unit)
        if self._tex_unit < texture_unit:
            self._tex_unit = texture_unit
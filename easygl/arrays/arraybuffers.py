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
from contextlib import contextmanager

import OpenGL.GL as GL
from .primitives import VertexArrayData
from .datatypes import DTypeInfo
from ..shaders import ShaderProgram
from typing import Union, Optional


__all__ = [
    'VertexArray',
]


class VertexArray(object):

    def __init__(self, arraydescriptor, data, shaderprogram):
        # type: (VertexArrayData, str, ShaderProgram) -> None
        # Create a new VAO (Vertex Array Object) and bind it
        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)

        # Generate buffers to hold our vertices
        vertex_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)

        stride = arraydescriptor.stride
        # for (name, primitive) in args:
        #     stride += primitive.sizeof

        offset = 0
        for name in arraydescriptor.descriptor:
            attrib_location = GL.glGetAttribLocation(shaderprogram.id, name)
            GL.glEnableVertexAttribArray(attrib_location)

            dtype = arraydescriptor.descriptor[name]   # type: DTypeInfo

            # Describe the attribute data layout in the buffer
            GL.glVertexAttribPointer(attrib_location, dtype.size, dtype.gl_size, False, stride, GL.GLvoidp(offset))
            offset += dtype.byte_size

        # Send the data over to the buffer
        num_bytes = len(arraydescriptor[data])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, num_bytes, arraydescriptor[data], GL.GL_DYNAMIC_DRAW)
        # print("num_bytes:", num_bytes)

        # Unbind the VAO first (Important)
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        self.array = arraydescriptor[data]
        self.vao = vertex_array_object
        self.vbo = vertex_buffer
        self._program = shaderprogram
        self._num_vertices = num_bytes // stride

    def update_data(self, offset, data=None):
        # type: (int, Optional[Union[bytes, bytearray]]) -> None
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

        if data is None:
            data = self.array
        GL.glBufferSubData(GL.GL_ARRAY_BUFFER, offset, len(data), data)

        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def draw_arrays(self, mode, count=None):
        # type: () -> None
        if count is None:
            count = self._num_vertices
        GL.glBindVertexArray(self.vao)
        GL.glDrawArrays(mode, 0, count)
        GL.glBindVertexArray(self.vao)

    @contextmanager
    def render(self, mode, count=None, with_shader=None):
        # type: (int, Optional[int], Optional[ShaderProgram]) -> None
        shader = with_shader if isinstance(with_shader, ShaderProgram) else self._program
        shader.use()

        yield self._program

        self.draw_arrays(mode, count)
        shader.unbind()

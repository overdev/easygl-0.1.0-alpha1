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
import os.path as path
from .programs import *


__all__ = [
    'ShaderCompileError',
    'ShaderProgramData',
]


class ShaderCompileError(Exception):
    pass


class ShaderProgramData(object):

    def __init__(self, shader_base_dir):
        # type: (str) -> None
        self._base_dir = shader_base_dir
        self._fragshaders = {}
        self._vertshaders = {}
        self._geomshaders = {}
        self._shaderprograms = {}

    def compile_fragment_shader(self, frag_shader_name, **kwargs):
        # type: (str, ...) -> None
        if 'shader_file' in kwargs:
            fname = path.join(self._base_dir, kwargs.get('shader_file'))
            with open(fname) as fsh:
                fragment_code = "\n".join(fsh.readlines())
        elif 'shader_code' in kwargs:
            fragment_code = kwargs.get('shader_code')
        else:
            raise ValueError("'shader_file' or 'shader_code' keyword argument expected.")

        fragment_id = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(fragment_id, fragment_code)
        GL.glCompileShader(fragment_id)

        if not GL.glGetShaderiv(fragment_id, GL.GL_COMPILE_STATUS):
            raise ShaderCompileError(GL.glGetShaderInfoLog(fragment_id))

        self._fragshaders[frag_shader_name] = fragment_id

    def compile_vertex_shader(self, vert_shader_name, **kwargs):
        # type: (str, ...) -> None
        if 'shader_file' in kwargs:
            fname = path.join(self._base_dir, kwargs.get('shader_file'))
            with open(fname) as fsh:
                vertex_code = "\n".join(fsh.readlines())
        elif 'shader_code' in kwargs:
            vertex_code = kwargs.get('shader_code')
        else:
            raise ValueError("'shader_file' or 'shader_code' keyword argument expected.")

        vertex_id = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(vertex_id, vertex_code)
        GL.glCompileShader(vertex_id)

        if not GL.glGetShaderiv(vertex_id, GL.GL_COMPILE_STATUS):
            raise ShaderCompileError(GL.glGetShaderInfoLog(vertex_id))

        self._vertshaders[vert_shader_name] = vertex_id

    def compile_geometry_shader(self, geom_shader_name, **kwargs):
        # type: (str, ...) -> None
        if 'shader_file' in kwargs:
            fname = path.join(self._base_dir, kwargs.get('shader_file'))
            with open(fname) as fsh:
                geometry_code = "\n".join(fsh.readlines())
        elif 'shader_code' in kwargs:
            geometry_code = kwargs.get('shader_code')
        else:
            raise ValueError("'shader_file' or 'shader_code' keyword argument expected.")

        geometry_id = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(geometry_id, geometry_code)
        GL.glCompileShader(geometry_id)

        if not GL.glGetShaderiv(geometry_id, GL.GL_COMPILE_STATUS):
            raise ShaderCompileError(GL.glGetShaderInfoLog(geometry_id))

        self._geomshaders[geom_shader_name] = geometry_id

    def link(self, program_name, **shaders):
        # type: (...) -> None
        vertex_id = self._vertshaders.get(shaders.get('vertex'))
        fragment_id = self._fragshaders.get(shaders.get('fragment'))
        geometry_id = self._geomshaders.get(shaders.get('geometry'))

        program = GL.glCreateProgram()

        if vertex_id is not None:
            GL.glAttachShader(program, vertex_id)
        if geometry_id is not None:
            GL.glAttachShader(program, geometry_id)
        if fragment_id is not None:
            GL.glAttachShader(program, fragment_id)

        GL.glLinkProgram(program)
        if not GL.glGetProgramiv(program, GL.GL_LINK_STATUS):
            message = GL.glGetProgramInfoLog(program).decode(errors='ignore')
            raise RuntimeError("ShaderProgramErrorMessage: '{}'".format(message))

        if vertex_id is not None:
            GL.glDetachShader(program, vertex_id)
        if geometry_id is not None:
            GL.glDetachShader(program, geometry_id)
        if fragment_id is not None:
            GL.glDetachShader(program, fragment_id)

        self._shaderprograms[program_name] = program

    def build(self, program_name, *uniforms):
        # type: (str, ...) -> ShaderProgram
        if program_name not in self._shaderprograms:
            raise ValueError("'{}' not found.".format(program_name))
        return ShaderProgram(self._shaderprograms[program_name], *uniforms)

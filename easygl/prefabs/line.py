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

import pygame as pg
from OpenGL.GL import GL_LINE_STRIP, GL_LINES, GL_LINE_LOOP
from typing import Optional, Callable
from easygl.arrays import VertexArrayData, DType, attribute, vertex, vertex_copy, VertexArray
from easygl.shaders import ShaderProgramData, ShaderProgram
from easygl.textures import TexDescriptor, TextureData, MipMap, Wrap, Filter
from easygl.structures import FrozenMat4, Vec2, Vec4, FrozenVec4
from easygl.display import BlendMode, GLWindow, Projection


__all__ = [
    'init',
    'line',
    'lines',
    'lineset',
    'vline',
    'hline',
    'bake_lines',
    'line_batch',
    'line_vertex_data',
    'line_shader',
    'line_shader_data',
]


_initialized = False
line_shader = None
line_shader_data = None
line_vertex_data = None

# region - - -- ----==<[ STUBS ]>==---- -- - -

def line_batch(window, view, projection, vert_array, count, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode):
    # type: (GLWindow, Mat4, Mat4, VertexArray, int, Union[Vec4, FrozenVec4], Optional[Union[Vec4, FrozenVec4]], Optional[TexDescription], float, BlendMode) -> None
    pass

def line(window, view, projection, point_a, point_b, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha, update=True):
    # type: (GLWindow, Mat4, Mat4, Vec2, Vec2, Union[Vec4, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode, bool) -> None
    pass


def lines(window, view, projection, points, closed, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha):
    # type: (GLWindow, Mat4, Mat4, Union[list, tuple], bool, Union[Vec4, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode, bool) -> None
    pass

def lineset(window, view, projection, points, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha, update=True, count=-1):
    # type: (GLWindow, Mat4, Mat4, Union[list, tuple], Union[Vec4, FrozenVec4], Union[Vec4, FrozenVec4], float, Optional[TexDescriptor], BlendMode, bool, int) -> None
    pass


def vline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
    # type: (GLWindow, Mat4, Mat4, Vec2, float, Union[Vec2, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode) -> None
    pass


def hline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
    # type: (GLWindow, Mat4, Mat4, Vec2, float, Union[Vec2, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode) -> None
    pass


def bezier(window, view, projection, points, ctrl_points, tex=None, vcoord=0, blend=BlendMode.alpha):
    # type: (GLWindow, Mat4, Mat4, Union[list, tuple], Union[list, tuple], Optional[TexDescriptor], float, BlendMode) -> None
    pass

def bake_lines(points, buffer=None):
    # type: (Union[list, tuple], bytearray) -> None
    pass

# endregion


def init():
    # type: () -> None
    global _initialized, line, lines, vline, hline, bezier, bake_lines, lineset, line_vertex_data, line_shader_data,\
           line_shader, line_batch

    if _initialized:
        return

    # region - - -- ----==<[ VERTEX DATA ]>==---- -- - -

    line_vertex_data = VertexArrayData()

    with line_vertex_data.definition():
        attribute('position', DType.float_v2)

    with line_vertex_data.new_primitive('line', 1024):
        v = 1. / 1024.
        for i in range(1024):
            vertex(position=(v * i, v * i))

    # endregion

    # region - - -- ----==<[ TEXTURES ]>==---- -- - -

    s = pg.Surface((4, 1))
    s.fill((255, 255, 255))
    texdata = TextureData()
    texdata.create_from_surface('line_tex', s, False, False, MipMap.linear_linear, Wrap.repeat,
                                Filter.linear)
    # endregion

    # region - - -- ----==<[ SHADERS ]>==---- -- - -

    line_vshader_code = """
    #version 330 core
    
    in vec2 position;
    
    uniform mat4 view;
    uniform mat4 projection;
    uniform vec4 start_color;
    uniform vec4 end_color;
    uniform float point_count;
    uniform float vcoord;
    
    out vec4 color;
    out vec2 coord;
    
    void main() {
    
        gl_Position = projection * view * vec4(position, 1.f, 1.f);
        color = mix(start_color, end_color, gl_VertexID / (point_count - 1));
        coord = vec2(mod(gl_VertexID, 2.f), vcoord);

    }
    """
    line_fshader_code = """
    #version 330 core
    
    in vec4 color;
    in vec2 coord;
    
    uniform sampler2D tex;
    uniform bool solidcolor;
    
    void main() {
    
        vec4 basecolor = color;
        if (solidcolor)
            basecolor *= texture(tex, coord);
        
        gl_FragColor = basecolor;
    }
    """

    line_shader_data = ShaderProgramData("")
    line_shader_data.compile_vertex_shader('line', shader_code=line_vshader_code)
    line_shader_data.compile_fragment_shader('line', shader_code=line_fshader_code)

    line_shader_data.link('line', vertex='line', fragment='line')

    line_shader = line_shader_data.build('line')

    # endregion

    # region - - -- ----==<[ VAOS ]>==---- -- - -

    line_vertex_array = VertexArray(line_vertex_data, 'line', line_shader)

    # endregion

    # region - - -- ----==<[ HELPER FUNCTIONS ]>==---- -- - -

    def bake_lines(points, buffer=None):
        # type: (Union[list, tuple], bytearray) -> None
        verts = len(points)
        if verts > 1024:
            raise ValueError("Line is too long (more then 1024 vertices).")

        stride = Vec2.bytesize()
        data = bytearray(stride * verts) if buffer is None else buffer
        for i, (x, y) in enumerate(points):
            offset = i * stride
            Vec2.pack_values_into(x, y, buffer=data, offset=offset)

        line_vertex_array.update_data(0, data)

    # endregion

    # region - - -- ----==<[ RENDER FUNCTIONS ]>==---- -- - -

    def line_batch(window, view, projection, vert_array, count, color_a, color_b = None, tex=None, vcoord=0, blend=BlendMode.alpha):
        # type: (GLWindow, Mat4, Mat4, VertexArray, int, Union[Vec4, FrozenVec4], Optional[Union[Vec4, FrozenVec4]], Optional[TexDescription], float, BlendMode) -> None
        current = window.blend_mode
        window.blend_mode = blend
        with vert_array.render(GL_LINES, count) as shader:  # type: ShaderProgram
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load4f('start_color', *color_a)
            shader.load4f('end_color', *color_b)
            shader.load1f('point_count', count)
            shader.load1f('vcoord', vcoord)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['line_tex'].id, 0)
                shader.load1i('solidcolor', 1)
        window.blend_mode = current

    def line(window, view, projection, point_a, point_b, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha, update=True):
        # type: (GLWindow, Mat4, Mat4, Vec2, Vec2, Union[Vec4, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode, bool) -> None
        current = window.blend_mode
        if update:
            data = Vec2(point_a).pack() + Vec2(point_b).pack()   # type: bytes
            line_vertex_array.update_data(0, data)

        if not isinstance(color_b , (Vec4, FrozenVec4)):
            color_b = color_a

        window.blend_mode = blend
        with line_vertex_array.render(GL_LINES, 2) as shader:  # type: ShaderProgram
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load4f('start_color', *color_a)
            shader.load4f('end_color', *color_b)
            shader.load1f('point_count', 2.)
            shader.load1f('vcoord', vcoord)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['line_tex'].id, 0)
                shader.load1i('solidcolor', 1)
        window.blend_mode = current

    def lines(window, view, projection, points, closed, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha, update=True):
        # type: (GLWindow, Mat4, Mat4, Union[list, tuple], bool, Union[Vec4, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode, bool) -> None
        if len(points) < 2 and not closed:
            return
        if len(points) < 3 and closed:
            return

        current = window.blend_mode
        if update:
            data = Vec2(points[0]).pack()    # type: bytes
            if window.projection is Projection.ortho_down:
                h = window.height
                for (x, y) in points[1:]:
                    data += Vec2.pack_values(x, h - y)
            else:
                for (x, y) in points[1:]:
                    data += Vec2.pack_values(x, y)
            line_vertex_array.update_data(0, data)

        if not isinstance(color_b , Vec4):
            color_b = color_a

        window.blend_mode = blend
        count = max(2, min(len(points), 1024))
        with line_vertex_array.render(GL_LINE_STRIP if not closed else GL_LINE_LOOP, count) as shader:  # type: ShaderProgram
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load4f('start_color', *color_a)
            shader.load4f('end_color', *color_b)
            shader.load1f('point_count', count)
            shader.load1f('vcoord', vcoord)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['line_tex'].id, 0)
                shader.load1i('solidcolor', 1)
        window.blend_mode = current

    def lineset(window, view, projection, points, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha, update=True, count=-1):
        # type: (GLWindow, Mat4, Mat4, Union[list, tuple], Union[Vec4, FrozenVec4], Union[Vec4, FrozenVec4], float, Optional[TexDescriptor], BlendMode, bool, int) -> None
        if len(points) % 2 != 0 and update is True:
            return

        current = window.blend_mode
        if update:
            data = Vec2(points[0]).pack()    # type: bytes
            if window.projection is Projection.ortho_down:
                h = window.height
                for (x, y) in points[1:]:
                    data += Vec2.pack_values(x, h - y)
            else:
                for (x, y) in points[1:]:
                    data += Vec2.pack_values(x, y)
            line_vertex_array.update_data(0, data)

        if not isinstance(color_b , Vec4):
            color_b = color_a

        window.blend_mode = blend
        count = max(2, min(len(points), 1024)) if count == -1 else count
        count -= (count % 2) if count > 2 else 0
        with line_vertex_array.render(GL_LINES, count) as shader:  # type: ShaderProgram
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load4f('start_color', *color_a)
            shader.load4f('end_color', *color_b)
            shader.load1f('point_count', count)
            shader.load1f('vcoord', vcoord)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['line_tex'].id, 0)
                shader.load1i('solidcolor', 1)
        window.blend_mode = current


    def vline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
        # type: (GLWindow, Mat4, Mat4, Vec2, float, Union[Vec2, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode) -> None
        line(window, view, projection, start, Vec2(start) + (0, length), color_a, color_b, tex, vcoord, blend)

    def hline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
        # type: (GLWindow, Mat4, Mat4, Vec2, float, Union[Vec2, FrozenVec4], Union[Vec4, FrozenVec4], Optional[TexDescriptor], float, BlendMode) -> None
        line(window, view, projection, start, Vec2(start) + (length, 0), color_a, color_b, tex, vcoord, blend)

    def bezier(window, view, projection, points, ctrl_points, tex=None, vcoord=0, blend=BlendMode.alpha):
        # type: (GLWindow, Mat4, Mat4, Union[list, tuple], Union[list, tuple], Optional[TexDescriptor], float, BlendMode) -> None
        pass


    # endregion

    _initialized = True

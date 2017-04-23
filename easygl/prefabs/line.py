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
from easygl.structures import FrozenMat4, Vec2, Vec4
from easygl.display import BlendMode, GLWindow, Projection


__all__ = [
    'init',
    'line',
    'lines',
    'vline',
    'hline',
]


_initialized = False


# region - - -- ----==<[ STUBS ]>==---- -- - -

def line(window, view, projection, point_a, point_b, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha, update=True):
    pass


def lines(window, view, projection, points, closed, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha):
    pass


def vline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
    pass


def hline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
    pass


def bezier(window, view, projection, points, ctrl_points, tex=None, vcoord=0, blend=BlendMode.alpha):
    pass

# endregion


def init():
    # type: () -> None
    global _initialized, line, lines, vline, hline, bezier

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

    # region - - -- ----==<[  ]>==---- -- - -

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
        color = mix(start_color, end_color, gl_VertexID / point_count);
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

    # region - - -- ----==<[ RENDER FUNCTIONS ]>==---- -- - -

    def line(window, view, projection, point_a, point_b, color_a, color_b=None, tex=None, vcoord=0, blend=BlendMode.alpha, update=True):
        current = window.blend_mode
        if update:
            data = Vec2(point_a).pack() + Vec2(point_b).pack()   # type: bytes
            line_vertex_array.update_data(0, data)

        if not isinstance(color_b , Vec4):
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

    def vline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
        line(window, view, projection, start, Vec2(start) + (0, length), color_a, color_b, tex, vcoord, blend)

    def hline(window, view, projection, start, length, color_a, color_b, tex=None, vcoord=0, blend=BlendMode.alpha):
        line(window, view, projection, start, Vec2(start) + (length, 0), color_a, color_b, tex, vcoord, blend)

    def bezier(window, view, projection, points, ctrl_points, tex=None, vcoord=0, blend=BlendMode.alpha):
        pass


    # endregion

    _initialized = True

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


import math
import pygame as pg
from OpenGL.GL import GL_LINE_STRIP, GL_TRIANGLE_STRIP
from typing import Optional, Callable
from easygl.arrays import VertexArrayData, DType, attribute, vertex, VertexArray
from easygl.shaders import ShaderProgramData, ShaderProgram
from easygl.textures import TexDescriptor, TextureData, MipMap, Wrap, Filter
from easygl.structures import FrozenMat4, Vec2, Vec4
from easygl.display import BlendMode, GLWindow, Projection
import geometry as ge


__all__ = [
    'init',
    'bake_vertices',
    'stripe',
]

_initialized = False


def hypot(a):
    # type: (tuple) -> float
    """Returns the hypotenuse of point."""
    return (a[0] ** 2) + (a[1] ** 2)


def length(a):
    # type: (tuple) -> float
    return math.sqrt(hypot(a))


def normalize(a):
    # type: (tuple) -> tuple
    mag = length(a)
    if mag != 0:
        return a[0] / mag, a[1] / mag
    return 0.0, 0.0


def _get_startpoints(start, end, thickness, alignment=0.5):
    # type: (tuple, tuple) -> tuple
    alignment = max(0., min(alignment, 1.))
    sx, sy = start
    ex, ey = end
    # subtract start from end
    lx = ex - sx
    ly = ey - sy
    # normalize length
    nx, ny = normalize((lx, ly))
    # perpend
    plx, ply = -ny, nx
    prx, pry = ny, -nx
    left = thickness * alignment
    right = thickness * (1. - alignment)
    # point a
    ax = sx + (plx * left)
    ay = sy + (ply * left)
    #point b
    bx = sx + (prx * right)
    by = sy + (pry * right)

    return (ax, ay), (bx, by)


def _get_endpoints(start, end, thickness, alignment=0.5):
    # type: (tuple, tuple) -> tuple
    alignment = max(0., min(alignment, 1.))
    sx, sy = start
    ex, ey = end
    # subtract start from end
    lx = ex - sx
    ly = ey - sy
    # normalize length
    nx, ny = normalize((lx, ly))
    # perpend
    plx, ply = -ny, nx
    prx, pry = ny, -nx
    left = thickness * alignment
    right = thickness * (1. - alignment)
    # point a
    ax = ex + (plx * left)
    ay = ey + (ply * left)
    #point b
    bx = ex + (prx * right)
    by = ey + (pry * right)

    return (ax, ay), (bx, by)


def stripe(window, view, projection, points, color_a, color_b=None, tex=None, vcoord=0., blend=BlendMode.alpha,
           update=True):
    # type: (GLWindow, Mat4, Mat4, Union[tuple, list], Vec4, Optional[Vec4], Optional[TextDescriptor], float, BlendMode, bool) -> None
    pass

# region - - -- ----==<[ BAKER ]>==---- -- - -

def bake_vertices(points, thickness):
    start = points[0]
    end = points[1]
    baked = []
    a, b = _get_startpoints(start, end, thickness)
    baked.append(a)
    baked.append(b)
    for i, end in enumerate(points[1:], 1):
        c, d = _get_endpoints(start, end, thickness)
        start = end
        baked.append(c)
        baked.append(d)
    return tuple(baked)

# endregion


def init():
    # type: () -> None
    global _initialized, stripe, stripe_array_data, bake_vertices, texdata, line_shader_data, line_shader

    # region - - -- ----==<[ ARRAY DATA ]>==---- -- - -

    stripe_array_data = VertexArrayData()

    with stripe_array_data.definition():
        attribute('position', DType.float_v2)
        # attribute('texcoord', DType.float_v2)

    with stripe_array_data.new_primitive('stripe', 1024):
        for i in range(1024):
            vertex(position=(0., 0.))

    # endregion

    # region - - -- ----==<[ TEXTURES ]>==---- -- - -

    s = pg.Surface((4, 1))
    s.fill((255, 255, 255))
    texdata = TextureData()
    texdata.create_from_surface('line_tex', s, False, False, MipMap.linear_linear, Wrap.repeat, Filter.linear)

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

    line_vertex_array = VertexArray(stripe_array_data, 'stripe', line_shader)

    # endregion

    # region - - -- ----==<[ RENDER FUNCTIONS ]>==---- -- - -

    def stripe(window, view, projection, points, color_a, color_b=None, tex=None, vcoord=0., blend=BlendMode.alpha, update=True):
        # type: (GLWindow, Mat4, Mat4, Union[tuple, list], Vec4, Optional[Vec4], Optional[TextDescriptor], float, BlendMode, bool) -> None
        if len(points) < 4:
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
        with line_vertex_array.render(GL_TRIANGLE_STRIP, count) as shader:  # type: ShaderProgram
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

    # endregion

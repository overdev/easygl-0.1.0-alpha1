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
from OpenGL.GL import GL_LINE_STRIP, GL_TRIANGLES
from typing import Optional, Callable
from easygl.arrays import VertexArrayData, DType, attribute, vertex, vertex_copy, VertexArray
from easygl.shaders import ShaderProgramData, ShaderProgram
from easygl.textures import TexDescriptor, TextureData, MipMap, Wrap, Filter
from easygl.structures import FrozenMat4, Vec2, Vec4
from easygl.display import BlendMode, GLWindow


__all__ = [
    'init',
    'rect_line',
    'rect_fill',
    'oriented_rect_line',
    'oriented_rect_fill',
]


_initialized = False


# region - - -- ----==<[ STUBS ]>==---- -- - -

def rect_line(window, view, projection, position, size, origin, color, tex=None, vcoord=0., blend=BlendMode.alpha):
    # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, Vec4, Optional[TexDescriptor], Optional[float], BlendMode) -> None
    pass


def oriented_rect_line(window, view, projection, position, size, origin, angle, color, tex=None, vcoord=0., blend=BlendMode.alpha):
    # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, float, Vec4, Optional[TexDescriptor], Optional[float], BlendMode) -> None
    pass


def rect_fill(window, view, projection, position, size, origin, color, blend=BlendMode.alpha):
    # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, Vec4, BlendMode) -> None
    pass


def oriented_rect_fill(window, view, projection, position, size, origin, angle, color, blend=BlendMode.alpha):
    # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, float, Vec4, BlendMode) -> None
    pass

# endregion


def init():
    global _initialized, rect_line, oriented_rect_line, rect_fill, oriented_rect_fill

    if _initialized:
        return

    # region - - -- ----==<[ ARRAY DATA ]>==---- -- - -

    rectangle_vertex_data = VertexArrayData()

    with rectangle_vertex_data.definition():
        attribute('position', DType.float_v2)
        attribute('ucoord', DType.float)

    with rectangle_vertex_data.new_primitive('quad_line', 4):
        vertex(position=(1., 1.), ucoord=0.)  # top right
        vertex(position=(1., 0.), ucoord=1.)  # bottom right
        vertex(position=(0., 0.), ucoord=0.)  # bottom left
        vertex(position=(0., 1.), ucoord=1.)  # top left
        vertex_copy(0)

    with rectangle_vertex_data.new_primitive('quad_fill', 6, ucoord=0.):
        vertex(position=(1., 1.))  # top right
        vertex(position=(1., 0.))  # bottom right
        vertex(position=(0., 1.))  # top left
        vertex_copy(1)
        vertex(position=(0., 0.))  # bottom left
        vertex_copy(2)

    # endregion

    # region - - -- ----==<[ TEXTURES ]>==---- -- - -

    s = pg.Surface((4, 1))
    s.fill((255, 255, 255))
    texdata = TextureData()
    texdata.create_from_surface('rect_tex', s, False, False, MipMap.linear_linear, Wrap.repeat,
                                Filter.linear)
    # endregion

    # region - - -- ----==<[ SHADERS ]>==---- -- - -

    rect_vshader_code = """
    #version 330 core
    
    in vec2 position;
    in float ucoord;
    
    uniform vec2 origin;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    uniform float vcoord;
    
    out vec2 coord;

    void main() {

        gl_Position = projection * view * model * vec4(position - origin, 0.f, 1.f);
        coord = vec2(ucoord, vcoord);
    }
    """
    rect_fshader_code = """
    #version 330 core
    
    in vec2 coord;
    
    uniform vec4 color;
    uniform sampler2D tex;
    uniform bool solidcolor;
    
    void main() {
    
        vec4 texcolor = texture(tex, coord);
        if (solidcolor)
            texcolor = vec4(1.f, 1.f, 1.f, 1.f);
        gl_FragColor = texture(tex, coord) * color;
    }
    
    """

    rect_shader_data = ShaderProgramData("")
    rect_shader_data.compile_vertex_shader('rect', shader_code=rect_vshader_code)
    rect_shader_data.compile_fragment_shader('rect', shader_code=rect_fshader_code)

    rect_shader_data.link('rect_shader', vertex='rect', fragment='rect')

    rect_shader = rect_shader_data.build('rect_shader')

    # endregion

    # region - - -- ----==<[ VAOS ]>==---- -- - -

    rectline_vertex_array = VertexArray(rectangle_vertex_data, 'quad_line', rect_shader)
    rectfill_vertex_array = VertexArray(rectangle_vertex_data, 'quad_fill', rect_shader)

    # endregion

    # region - - -- ----==<[ RENDER FUNCTIONS ]>==---- -- - -

    def rect_line(window, view, projection, position, size, origin, color, tex=None, vcoord=0., blend=BlendMode.alpha):
        # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, Vec4, Optional[TexDescriptor], Optional[float], BlendMode) -> None
        model = FrozenMat4.transform(Vec4(position, 0., 1.), 0., Vec4(size, 0., 1.))
        current = window.blend_mode
        window.blend_mode = blend
        with rectline_vertex_array.render(GL_LINE_STRIP) as shader:   # type: ShaderProgram
            shader.load2f('origin', *origin)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load1f('vcoord', vcoord)
            shader.load4f('color', *color)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['rect_tex'].id, 0)
                shader.load1i('solidcolor', 1)
        window.blend_mode = current


    def oriented_rect_line(window, view, projection, position, size, origin, angle, color, tex=None, vcoord=0., blend=BlendMode.alpha):
        # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, float, Vec4, Optional[TexDescriptor], Optional[float], BlendMode) -> None
        model = FrozenMat4.transform(Vec4(position, 0., 1.), angle, Vec4(size, 0., 1.))
        current = window.blend_mode
        window.blend_mode = blend
        with rectline_vertex_array.render(GL_LINE_STRIP) as shader:   # type: ShaderProgram
            shader.load2f('origin', *origin)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load1f('vcoord', vcoord)
            shader.load4f('color', *color)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['rect_tex'].id, 0)
                shader.load1i('solidcolor', 1)
        window.blend_mode = current


    def rect_fill(window, view, projection, position, size, origin, color, blend=BlendMode.alpha):
        # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, Vec4, BlendMode) -> None
        model = FrozenMat4.transform(Vec4(position, 0., 1.), 0., Vec4(size, 0., 1.))
        current = window.blend_mode
        window.blend_mode = blend
        with rectfill_vertex_array.render(GL_TRIANGLES) as shader:   # type: ShaderProgram
            shader.load2f('origin', *origin)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load1f('vcoord', 0.)
            shader.load4f('color', *color)
            shader.load_sampler2d('tex', texdata['rect_tex'].id, 0)
            shader.load1i('solidcolor', 1)
        window.blend_mode = current


    def oriented_rect_fill(window, view, projection, position, size, origin, angle, color, blend=BlendMode.alpha):
        # type: (GLWindow, FrozenMat4, FrozenMat4, Vec2, Vec2, Vec2, float, Vec4, BlendMode) -> None
        model = FrozenMat4.transform(Vec4(position, 0., 1.), angle, Vec4(size, 0., 1.))
        current = window.blend_mode
        window.blend_mode = blend
        with rectfill_vertex_array.render(GL_TRIANGLES) as shader:  # type: ShaderProgram
            shader.load2f('origin', *origin)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load1f('vcoord', 0.)
            shader.load4f('color', *color)
            shader.load_sampler2d('tex', texdata['rect_tex'].id, 0)
            shader.load1i('solidcolor', 1)
        window.blend_mode = current

    # endregion

    _initialized = True

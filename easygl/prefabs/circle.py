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
from OpenGL.GL import GL_LINES, GL_LINE_STRIP
from typing import Optional, Callable
from easygl.arrays import VertexArrayData, DType, attribute, vertex, VertexArray
from easygl.shaders import ShaderProgramData, ShaderProgram
from easygl.textures import TexDescriptor, TextureData, MipMap, Wrap, Filter
from easygl.structures import FrozenMat4, Vec2, Vec4
from easygl.display import BlendMode, GLWindow


__all__ = [
    'MAX_PRECISION',
    'circle_line',
    'arc_line',
    'init',
]


MAX_PRECISION = 721
_initialized = False


def circle_line(window, view, projection, position, rotation, radius, color, precision, tex=None, vcoord=0.,
                blend=BlendMode.alpha):
    # type: (GLWindow, Mat4, Mat4, Vec2, float, float, Vec4, int, Optional[TexDescriptor], float) -> None
    pass


def arc_line(window, view, projection, position, rotation, radius, start, end, color, precision, tex=None, vcoord=0.,
             blend=BlendMode.alpha):
    # type: (GLWindow, Mat4, Mat4, Vec2, float, float, float, float, Vec4, float, Optional[TexDescriptor], float, BlendMode) -> None
    pass


def pie_line(window, view, projection, position, rotation, radius, start, end, color, precision, tex=None, vcoord=0.,
             blend=BlendMode.alpha):
    # type: (GLWindow, Mat4, Mat4, Vec2, float, float, float, float, Vec4, float, Optional[TexDescriptor], float, BlendMode) -> None
    pass


def init():
    global _initialized, circle_line, arc_line, pie_line, circle_shader_data, circle_vertex_array, circle_shader, texdata

    # region - - -- ----==<[ ARRAYS ]>==---- -- - -

    circle_vertex_data = VertexArrayData()

    with circle_vertex_data.definition():
        attribute('idx', DType.ubyte)

    with circle_vertex_data.new_primitive('indices', MAX_PRECISION + 1):
        for i in range(MAX_PRECISION + 1):
            vertex(index=0)

    # endregion

    # region - - -- ----==<[ TEXTURES ]>==---- -- - -

    s = pg.Surface((4, 1))
    s.fill((255, 255, 255))
    texdata = TextureData()
    texdata.create_from_surface('circle_line_tex', s, False, False, MipMap.linear_linear, Wrap.repeat, Filter.linear)

    # endregion

    # region - - -- ----==<[ SHADERS ]>==---- -- - -

    circle_vshader_code = """
    #version 330 core
    
    in float idx;
    
    uniform float circle_prec;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    uniform float vcoord;
   
    out vec2 coord;
   
    vec4 vertex(float num, float den) {
    
        float ang = radians((num / den) * 360.0f);
        
        return vec4(cos(ang), sin(ang), 0.0f, 1.0f);

    }

    void main() {
    
        gl_Position = projection * view * model * vertex(gl_VertexID, circle_prec + idx);
        coord = vec2(gl_VertexID / circle_prec, vcoord);

    }
    """
    circle_fshader_code = """
    #version 330 core
    
    in vec2 coord;
    
    uniform sampler2D tex;
    uniform vec4 color;
    uniform bool solidcolor;
    
    void main() {
    
        if (solidcolor)
            gl_FragColor = color;
        else
            gl_FragColor = color * texture(tex, coord);
    }
    """

    arc_vshader_code = """
    #version 330 core
    
    in int idx;
    
    uniform float angle;
    uniform float theta;
    uniform float arc_prec;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    uniform float vcoord;
    
    out vec2 coord;
    
    void main() {
    
        float i = idx - idx;
        float step = (gl_VertexID + i) / arc_prec;
        float micro = step * theta;
        float arc_angle = mod(angle + micro, 360.0f);
        float rad = radians(arc_angle);
        vec4 position = vec4(cos(rad), sin(rad), 0.0f, 1.0f);
        
        gl_Position = projection * view * model * position;
        coord = vec2(step, vcoord);

    }
    """
    pie_vshader_code = """
    #version 330 core
    
    in int idx;
    
    uniform float angle;
    uniform float theta;
    uniform float arc_prec;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    uniform float vcoord;
    
    out vec2 coord;
    
    void main() {
    
        float step = (gl_VertexID + idx) / arc_prec;
        float micro = ((gl_VertexID + idx) / (arc_prec - 2)) * theta;
        float arc_angle = mod(angle + micro, 360.0f);
        float rad = radians(arc_angle);
        
        vec4 position = vec4(cos(rad), sin(rad), 0.0f, 1.0f);
        if (step == 0.0f || step == 1.0f)
            position = vec4(0.0f, 0.0f, 0.0f, 1.0f);
        
        gl_Position = projection * view * model * position;
        coord = vec2(step, vcoord);

    }
    """

    circle_shader_data = ShaderProgramData("")
    circle_shader_data.compile_vertex_shader('circle', shader_code=circle_vshader_code)
    circle_shader_data.compile_fragment_shader('circle', shader_code=circle_fshader_code)

    circle_shader_data.compile_vertex_shader('arc', shader_code=arc_vshader_code)
    circle_shader_data.compile_vertex_shader('pie', shader_code=pie_vshader_code)

    circle_shader_data.link('circle_shader', vertex='circle', fragment='circle')
    circle_shader_data.link('arc_shader', vertex='arc', fragment='circle')
    circle_shader_data.link('pie_shader', vertex='pie', fragment='circle')

    circle_shader = circle_shader_data.build(
        'circle_shader',
        circle_prec=DType.float,
        model=DType.float_m4,
        view=DType.float_m4,
        projection=DType.float_m4,
        vcoord=DType.float,
        tex=DType.int,
        color=DType.float_v4,
        solidcolor=DType.bool
    )

    arc_shader = circle_shader_data.build(
        'arc_shader',
        angle=DType.float,
        theta=DType.float,
        arc_prec=DType.float,
        model=DType.float_m4,
        view=DType.float_m4,
        projection=DType.float_m4,
        vcoord=DType.float,
        tex=DType.int,
        color=DType.float_v4,
        solidcolor=DType.bool
    )

    pie_shader = circle_shader_data.build(
        'pie_shader',
        angle=DType.float,
        theta=DType.float,
        arc_prec=DType.float,
        model=DType.float_m4,
        view=DType.float_m4,
        projection=DType.float_m4,
        vcoord=DType.float,
        tex=DType.int,
        color=DType.float_v4,
        solidcolor=DType.bool
    )

    # endregion

    # region - - -- ----==<[ VAOS ]>==---- -- - -

    circle_vertex_array = VertexArray(circle_vertex_data, 'indices', circle_shader)
    arc_vertex_array = VertexArray(circle_vertex_data, 'indices', arc_shader)
    pie_vertex_array = VertexArray(circle_vertex_data, 'indices', pie_shader)

    # endregion

    # region - - -- ----==<[ RENDER FUNCTIONS ]>==---- -- - -

    def circle_line(window, view, projection, position, rotation, radius, color, precision, tex=None, vcoord=0., blend=BlendMode.alpha):
        # type: (GLWindow, Mat4, Mat4, Vec2, float, float, Vec4, int, Optional[TexDescriptor], float) -> None
        count = max(8, min(precision, MAX_PRECISION))
        model = FrozenMat4.transform(Vec4(position, 0., 1.), rotation, Vec4(radius, radius, 0., 1.))

        current = window.blend_mode
        window.blend_mode = blend
        with circle_vertex_array.render(GL_LINE_STRIP, count + 1) as shader:   # type: ShaderProgram
            shader.load1f('circle_prec', count)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load1f('vcoord', vcoord)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['circle_line_tex'].id, 0)
                shader.load1i('solidcolor', 1)
            shader.load4f('color', *color)

        window.blend_mode = current


    def arc_line(window, view, projection, position, rotation, radius, start, end, color, precision, tex=None, vcoord=0., blend=BlendMode.alpha):
        # type: (GLWindow, Mat4, Mat4, Vec2, float, float, float, float, Vec4, float, Optional[TexDescriptor], float, BlendMode) -> None
        a = start % 360.
        b = end % 360.
        if b < a:
            theta = (360. - a) + b
        else:
            theta = b - a
        if theta == 0:
            return

        model = FrozenMat4.transform(Vec4(position, 0., 1.), rotation, Vec4(radius, radius, 0., 1.))
        arc_prec = int(max(2, min(precision, MAX_PRECISION -1)))
        current = window.blend_mode
        window.blend_mode = blend
        with arc_vertex_array.render(GL_LINE_STRIP, arc_prec) as shader:   # type: ShaderProgram
            shader.load1f('angle', a + 1)
            shader.load1f('theta', theta)
            shader.load1f('arc_prec', arc_prec)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load1f('vcoord', vcoord)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['circle_line_tex'].id, 0)
                shader.load1i('solidcolor', 1)
            shader.load4f('color', *color)

        window.blend_mode = current


    def pie_line(window, view, projection, position, rotation, radius, start, end, color, precision, tex=None, vcoord=0., blend=BlendMode.alpha):

        a = start % 360.
        b = end % 360.
        if b < a:
            theta = (360. - a) + b
        else:
            theta = b - a
        if theta == 0:
            return

        model = FrozenMat4.transform(Vec4(position, 0., 1.), rotation, Vec4(radius, radius, 0., 1.))
        arc_prec = int(max(5, precision / (360. / theta)))
        current = window.blend_mode
        window.blend_mode = blend
        with pie_vertex_array.render(GL_LINE_STRIP, arc_prec) as shader:  # type: ShaderProgram
            shader.load1f('angle', a)
            shader.load1f('theta', theta)
            shader.load1f('arc_prec', arc_prec - 1)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, tuple(view))
            shader.load_matrix4f('projection', 1, False, tuple(projection))
            shader.load1f('vcoord', vcoord)
            if isinstance(tex, TexDescriptor):
                shader.load_sampler2d('tex', tex.id, 0)
                shader.load1i('solidcolor', 0)
            else:
                shader.load_sampler2d('tex', texdata['circle_line_tex'].id, 0)
                shader.load1i('solidcolor', 1)
            shader.load4f('color', *color)

        window.blend_mode = current
    # endregion

    _initialized = True

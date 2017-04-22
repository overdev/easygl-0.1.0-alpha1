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

VERTEXARRAYDATA = {}
SHADERPROGRAMDATA = ShaderProgramData("")
SHADERPROGRAM = {}
VERTEXARRAY = {}


def get(prefab):
    # type: (int) -> Optional[VertexArray]
    if prefab & INITIALIZED_DATA != prefab:
        return None
    return VERTEXARRAY[prefab]


def init_sprite_static():
    # type: () -> None
    global INITIALIZED_DATA
    if SPRITE_STATIC & INITIALIZED_DATA != 0:
        return

    vertex_array_data = VertexArrayData()
    VERTEXARRAYDATA[SPRITE_STATIC] = vertex_array_data
    with vertex_array_data.definition():
        attribute('position', DType.float_v2)
        attribute('texcoord', DType.float_v2)

    with vertex_array_data.new_primitive('sprite_static', 6):
        vertex(position=(.5, .5), texcoord=(1.0, 1.0))  # Top Right
        vertex(position=(.5, -.5), texcoord=(1.0, 0.0))  # Bottom Right
        vertex(position=(-.5, .5), texcoord=(0.0, 1.0))  # Top Left
        vertex_copy(1)
        vertex(position=(-.5, -.5), texcoord=(0.0, 0.0))  # Bottom Left
        vertex_copy(2)

    vsh_sprite_static = """
    #version 330 core
    
    in vec2 position;
    in vec2 texcoord;
    
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    
    out vec2 coord;
    
    void main() {
    
        gl_Position = projection * view * model * vec4(position, 0.0f, 1.0f);
        coord = texcoord;
    }
    """
    fsh_sprite_static = """
    #version 330 core
    
    in vec2 coord;
    
    uniform sampler2D tex;
    uniform vec4 color;
    
    void main() {
    
        gl_FragColor = texture(tex, coord) * color;
    
    }
    """

    SHADERPROGRAMDATA.compile_vertex_shader('sprite_static', shader_code=vsh_sprite_static)
    # SPRITE_STATIC & SPRITE_ANIMATED shares the same fragment shader, so, if SPRITE_ANIMATED is already initialized,
    # then the compiled fragment shader is used.
    if INITIALIZED_DATA & SPRITE_ANIMATED == 0:
        SHADERPROGRAMDATA.compile_fragment_shader('sprite', shader_code=fsh_sprite_static)

    SHADERPROGRAMDATA.link('sprite_static', vertex='sprite_static', fragment='sprite')

    SHADERPROGRAM[SPRITE_STATIC] = SHADERPROGRAMDATA.build(
        'sprite_static',
        'model', 'view', 'projection', 'tex', 'color'
    )

    VERTEXARRAY[SPRITE_STATIC] = VertexArray(
        VERTEXARRAYDATA[SPRITE_STATIC], 'sprite_static', SHADERPROGRAM[SPRITE_STATIC])

    INITIALIZED_DATA |= SPRITE_STATIC


def init_sprite_animated():
    # type: () -> None
    global INITIALIZED_DATA
    if SPRITE_ANIMATED & INITIALIZED_DATA != 0:
        return

    vertex_array_data = VertexArrayData()
    VERTEXARRAYDATA[SPRITE_ANIMATED] = vertex_array_data
    with vertex_array_data.definition():
        attribute('position', DType.float_v2)

    with vertex_array_data.new_primitive('sprite_animated', 6):
        vertex(position=(.5, .5))  # Top Right
        vertex(position=(.5, -.5))  # Bottom Right
        vertex(position=(-.5, .5))  # Top Left
        vertex_copy(1)
        vertex(position=(-.5, -.5))  # Bottom Left
        vertex_copy(2)

    vsh_sprite_animated = """
        #version 330 core

        in vec2 position;
        in vec2 texcoord;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        out vec2 coord;

        void main() {

            gl_Position = projection * view * model * vec4(position, 0.0f, 1.0f);
            coord = texcoord;
        }
        """
    fsh_sprite_animated = """
    #version 330 core
    
    in vec2 position;
    
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    //uniform vec2 bottomleft;
    //uniform vec2 topright;
    uniform vec4 lefttoprightbottom;

    /*
    vec2 coords[6] = vec2[](
        topright,
        vec2(topright.x, bottomleft.y),
        vec2(bottomleft.x, topright.y),
        vec2(topright.x, bottomleft.y),
        bottomleft,
        vec2(bottomleft.x, topright.y)
    );
    */
    out vec2 coord;
    
    vec2 getCoord(vec4 ltrb, float index) {
    //           T     Y
    // xyzw     L R   X Z
    // ltrb      B     W
    if (index == 0)                         // top right
        return ltrb.zy;
    else if (index == 1 || index == 3)      // bottom right
        return ltrb.zw;
    else if (index == 2 || index == 5)      // top left
        return ltrb.xy;
    else                                    // bottom left
        return ltrb.xw;
}

    void main() {
        gl_Position = projection * model * view * vec4(position, 1.0f, 1.0f);
    
        coord = getCoord(lefttoprightbottom, gl_VertexID);
    
    }
    """

    SHADERPROGRAMDATA.compile_vertex_shader('sprite_animated', shader_code=vsh_sprite_animated)
    # SPRITE_STATIC & SPRITE_ANIMATED shares the same fragment shader, so, if SPRITE_STATIC is already initialized,
    # then the compiled fragment shader is used.
    if INITIALIZED_DATA & SPRITE_STATIC == 0:
        SHADERPROGRAMDATA.compile_fragment_shader('sprite', shader_code=fsh_sprite_animated)

    SHADERPROGRAMDATA.link('sprite_animated', vertex='sprite_animated', fragment='sprite')

    SHADERPROGRAM[SPRITE_ANIMATED] = SHADERPROGRAMDATA.build(
        'sprite_animated',
        "model", "view", "projection", "lefttoprightbottom", "color", "tex"
    )

    VERTEXARRAY[SPRITE_ANIMATED] = VertexArray(
        VERTEXARRAYDATA[SPRITE_ANIMATED], 'sprite_animated', SHADERPROGRAM[SPRITE_ANIMATED])

    INITIALIZED_DATA |= SPRITE_ANIMATED


def init_circle_line():
    global INITIALIZED_DATA
    if CIRCLE_LINE & INITIALIZED_DATA != 0:
        return

    if INITIALIZED_DATA & (PIE_ELLIPSE_LINE | ARC_CIRCLE) == 0:
        vertex_array_data = VertexArrayData()
        VERTEXARRAYDATA[CIRCLE_LINE] = vertex_array_data
        with vertex_array_data.definition():
            attribute('idx', DType.float)

        with vertex_array_data.new_primitive('circle_arc_pie_line', MAX_PRECISION + 1):
            for i in range(MAX_PRECISION + 1):
                vertex(index=float(i))

    vsh_circle_line = """
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
    fsh_circle_line = """
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

    SHADERPROGRAMDATA.compile_vertex_shader('circle_line', shader_code=vsh_circle_line)

    if INITIALIZED_DATA & (PIE_ELLIPSE_LINE | ARC_CIRCLE) != 0:
        SHADERPROGRAMDATA.compile_fragment_shader('circle_arc_pie_line', shader_code=fsh_circle_line)

    SHADERPROGRAMDATA.link('circle_line', vertex='circle_line', fragment='circle_arc_pie_line')

    SHADERPROGRAM[CIRCLE_LINE] = SHADERPROGRAMDATA.build(
        'circle_line',
        "circle_prec", "model", "view", "projection", "vcoord", "color", "tex", "solidcolor"
    )

    VERTEXARRAY[CIRCLE_LINE] = VertexArray(
        VERTEXARRAYDATA[CIRCLE_LINE], 'circle_arc_pie_line', SHADERPROGRAM[CIRCLE_LINE])

    INITIALIZED_DATA |= CIRCLE_LINE


def init_circle_fill():
    global INITIALIZED_DATA
    if CIRCLE_FILL & INITIALIZED_DATA != 0:
        return

    if INITIALIZED_DATA & CIRCLE == 0:
        vertex_array_data = VertexArrayData()
        VERTEXARRAYDATA[CIRCLE_FILL] = vertex_array_data
        with vertex_array_data.definition():
            attribute('idx', DType.float)

        with vertex_array_data.new_primitive('circle_arc_pie_fill', MAX_PRECISION + 1):
            for i in range(MAX_PRECISION + 1):
                vertex(index=float(i))

    vsh_circle_fill = """
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
    fsh_circle_fill = """
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

    SHADERPROGRAMDATA.compile_vertex_shader('circle_fill', shader_code=vsh_circle_line)

    if INITIALIZED_DATA & (PIE_ELLIPSE_LINE | ARC_CIRCLE) != 0:
        SHADERPROGRAMDATA.compile_fragment_shader('circle_arc_pie_fill', shader_code=fsh_circle_line)

    SHADERPROGRAMDATA.link('circle_fill', vertex='circle_fill', fragment='circle_arc_pie_fill')

    SHADERPROGRAM[CIRCLE_FILL] = SHADERPROGRAMDATA.build(
        'circle_fill',
        "circle_prec", "model", "view", "projection", "vcoord", "color", "tex", "solidcolor"
    )

    VERTEXARRAY[CIRCLE_FILL] = VertexArray(
        VERTEXARRAYDATA[CIRCLE_FILL], 'circle_arc_pie_fill', SHADERPROGRAM[CIRCLE_FILL])

    INITIALIZED_DATA |= CIRCLE_FILL

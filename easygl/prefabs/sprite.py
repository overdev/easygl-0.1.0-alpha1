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
from easygl.arrays import VertexArrayData, attribute, vertex, vertex_copy, DType
from easygl.shaders import ShaderProgramData, ShaderProgram
from easygl.arrays.arraybuffers import VertexArray
from easygl.structures import Vec2, Vec4, Mat4
from easygl.textures import TexDescriptor, TexSubImageDescriptor
from easygl.display import BlendMode
from OpenGL.GL import GL_TRIANGLES


__all__ = [
    'SpriteState',
    'AnimationState',
]

_initialized = False
# SpriteState = None


def init():
    global SpriteState, AnimationState, _initialized

    if _initialized:
        return

    # region - - -- ----==<[ SPRITE VEXTEX DATA ]>==---- -- - -

    SpriteVertexData = VertexArrayData()

    with SpriteVertexData.definition():
        attribute('position', DType.float_v2)
        attribute('texcoord', DType.float_v2)

    with SpriteVertexData.new_primitive('sprite', 6):
        vertex(position=(.5, .5), texcoord=(1.0, 1.0))  # Top Right
        vertex(position=(.5, -.5), texcoord=(1.0, 0.0))  # Bottom Right
        vertex(position=(-.5, .5), texcoord=(0.0, 1.0))  # Top Left
        vertex_copy(1)
        vertex(position=(-.5, -.5), texcoord=(0.0, 0.0))  # Bottom Left
        vertex_copy(2)

    AnimatedVertexData = VertexArrayData()

    with AnimatedVertexData.definition():
        attribute('position', DType.float_v2)

    with AnimatedVertexData.new_primitive('anim_sprite', 6):
        vertex(position=(.5, .5))  # Top Right
        vertex(position=(.5, -.5))  # Bottom Right
        vertex(position=(-.5, .5))  # Top Left
        vertex_copy(1)
        vertex(position=(-.5, -.5))  # Bottom Left
        vertex_copy(2)

    # endregion

    # region - - -- ----==<[ SPRITE SHADER CODE, DATA & PROGRAMS ]>==---- -- - -

    sprite_vshader = """
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
    sprite_fshader = """
    #version 330 core
    
    in vec2 coord;
    
    uniform sampler2D tex;
    uniform vec4 color;
    
    void main() {
    
        gl_FragColor = texture(tex, coord) * color;
    
    }
    """
    anim_sprite_vshader = """
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

    SpriteShaderData = ShaderProgramData("")

    SpriteShaderData.compile_fragment_shader('sprite', shader_code=sprite_fshader)
    SpriteShaderData.compile_vertex_shader('sprite', shader_code=sprite_vshader)
    SpriteShaderData.compile_vertex_shader('anim_sprite', shader_code=anim_sprite_vshader)

    SpriteShaderData.link('sprite_shader', fragment='sprite', vertex='sprite')
    SpriteShaderData.link('anim_sprite_shader', fragment='sprite', vertex='anim_sprite')

    sprite_program = SpriteShaderData.build(
        'sprite_shader',
        "model", "view", "projection", "color", "tex"
    )

    anim_sprite_program = SpriteShaderData.build(
        'anim_sprite_shader',
        "model", "view", "projection", "lefttoprightbottom", "color", "tex"
    )
    # endregion

    # region - - -- ----==<[ SPRITE VERTEXARRAYS ]>==---- -- - -

    sprite_array = VertexArray(SpriteVertexData, 'sprite', sprite_program)
    anim_sprite_array = VertexArray(AnimatedVertexData, 'anim_sprite', anim_sprite_program)

    # endregion

    # region - - -- ----==<[ RENDER FUNCTIONS ]>==---- -- - -

    def draw_sprite(texture, position):
        pass

    # endregion

    # region - - -- ----==<[ SPRITE RENDER STATE ]>==---- -- - -

    class SpriteState(object):

        def __init__(self, texdescriptor):
            # type: (TexDescriptor) -> None
            self._texdescriptor = texdescriptor
            self._position = Vec2(0., 0.)
            self._rotation = 0.
            self._scaling = Vec2(1., 1.)
            self._color = Vec4(1., 1., 1., 1.)
            self._blend = BlendMode.alpha
            self._alpha = 1.

        @property
        def position(self):
            # type: () -> Vec2
            return self._position

        @position.setter
        def position(self, value):
            self._position.xy = value

        @property
        def rotation(self):
            return self._rotation

        @rotation.setter
        def rotation(self, value):
            self._rotation = float(value) % 360.

        @property
        def scaling(self):
            return self._scaling.xy

        @scaling.setter
        def scaling(self, value):
            self._scaling.xy = value

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            self._color.rgba = value

        @property
        def blend(self):
            return self._blend

        @blend.setter
        def blend(self, value):
            # type: (BlendMode) -> None
            if value is BlendMode:
                self._blend = value

        @property
        def alpha(self):
            return self._alpha

        @alpha.setter
        def alpha(self, value):
            self._alpha = max(0., min(value, 1.))

        def render(self, view, projection):
            # type: (Mat4, Mat4) -> None
            model = tuple(Mat4.transform(
                Vec4(self._position, 0., 1.),
                self._rotation,
                Vec4(self._scaling * self._texdescriptor.size, 0., 1.)
            ))
            color = Vec4(self._color.rgb, self._color.a * self._alpha)

            with sprite_array.render(GL_TRIANGLES) as shader:   # type: ShaderProgram
                shader.load_matrix4f('model', 1, False, model)
                shader.load_matrix4f('view', 1, False, tuple(view))
                shader.load_matrix4f('projection', 1, False, tuple(projection))
                shader.load4f('color', *color)
                shader.load_sampler2d('tex', self._texdescriptor.id, 0)


    class AnimationState(SpriteState):

        def __init__(self, texsubimagedescriptor):
            # type: (TexSubImageDescriptor) -> None
            super(AnimationState, self).__init__(texsubimagedescriptor.tex_descriptor)
            self._anim_descriptor = texsubimagedescriptor
            self._subimage = 0
            self._flip_speed = 1.

        @property
        def subimage(self):
            # type: () -> int
            return int(round(self._subimage, 0) % self._anim_descriptor.image_count)

        @subimage.setter
        def subimage(self, value):
            # type: (Union[int, float]) -> None
            self._subimage = float(value)

        @property
        def flip_speed(self):
            # type: () -> float
            return self._flip_speed

        @flip_speed.setter
        def flip_speed(self, value):
            # type: (float) -> None
            self._flip_speed = float(value)

        def render(self, view, projection):
            # type: (Mat4, Mat4) -> None
            model = tuple(Mat4.transform(
                Vec4(self._position, 0., 1.),
                self._rotation,
                Vec4(self._scaling * self._anim_descriptor.image_size, 0., 1.)
            ))
            image_index = int(round(self._subimage, 0)) % self._anim_descriptor.image_count
            l, t, r, b = self._anim_descriptor.bboxes[image_index]
            color = Vec4(self._color.rgb, self._color.a * self._alpha)

            with anim_sprite_array.render(GL_TRIANGLES)  as shader:   # type: ShaderProgram
                shader.load_matrix4f('model', 1, False, model)
                shader.load_matrix4f('view', 1, False, tuple(view))
                shader.load_matrix4f('projection', 1, False, tuple(projection))
                shader.load4f('lefttoprightbottom', l, t, r, b)
                shader.load4f('color', *color)
                shader.load_sampler2d('tex', self._texdescriptor.id, 0)

            if self._flip_speed != 0:
                self._subimage = (self._subimage + self._flip_speed) % self._anim_descriptor.image_count

    # endregion
    _initialized = True

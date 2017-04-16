easygl
======

`easygl` is a small python package made on top of **PyGame** and **PyOpenGL** for easy
easy rendering of 2D graphics. `easygl` makes easy the creation of shapes,
textures, VAOs and comes with a small set of _ready-to-use_ drawing functions similar to
those in PyGame's draw module.

Features
---
+ Easy definition and creation of vertex array attributes without a single OpenGL call.
+ Easy creation of textures from image files, PyGame surfaces or screen capture.
+ Easy compilation of shader code, linkage and reuse of compiled shaders.
+ Easy and simplified process of passing uniform data to shader programs.
+ Vector classes (Vec2, Vec3 and Vec4) that supports attribute swizzling, like `position.zxyy` or `color.grba`.
+ Matrix classes (Mat2, Mat3 and Mat4).

Examples
---
### Defining and creating a textured quad ###

```python
from easygl.arrays import VertexArrayData, DType, attribute, vertex, vertex_copy

# VertexArrayData instances stores the vertex attribute definition
textured_quad = VertexArrayData()

# the vertex attributes are defined like this:
with textured_quad.definition():
    attribute('position', DType.float_v2)
    attribute('texcoord', DType.float_v2)

# now is possible to define geometries that shares the same vertex definition:
with textured_quad.new_primitive('texquad', 6):
    vertex(position=(.5, .5),  texcoord=(1.0, 1.0))   # Top Right
    vertex(position=(.5, -.5), texcoord=(1.0, 0.0))   # Bottom Right
    vertex(position=(-.5, .5), texcoord=(0.0, 1.0))   # Top Left
    vertex_copy(1)   # copies the Bottom Right vertex
    vertex(position=(-.5, -.5), texcoord=(0.0, 0.0))  # Bottom Left
    vertex_copy(2)   # copies the Top Left vertex
```

### Initializing the display ###
The piece of code below shows how the PyGame window is initialized with an OpenGL context.
There's nothing special about `GLWindow` object (except that only one instance should exist at a time),
its job is to only simplify the setup and most common input, display and rendering operations.

It must be initialize before OpenGL operations takes place.
```python
from easygl.display.window import GLWindow, Multisamples, BlendMode, Projection

window = GLWindow(
    800,                    # width in pixels
    600,                    # height in pixels
    "Game Window",          # the caption for non-fullscreen displays
    Multisamples.quad,      # the multisampling level (none, double, triple or quad)
    BlendMode.alpha,        # the default blend mode
    Projection.custom       # determines the return value of `mouse_position` and `mouse_motion` properties.
)
```

### Texture loading ###

```python
from easygl.textures import TextureData, MipMap, Wrap, Filter

texdata = TextureData()
texdata.load_from_file(
    "the_texture",                      # the texture name in the texdata object
    "path/to/the_texture/image.png",    # the image file to be loaded
    True,                               # whether the texture has alpha channel
    True,                               # whether it should be flipped vertically
    MipMap.none,                        # whether and how to generate mipmaps
    Wrap.repeat,                        # how to wrap the texture in the primitive
    Filter.linear                       # how to filter between mipmap levels
)

# You can easily access the texture settings after creation, if needed:
texdescriptor = texdata['the_texture']

tex_size = texdescriptor.size
tex_id = texdescriptor.id
```

### Shaders ###
```python
from easygl.shaders import ShaderProgramData, ShaderProgram, ShaderCompileError

vsh_code = """#version 330 core

in vec2 position;
in vec2 texcoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec4 blendColor;

out vec2 coord;
out vec4 color;

void main() {

    gl_Position = projection * view * model * vec4(position, 0.0, 1.0);
    coord = texcoord;
    color = blendColor;
}
"""

fsh_code = """#version 330 core

uniform sampler2D tex;

in vec2 coord;
in vec4 color;

void main() {

    gl_FragColor = texture(tex, coord) * color;

}
"""

shaderlib = ShaderProgramData("")
shaderlib.compile_fragment_shader('sprite', shader_code=fsh_code)
shaderlib.compile_vertex_shader('sprite', shader_code=vsh_code)

shaderlib.link('sprite', vertex='sprite', fragment='sprite')

sprite_shader = shaderlib.build('sprite',
                                'model', 'view', 'projection', 'tex', 'blendColor')
```

### VertexArrays ###
```python
from easygl.arrays import VertexArray

texquad = VertexArray(textured_quad, 'texquad', sprite_shader)  # using values from examples above
```

### Vectors and Matrices ###
```python
from easygl.structures import FrozenMat4, Vec4
from easygl.display import ndc

model = FrozenMat4.transform(Vec4(ndc(0., 0.), 0., 1.), 10.0, Vec4(texdata['the_texture'].size, 1., 1.))
view = FrozenMat4.transform(Vec4(0., 0., 0., 1.), 0., Vec4(1., 1., 0., 1.))
projection = FrozenMat4.ortho(0, window.width, 0, window.height, -1, 1)

```

### Game loop, input and rendering ###
Following the examples above, we can now implement the game loop to process input and render the frame:
```python
import pygame as pg
import easygl.display.events as ev

while not window.should_close:
    # the values yield from input() context manager were processed, so position and motion are
    # Vec2 objects, not tuples, delta measures the frame time in milliseconds. By calling
    # window.input() passing `raw` as True, the common PyGame event objects are yield.
    with window.input(raw=False) as (delta, events, keys, position, motion):
        for event in events:
            if isinstance(event, ev.KeyDown):
                # Quit by pressing Alt+F4
                if event.key == pg.K_F4 and event.alt:
                    window.close()

    # Entering the context the screen is cleared and at the exit of the rendering
    # context pg.display.flip() is called. It also yields a delta just like input().
    with window.rendering():

        # here's how texquad is rendered:
        with texquad.render(GL.GL_LINES) as shader:   # type: ShaderProgram
            tex = texdata['karen']   # type: TexDescriptor
            # load_sampler2d() enables to pass more than one texture when needed. The last argument
            # activates the texture unit.
            shader.load_sampler2d('tex', tex.id, 0)
            shader.load_matrix4f('model', 1, False, model)
            shader.load_matrix4f('view', 1, False, view)
            shader.load_matrix4f('projection', 1, False, projection)
            shader.load4f('blendColor', 1., 1., 1., 1.)

```

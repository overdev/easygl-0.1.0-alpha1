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
import pygame.image as image
from pygame import Surface
from collections import namedtuple as nt
from enum import Enum

__all__ = [
    'Filter',
    'MipMap',
    'TexDescriptor',
    'TexSubImageDescriptor',
    'TextureData',
    'Wrap',
]


class MipMap(Enum):
    none = 0
    nearest_nearest = 1
    nearest_linear = 2
    linear_nearest = 3
    linear_linear = 4


class Wrap(Enum):
    repeat = 0
    mirror_repeat = 1
    clamp_to_edge = 2
    clamp_to_border = 3


class Filter(Enum):
    linear = 0
    nearest = 1


SubImage = nt("SubImage", "left top right bottom")


class TexSubImageDescriptor(nt("TexSubImageDescriptor", "tex_descriptor image_count image_size bboxes")):

    @classmethod
    def describe_vertical_strip(cls, texdescriptor, image_number):
        # type: (TexDescriptor) -> TexSubImageDescriptor
        width, height = texdescriptor.size
        subimage_height = height / float(image_number)
        subimage_left = 0
        subimage_right = width - 1
        subimage_top = 0
        subimage_bottom = subimage_height -1
        subimages = []
        size = width, subimage_height
        for _ in range(image_number):
            left, top = texdescriptor.texcoord((subimage_left, subimage_top))
            right, bottom = texdescriptor.texcoord((subimage_right, subimage_bottom))
            subimages.append(SubImage(left, bottom, right, top))
            subimage_top += subimage_height
            subimage_bottom += subimage_height

        return cls(texdescriptor, image_number, size, tuple(subimages))

    @classmethod
    def describe_horizontal_strip(cls, texdescriptor, image_number):
        # type: (TexDescriptor) -> TexSubImageDescriptor
        width, height = texdescriptor.size
        subimage_width = width / float(image_number)
        subimage_left = 0
        subimage_right = subimage_width - 1
        subimage_top = 0
        subimage_bottom = height - 1
        subimages = []
        size = subimage_width, height
        for _ in range(image_number):
            left, top = texdescriptor.texcoord((subimage_left, subimage_top))
            right, bottom = texdescriptor.texcoord((subimage_right, subimage_bottom))
            subimages.append(SubImage(left, bottom, right, top))
            subimage_left += subimage_width
            subimage_right += subimage_width

        return cls(texdescriptor, image_number, size, tuple(subimages))

    @classmethod
    def describe_specific(cls, texdescriptor, image_number, images_per_row, offset, image_spacing, image_size):
        # type: (TexDescriptor, int, int, tuple, tuple, tuple) -> TexSubImageDescriptor
        width, height = texdescriptor.size
        left, top = offset
        right, bottom = left, top

        iw, ih = image_size
        sw, sh = image_spacing
        lines, remain = divmod(image_number, images_per_row)
        if remain != 0:
            lines += 1
        right += (iw * images_per_row) + (sw * (images_per_row - 1))
        bottom += (ih * lines) + (sh * (lines - 1))

        errors = "Error(s) found:"

        ok = True
        if not 0 <= left < right <= width:
            ok = False
            errors += "\n- subimages does not fit horizontaly inside image area."

        if not 0 <= top < bottom <= height:
            ok = False
            errors += "\n- subimages does not fit verticaly inside image area."

        if image_number <= 0 or images_per_row <= 0:
            ok = False
            errors += "\n- number of subimages is lesser than or equal zero."

        if sw < 0 or sh < 0:
            ok = False
            errors += "\n- subimages spacing bellow zero (subimage overlap)."

        if iw < 0 or ih < 0:
            ok = False
            errors += "\n- negative or empty subimages size."

        if not ok:
            raise ValueError(errors)

        x, y = offset
        row = 0
        line = 0
        subimages = []

        subimage_left = x
        subimage_top = y
        subimage_right = subimage_left + iw
        subimage_bottom = subimage_top + ih

        # print("...")
        for index in range(image_number):
            left, top = texdescriptor.texcoord((subimage_left, subimage_top))
            right, bottom = texdescriptor.texcoord((subimage_right, subimage_bottom))
            # print(index, '-', left, top, right, bottom)
            subimages.append(SubImage(left, top, right, bottom))

            subimage_left += iw + sw
            subimage_right = subimage_left + iw
            row += 1
            if row == images_per_row:
                row = 0
                subimage_left = offset[0]
                subimage_right = subimage_left + iw
                subimage_top += ih + sh
                subimage_bottom = subimage_top + ih

        return cls(texdescriptor, image_number, image_size, tuple(subimages))


class TexDescriptor(nt("TexDescriptor", "id width height flip mipmap wrap filter")):

    def uniform(self, shader_id, name, texture_unit=0):
        # type: (int, str, int) -> None
        GL.glActiveTexture(GL.GL_TEXTURE0 + texture_unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)
        GL.glUniform1i(GL.glGetUniformLocation(shader_id, name), texture_unit)

    @property
    def size(self):
        # type: () -> tuple
        return self.width, self.height

    def texcoord(self, pos):
        # type: (tuple) -> tuple
        x, y = pos
        return (x / float(self.width - 1)) % 1.0, (y / float(self.height - 1)) % 1.0


class TextureData(object):

    def __init__(self):
        # type: () -> None
        self._descriptors = {}

    def load_from_file(self, tex_name, file_name, has_alpha, flip_vertically, mipmap, wrap, filtering):
        # type: (str, str, bool, bool, MipMap, Wrap, Filter) -> None
        data = image.load(file_name)   # type: Surface

        width, height = data.get_size()

        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        wrap_value = {
            Wrap.repeat: GL.GL_REPEAT,
            Wrap.mirror_repeat: GL.GL_MIRRORED_REPEAT,
            Wrap.clamp_to_edge: GL.GL_CLAMP_TO_EDGE,
            Wrap.clamp_to_border: GL.GL_CLAMP_TO_BORDER
        }.get(wrap, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_value)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_value)

        # Set the texture magnification filtering
        filter_value = {
            Filter.linear: GL.GL_LINEAR,
            Filter.nearest: GL.GL_NEAREST
        }.get(filtering, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, filter_value)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, filter_value)

        if has_alpha:
            gl_channels = GL.GL_RGBA
            channels = 'RGBA'
            data = data.convert_alpha()
        else:
            gl_channels = GL.GL_RGB
            channels = 'RGB'

        data = image.tostring(data, channels, flip_vertically)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, gl_channels, width, height, 0, gl_channels, GL.GL_UNSIGNED_BYTE, data)

        # Apply the texture mipmaps
        if mipmap is not MipMap.none:
            mipmap_value = {
                MipMap.nearest_nearest: GL.GL_NEAREST_MIPMAP_NEAREST,
                MipMap.nearest_linear: GL.GL_NEAREST_MIPMAP_LINEAR,
                MipMap.linear_nearest: GL.GL_LINEAR_MIPMAP_NEAREST,
                MipMap.linear_linear: GL.GL_LINEAR_MIPMAP_LINEAR
            }.get(mipmap, GL.GL_LINEAR_MIPMAP_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, mipmap_value)
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        self._descriptors[tex_name] = TexDescriptor(texture, width, height, flip_vertically, mipmap, wrap, filtering)

    def capture_from_screen(self, tex_name, left, top, width, height, has_alpha, mipmap, wrap, filtering):
        # type: (str, int, int, int, int, bool, MipMap, Wrap, Filter) -> None
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 4)
        GL.glPixelStorei(GL.GL_PACK_ROW_LENGTH, 0)
        GL.glPixelStorei(GL.GL_PACK_SKIP_ROWS, 0)
        GL.glPixelStorei(GL.GL_PACK_SKIP_PIXELS, 0)

        if has_alpha:
            gl_channels = GL.GL_RGBA
        else:
            gl_channels = GL.GL_RGB
        data = GL.glReadPixels(left, top, width, height, gl_channels, GL.GL_UNSIGNED_BYTE)

        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        wrap_value = {
            Wrap.repeat: GL.GL_REPEAT,
            Wrap.mirror_repeat: GL.GL_MIRRORED_REPEAT,
            Wrap.clamp_to_edge: GL.GL_CLAMP_TO_EDGE,
            Wrap.clamp_to_border: GL.GL_CLAMP_TO_BORDER
        }.get(wrap, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_value)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_value)

        # Set the texture magnification filtering
        filter_value = {
            Filter.linear: GL.GL_LINEAR,
            Filter.nearest: GL.GL_NEAREST
        }.get(filtering, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, filter_value)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, filter_value)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, gl_channels, width, height, 0, gl_channels, GL.GL_UNSIGNED_BYTE, data)

        # Apply the texture mipmaps
        if mipmap is not MipMap.none:
            mipmap_value = {
                MipMap.nearest_nearest: GL.GL_NEAREST_MIPMAP_NEAREST,
                MipMap.nearest_linear: GL.GL_NEAREST_MIPMAP_LINEAR,
                MipMap.linear_nearest: GL.GL_LINEAR_MIPMAP_NEAREST,
                MipMap.linear_linear: GL.GL_LINEAR_MIPMAP_LINEAR
            }.get(mipmap, GL.GL_LINEAR_MIPMAP_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, mipmap_value)
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        self._descriptors[tex_name] = TexDescriptor(texture, width, height, False, mipmap, wrap, filtering)

    def create_from_surface(self, tex_name, surface, has_alpha, flip_vertically, mipmap, wrap, filtering):
        if has_alpha:
            gl_channels = GL.GL_RGBA
            fmt = 'RGBA'
        else:
            gl_channels = GL.GL_RGB
            fmt = 'RGB'

        width, height = surface.get_size()
        data = image.tostring(surface, fmt, flip_vertically)

        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        wrap_value = {
            Wrap.repeat: GL.GL_REPEAT,
            Wrap.mirror_repeat: GL.GL_MIRRORED_REPEAT,
            Wrap.clamp_to_edge: GL.GL_CLAMP_TO_EDGE,
            Wrap.clamp_to_border: GL.GL_CLAMP_TO_BORDER
        }.get(wrap, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_value)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_value)

        # Set the texture magnification filtering
        filter_value = {
            Filter.linear: GL.GL_LINEAR,
            Filter.nearest: GL.GL_NEAREST
        }.get(filtering, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, filter_value)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, filter_value)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, gl_channels, width, height, 0, gl_channels, GL.GL_UNSIGNED_BYTE, data)

        # Apply the texture mipmaps
        if mipmap is not MipMap.none:
            mipmap_value = {
                MipMap.nearest_nearest: GL.GL_NEAREST_MIPMAP_NEAREST,
                MipMap.nearest_linear: GL.GL_NEAREST_MIPMAP_LINEAR,
                MipMap.linear_nearest: GL.GL_LINEAR_MIPMAP_NEAREST,
                MipMap.linear_linear: GL.GL_LINEAR_MIPMAP_LINEAR
            }.get(mipmap, GL.GL_LINEAR_MIPMAP_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, mipmap_value)
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        self._descriptors[tex_name] = TexDescriptor(texture, width, height, False, mipmap, wrap, filtering)

    def __getitem__(self, key):
        # type: (str) -> TexDescriptor
        return self._descriptors.__getitem__(key)

    def __delitem__(self, key):
        # type: (str) -> None
        self._descriptors.__delitem__(key)

    @staticmethod
    def unbind_all():
        # type: () -> None
        for i in range(1, 16):
            GL.glActiveTexture(GL.GL_TEXTURE0 + i)
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glActiveTexture(GL.GL_TEXTURE0)

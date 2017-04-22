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

import datetime as dt
import OpenGL.GL as GL
import pygame as pg
import pygame.locals as co
from enum import Enum
from typing import Union, Optional
from contextlib import contextmanager
from easygl.structures import Vec4, Vec2
from .events import *


__all__ = [
    'BlendMode',
    'DisplayError',
    'GLWindow',
    'Multisamples',
    'Projection',
]


class DisplayError(Exception):
    pass


class Multisamples(Enum):
    none = 0
    double = 1
    triple = 2
    quad = 3


class BlendMode(Enum):
    none = 0
    add = 1
    alpha = 2
    multiply = 3


class Projection(Enum):
    custom = 0
    ortho_up = 1
    ortho_down = 2


class GLWindow(object):

    _current = None    # type: GLWindow

    def __init__(self, width, height, title, multisamples, blendmode, projection, **kwargs):
        # type: (int, int, str, Multisamples, BlendMode, Projection) -> None
        if self.__class__._current is not None:
            raise DisplayError("Display already initialized. Call reset() method to change settings.")

        color = kwargs.get('clear_color', (0., 0., 0., 1.))
        size = width, height
        flags = co.OPENGL

        flags |= co.RESIZABLE if kwargs.get('resizable', False) else 0
        flags |= co.DOUBLEBUF if kwargs.get('doublebuf', False) else 0
        flags |= co.FULLSCREEN if kwargs.get('fullscreen', False) else 0
        flags |= co.HWSURFACE if kwargs.get('hwsurface', False) else 0

        pg.init()
        if multisamples is not Multisamples.none:
            samples = {
                Multisamples.double: 2,
                Multisamples.triple: 3,
                Multisamples.quad: 4
            }.get(multisamples, 2)
            pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, samples)

        surface = pg.display.set_mode(size, flags)
        print(surface)
        width, height = surface.get_size()
        pg.display.set_caption(title, title)

        if multisamples is not Multisamples.none:
            GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_BLEND)
        GL.glClearColor(*color)
        GL.glViewport(0, 0, width, height)

        self._close_request = False
        self._blend_mode = None
        self.blend_mode = blendmode
        self._projection = projection
        self._flip_time = 0
        self._input_time = 0
        self._render_time = 0
        self._delta = 1

    @property
    def projection(self):
        return self._projection

    @property
    def title(self):
        return pg.display.get_caption()

    @title.setter
    def title(self, value):
        pg.display.set_caption(repr(value), repr(value))

    @property
    def should_close(self):
        # type: () -> bool
        return self._close_request

    @property
    def resolution(self):
        # type: () -> tuple
        return pg.display.get_surface().get_size()

    @property
    def width(self):
        # type: () -> int
        return pg.display.get_surface().get_width()

    @property
    def height(self):
        # type: () -> int
        return pg.display.get_surface().get_height()

    @property
    def blend_mode(self):
        # type: () -> BlendMode
        return self._blend_mode

    @blend_mode.setter
    def blend_mode(self, value):
        # type: (BlendMode) -> None
        if value is not self._blend_mode:
            self._blend_mode = value
            if value is BlendMode.none:
                GL.glBlendFunc(GL.GL_ONE, GL.GL_ZERO)

            elif value is BlendMode.add:
                try:
                    GL.glBlendFuncSeparate(GL.GL_SRC_ALPHA, GL.GL_ONE, GL.GL_ONE, GL.GL_ONE)
                except (NameError, Exception):
                    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)

            elif value is BlendMode.alpha:
                try:
                    GL.glBlendFuncSeparate(
                        GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA)
                except (NameError, Exception):
                    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

            elif value is BlendMode.multiply:
                try:
                    GL.glBlendFuncSeparate(GL.GL_ALPHA, GL.GL_ONE, GL.GL_ONE, GL.GL_ONE)
                except (NameError, Exception):
                    GL.glBlendFunc(GL.GL_DST_COLOR, GL.GL_ZERO)

    @property
    def mouse_pos(self):
        # type: () -> Vec2
        x, y = pg.mouse.get_pos()
        if self._projection is Projection.ortho_up:
            y = pg.display.get_surface().get_height() - y
        return Vec2(x, y)

    @property
    def mouse_motion(self):
        # type: () -> Vec2
        x, y = pg.mouse.get_rel()
        if self._projection is Projection.ortho_up:
            y = -y
        return Vec2(x, y)

    @property
    def frame_delta(self):
        # type: () -> int
        return self._delta

    @contextmanager
    def input(self, raw=False):
        # type: () -> None
        time = pg.time.get_ticks()
        delta = time - self._input_time
        self._input_time = time
        if raw:
            yield delta, pg.event.get(), pg.key.get_pressed(), Vec2(*pg.mouse.get_pos()), Vec2(*pg.mouse.get_rel())
        else:
            events = []
            for event in pg.event.get():
                if event.type == co.ACTIVEEVENT:
                    events.append(Focus(event.gain, event.state, pg.time.get_ticks()))

                elif event.type == co.QUIT:
                    now = dt.datetime.now()
                    ms = pg.time.get_ticks()
                    self._close_request = True
                    events.append(CloseWindow(ms, now))

                elif event.type == co.KEYDOWN:
                    ctrl = event.mod & co.KMOD_ALT != 0
                    shift = event.mod & co.KMOD_SHIFT != 0
                    alt = event.mod & co.KMOD_ALT != 0
                    events.append(KeyDown(event.key, event.unicode, event.mod, ctrl, shift, alt))

                elif event.type == co.KEYUP:
                    ctrl = event.mod & co.KMOD_ALT != 0
                    shift = event.mod & co.KMOD_SHIFT != 0
                    alt = event.mod & co.KMOD_ALT != 0
                    events.append(KeyUp(event.key, event.mod, ctrl, shift, alt))

                elif event.type == co.MOUSEMOTION:
                    height = pg.display.get_surface().get_height()
                    x, y = event.pos
                    mx, my = event.rel
                    if self._projection is Projection.ortho_up:
                        y = height - y
                        my = -my
                    lbutton, mbutton, rbutton = event.buttons
                    events.append(MouseMotion(Vec2(x, y), Vec2(mx, my), lbutton, mbutton, rbutton))

                elif event.type == co.MOUSEBUTTONDOWN:
                    height = pg.display.get_surface().get_height()
                    x, y = event.pos
                    if self._projection is Projection.ortho_up:
                        y = height - y
                    if event.button == 1:
                        events.append(LeftButtonDown(Vec2(x, y), x, y))
                    elif event.button == 2:
                        events.append(MiddleButtonDown(Vec2(x, y), x, y))
                    elif event.button == 3:
                        events.append(RightButtonDown(Vec2(x, y), x, y))
                    elif event.button == 4:
                        events.append(MouseWheelUp(Vec2(x, y), x, y))
                    else:
                        events.append(MouseWheelDown(Vec2(x, y), x, y))

                elif event.type == co.MOUSEBUTTONUP:
                    height = pg.display.get_surface().get_height()
                    x, y = event.pos
                    if self._projection is Projection.ortho_up:
                        y = height - y
                    if event.button == 1:
                        events.append(LeftButtonUp(Vec2(x, y), x, y))
                    elif event.button == 2:
                        events.append(MiddleButtonUp(Vec2(x, y), x, y))
                    else:
                        events.append(RightButtonUp(Vec2(x, y), x, y))

                elif event.type == co.VIDEORESIZE:
                    events.append(VideoResize(event.w, event.h, event.size))

                elif event.type == co.VIDEOEXPOSE:
                    now = dt.datetime.now()
                    ms = pg.time.get_ticks()
                    events.append(VideoExpose(ms, now))

                elif event.type == co.JOYAXISMOTION:
                    events.append(JoyAxis(event.joy, event.axis, event.value))

                elif event.type == co.JOYBALLMOTION:
                    events.append(JoyBall(event.joy, event.ball, event.rel))

                elif event.type == co.JOYHATMOTION:
                    events.append(JoyHat(event.joy, event.hat, event.value))

                elif event.type == co.JOYBUTTONDOWN:
                    events.append(JoyButtonDown(event.joy, event.button))

                elif event.type == co.JOYBUTTONUP:
                    events.append(JoyButtonUp(event.joy, event.button))
            keys = pg.key.get_pressed()
            mouse_pos = Vec2(*pg.mouse.get_pos())
            mouse_rel = Vec2(*pg.mouse.get_rel())
            if self._projection is Projection.ortho_up:
                mouse_pos.y = self.height - mouse_pos.y
                mouse_rel.y = -mouse_rel.y
            yield delta, events, keys, mouse_pos, mouse_rel

    @contextmanager
    def rendering(self, clear_color=None):
        # type: (Optional[Union[Vec4, tuple, list]]) -> None
        time = pg.time.get_ticks()
        delta = time - self._render_time
        self._render_time = time

        yield delta

        pg.display.flip()
        time = pg.time.get_ticks()
        self._delta = time - self._flip_time
        self._flip_time = time
        if clear_color is not None:
            GL.glClearColor(*clear_color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    def close(self):
        # type: () -> None
        self._close_request = True

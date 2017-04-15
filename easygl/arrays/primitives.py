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

# import numpy as np


from collections import OrderedDict
from contextlib import contextmanager
from typing import Optional
from .datatypes import *
import struct

__all__ = [
    'attribute',
    'vertex',
    'vertex_copy',
    'VertexArrayData',
]


def attribute(name, dtype):
    # type: (str, DTypeInfo, Optional[int]) -> None
    attributes = VertexArrayData.get()
    if isinstance(attributes, (dict, OrderedDict)):
        if name in attributes:
            raise ValueError("'{}' attribute already defined (as {}).".format(
                name, attributes[name].name
            ))
        if dtype not in DType:
            raise ValueError("'dtype' argument is not a valid DType member value.")

        attributes[name] = dtype


def vertex(**attrs):
    # type: (...) -> bool
    arraystate = VertexArrayData.state()
    if arraystate is not None:
        data = arraystate.data    # type: bytearray
        descriptor = arraystate.descriptor    # type: VertexArrayData
        position = arraystate.vertex_index * descriptor.stride
        if position >= len(data):
            return True
        offset = 0
        if data is not None:
            for attr in descriptor.names:   # type: str
                dtype = descriptor.dtype(attr)   # type: DTypeInfo
                if dtype.size > 1:
                    values = attrs.get(attr, arraystate.lastvalues.get(attr, (0,) * dtype.size))
                    arraystate.lastvalues[attr] = values
                    struct.pack_into(dtype.format, data, position + offset, *values)
                else:
                    value = attrs.get(attr, arraystate.lastvalues.get(attr, 0))
                    arraystate.lastvalues[attr] = value
                    struct.pack_into(dtype.format, data, position + offset, value)
                offset += dtype.byte_size
            arraystate += 1
    return False


def vertex_copy(index):
    # type: (int) -> bool
    arraystate = VertexArrayData.state()
    if arraystate is not None:
        data = arraystate.data  # type: bytearray
        descriptor = arraystate.descriptor  # type: VertexArrayData
        chunk_position = index * descriptor.stride
        position = arraystate.vertex_index * descriptor.stride

        if not (0 <= chunk_position < position):
            raise ValueError("'index' argument must be smaller than current index.")

        if data is not None:
            chunk = data[chunk_position: chunk_position + descriptor.stride]
            data[position: position + descriptor.stride] = chunk
            arraystate += 1
    return False


class VertexArrayData(object):

    _defining = []
    _arraystate = []

    class ArrayState(object):
        __slots__ = 'primitive_name', 'vertex_index', 'descriptor', 'lastvalues'

        def __init__(self, primitive_name, vertex_index, descriptor, defaults):
            # type: (str, int, VertexArrayData, dict) -> None
            self.primitive_name = primitive_name
            self.vertex_index = vertex_index
            self.descriptor = descriptor
            self.lastvalues = defaults

        def __eq__(self, other):
            if isinstance(other, VertexArrayData.ArrayState):
                if self.descriptor is not other.descriptor:
                    return False
                if self.primitive_name != other.primitive_name:
                    return False
                if self.vertex_index != other.vertex_index:
                    return False
                return True
            return False

        def __ne__(self, other):
            return not self.__eq__(other)

        def __iadd__(self, other):
            # type: (int) -> VertexArrayData.ArrayState
            if isinstance(other, int):
                self.vertex_index += other
            return self

        def __int__(self):
            # type: () -> int
            return self.vertex_index

        def __index__(self):
            return self.vertex_index

        @property
        def data(self):
            # type: () -> Optional[bytearray]
            try:
                return self.descriptor[self.primitive_name]
            except (IndexError, KeyError):
                return None

    @classmethod
    def get(cls):
        # type: () -> Optional[OrderedDict]
        if len(cls._defining) > 0:
            return cls._defining[-1]
        return None

    @classmethod
    def state(cls):
        # type: () -> Optional[VertexArrayData.ArrayState]
        if len(cls._arraystate) > 0:
            return cls._arraystate[-1]
        return None

    def __init__(self):
        # type: () -> None
        self._attributes = OrderedDict()
        self._defined = False
        self._data = {}

    def __getitem__(self, key):
        # type: (str) -> bytearray
        return self._data.__getitem__(key)

    def __delitem__(self, key):
        # type: (str) -> None
        self._data.__delitem__(key)

    @property
    def descriptor(self):
        # type: () -> OrderedDict
        return self._attributes.copy()

    @property
    def names(self):
        return tuple(self._attributes.keys())

    def dtype(self, name):
        # type: (str) -> Optional[DTypeInfo]
        return self._attributes.get(name)

    @contextmanager
    def definition(self):
        # type: () -> None
        if self._defined:
            raise TypeError("VertexArrayData object atributes are already defined.")
        self.__class__._defining.append(self._attributes)

        yield

        self.__class__._defining.pop()
        self._defined = True

    @contextmanager
    def new_primitive(self, name, vert_count, **defaults):
        if not self._defined:
            raise TypeError("VertexArrayData object atributes are not defined yet.")
        byte_size = self.stride * vert_count
        self._data[name] = bytearray(byte_size)
        state = self.__class__.ArrayState(name, 0, self, defaults)
        # begin
        self.__class__._arraystate.append(state)
        yield
        # end
        self.__class__._arraystate.pop()
        # NOTE: glBufferData won't accept bytearray, but it'll accept bytes as data (don't know why, though).
        self._data[name] = bytes(self._data[name])

    @property
    def stride(self):
        # type: () -> int
        stride = 0
        if self._defined:
            for name in self._attributes:
                dtype = self._attributes[name]   # type: DTypeInfo
                stride += dtype.byte_size

        return stride

    def offset(self, attr_name):
        # type: (str) -> int
        offset = 0

        if self._defined:
            for name in self._attributes:
                if name == attr_name:
                    break
                dtype = self._attributes[name]   # type: DTypeInfo
                offset += dtype.byte_size

        return offset

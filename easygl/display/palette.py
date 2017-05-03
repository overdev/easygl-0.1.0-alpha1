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

from typing import Union
from easygl.structures import FrozenVec4, Vec4

__all__ = [

]


def mix(a, b, r):
    # type: (Union[Vec4, FrozenVec4], Union[Vec4, FrozenVec4]) -> FrozenVec4
    ar, ag, ab, aa = a
    br, bg, bb, ba = b
    return FrozenVec4(
        ar + (br - ar) * r,
        ag + (bg - ag) * r,
        ab + (bb - ab) * r,
        aa + (ba - aa) * r
    )

def from_hexcolor(hexstr):
    # type: (str) -> FrozenVec4
    x = 1 / 255.
    n = len(hexstr)
    if n == 1:
        r = g = b = x * int(hexstr * hexstr, 16)
        a = 1.
    elif n == 2:
        r = g = b = x * int(hexstr, 16)
        a = 1.
    elif n == 3:
        r, g, b = [x * int(ch + ch, 16) for ch in hexstr]
        a = 1.
    elif n == 4:
        r, g, b, a = [x * int(ch + ch, 16) for ch in hexstr]

    elif n == 6:
        r = x * int(hexstr[0:2], 16)
        g = x * int(hexstr[2:4], 16)
        b = x * int(hexstr[4:6], 16)
        a = 1.

    elif n == 8:
        r = x * int(hexstr[0:2], 16)
        g = x * int(hexstr[2:4], 16)
        b = x * int(hexstr[4:6], 16)
        a = x * int(hexstr[6:8], 16)

    else:
        raise ValueError("'{}' is not a valid hex color value.".format(hexstr))

    return FrozenVec4(r, g, b, a)


ALICEBLUE = from_hexcolor('F0F8FF')
ANTIQUEWHITE = from_hexcolor('FAEDB7')
AQUA = from_hexcolor('0FF')
AQUAMARINE = from_hexcolor('7FFFD4')
AZURE = from_hexcolor('F0FFFF')
BEIGE = from_hexcolor('F5F5DC')
BISQUE = from_hexcolor('FFE4C4')
BLACK = from_hexcolor('000')
BLANCHEALMOND = from_hexcolor('FFEBCD')
BLUE = from_hexcolor('00F')
BLUEVIOLET = from_hexcolor('8A2BE2')
BROWN = from_hexcolor('A52A2A')
BURLYWOOD = from_hexcolor('DEB887')
CADETBLUE = from_hexcolor('5F9EA0')
CHARTREUSE = from_hexcolor('7FFF00')
CHOCOLATE = from_hexcolor('D2691E')
CORAL = from_hexcolor('FF7F50')
CORNFLOWERBLUE = from_hexcolor('6495ED')
CORNSILK = from_hexcolor('FFF8DC')
CRIMSON = from_hexcolor('DC143C')
CYAN = from_hexcolor('0FF')
DARKBLUE = from_hexcolor('00008B')
DARKCYAN = from_hexcolor('008B8B')
DARKGOLDENROD = from_hexcolor('B8860B')
DARKGRAY = from_hexcolor('A9A9A9')
DARKGREY = from_hexcolor('A9A9A9')
DRAKGREEN = from_hexcolor('006400')
DARKKHAKI = from_hexcolor('BDB76B')
DARKMAGENTA = from_hexcolor('8B008B')
DARKOLIVEGREEN = from_hexcolor('556B2F')
DARKORANGE = from_hexcolor('FF8C00')
DARKORCHID = from_hexcolor('9932CC')
DARKRED = from_hexcolor('8B0000')
DARKSALMON = from_hexcolor('E9967A')
DARKSEAGREEN = from_hexcolor('8FBC8F')
DARKSLATEBLUE = from_hexcolor('483D8B')
DARKSLATEGRAY = from_hexcolor('2F4F4F')
DARKSLATEGREY = from_hexcolor('2F4F4F')
DARKTURQUOISE = from_hexcolor('00CED1')
DARKVIOLET = from_hexcolor('9400D3')
DEEPPINK = from_hexcolor('FF1493')
DEEPSKYBLUE = from_hexcolor('00BFFF')
DIMGRAY = from_hexcolor('696969')
DIMGREY = from_hexcolor('696969')
DODGERBLUE = from_hexcolor('1E90FF')
FIREBRICK = from_hexcolor('B22222')
FLORALWHITE = from_hexcolor('FFFAF0')
FORESTGREEN = from_hexcolor('228B22')
FUCHSIA = from_hexcolor('F0F')
GAINSBORO = from_hexcolor('DCDCDC')
GHOSTWHITE = from_hexcolor('F8F8FF')
GOLD = from_hexcolor('FFD700')
GOLDENROD = from_hexcolor('DAA520')
GRAY = from_hexcolor('808080')
GREY = from_hexcolor('808080')
GREEN = from_hexcolor('008000')
GREENYELLOW = from_hexcolor('ADFF2F')
HONEYDEW = from_hexcolor('F0FFF0')
HOTPINK = from_hexcolor('FF69B4')
INDIANRED = from_hexcolor('CD5C5C')
INDIGO = from_hexcolor('4B0082')
IVORY = from_hexcolor('FFFFF0')
KHAKY = from_hexcolor('F0E68C')
LAVENDER = from_hexcolor('E6E6FA')
LAVENDERBLUSH = from_hexcolor('FFF0F5')
LAWNGREEN = from_hexcolor('7CFC00')
LEMONCHIFFON = from_hexcolor('FFFACD')
LIGHTBLUE = from_hexcolor('ADD8E6')
LIGHTCORAL = from_hexcolor('F08080')
LIGHTCYAN = from_hexcolor('E0FFFF')
LIGHTGOLDENRODYELLOW = from_hexcolor('FAFAD2')
LIGHTGRAY = from_hexcolor('D3D3D3')
LIGHTGREY = from_hexcolor('D3D3D3')
LIGHTGREEN = from_hexcolor('90EE90')
LIGHTPINK = from_hexcolor('FFB6C1')
LIGHTSALMON = from_hexcolor('FFA07A')
LIGHTSEAGREEN = from_hexcolor('20B2AA')
LIGHTSKYBLUE = from_hexcolor('87CEFA')
LIGHTSLATEGRAY = from_hexcolor('789')
LIGHTSLATEGREY = from_hexcolor('789')
LIGHTSTEELBLUE = from_hexcolor('B0C4DE')
LIGHTYELLOW = from_hexcolor('FFFFE0')
LIME = from_hexcolor('0F0')
LIMEGREEN = from_hexcolor('32CD32')
LINEN = from_hexcolor('FAF0E6')
MAGENTA = from_hexcolor('0F0')
MARRON = from_hexcolor('800000')
MEDIUMAQUAMARINE = from_hexcolor('66CDAA')
MEDIUMBLUE = from_hexcolor('0000CD')
MEDIUMORCHID = from_hexcolor('BA55D3')
MEDIUMPURPLE = from_hexcolor('9370DB')
MEDIUMSEAGREEN = from_hexcolor('3CB371')
MEDIUMSLATEBLUE = from_hexcolor('7B68EE')
MEDIUMSPRINGGREEN = from_hexcolor('00FA9A')
MEDIUMTURQUOISE = from_hexcolor('48D1CC')
MEDIUMVIOLETRED = from_hexcolor('C71585')
MIDNIGHTBLUE = from_hexcolor('191970')
MINTCREAM = from_hexcolor('F5FFFA')
MISTYROSE = from_hexcolor('FFE4E1')
MOCCASIN = from_hexcolor('FFE4B5')
NAVAJOWHITE = from_hexcolor('FFDEAD')
NAVY = from_hexcolor('000080')
OLDLACE = from_hexcolor('FDF5E6')
OLIVE = from_hexcolor('808000')
OLIVEDRAG = from_hexcolor('6B8E23')
ORANGE = from_hexcolor('FFA500')
ORANGERED = from_hexcolor('FF4500')
ORCHID = from_hexcolor('DA70D6')
PALEGOLDENROD = from_hexcolor('EEE8AA')
PALEGREEN = from_hexcolor('98FB98')
PALETURQUOISE = from_hexcolor('AFEEEE')
PALEVIOLETRED = from_hexcolor('DB7093')
PAPAYAWHIP = from_hexcolor('FFEFD5')
PEACHPUFF = from_hexcolor('FFDAB9')
PERU = from_hexcolor('CD853F')
PINK = from_hexcolor('FFC0CB')
PLUM = from_hexcolor('DDA0DD')
POWDERBLUE = from_hexcolor('B0E0E6')
PURPLE = from_hexcolor('800080')
REBECCAPURPLE = from_hexcolor('639')
RED = from_hexcolor('F00')
ROSYBROWN = from_hexcolor('BC8F8F')
ROYALBLUE = from_hexcolor('4160E1')
SADDLEBROWN = from_hexcolor('8B4513')
SALMON = from_hexcolor('FA8072')
SANDYBROWN = from_hexcolor('F4A460')
SEAGREEN = from_hexcolor('2E8B57')
SEASHELL = from_hexcolor('FFF5EE')
SIENNA = from_hexcolor('A0522D')
SILVER = from_hexcolor('C0C0C0')
SKYBLUE = from_hexcolor('87CEEB')
SLATEGRAY = from_hexcolor('708090')
SLATEGREY = from_hexcolor('708090')
SNOW = from_hexcolor('FFFAFA')
SPRINGGREEN = from_hexcolor('00FF7F')
STEELBLUE = from_hexcolor('4682B4')
TAN = from_hexcolor('D2B48C')
TEAL = from_hexcolor('008080')
THISTLE = from_hexcolor('D8BFD8')
TOMATO = from_hexcolor('FF6347')
TURQUOISE = from_hexcolor('40E0D0')
VIOLET = from_hexcolor('EE82EE')
WHEAT = from_hexcolor('F5DEB3')
WHITE = from_hexcolor('FFF')
WHITESMOKE = from_hexcolor('F5F5F5')
YELLOW = from_hexcolor('FF0')
YELLOWGREEN = from_hexcolor('9ACD32')
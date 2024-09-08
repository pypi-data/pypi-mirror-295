from __future__ import annotations

from pyglet import gl

# Texture min/mag filters
NEAREST = 0x2600
LINEAR = 0x2601
NEAREST_MIPMAP_NEAREST = 0x2700
LINEAR_MIPMAP_NEAREST = 0x2701
NEAREST_MIPMAP_LINEAR = 0x2702
LINEAR_MIPMAP_LINEAR = 0x2703

# Texture wrapping
REPEAT = gl.GL_REPEAT
CLAMP_TO_EDGE = gl.GL_CLAMP_TO_EDGE
CLAMP_TO_BORDER = gl.GL_CLAMP_TO_BORDER
MIRRORED_REPEAT = gl.GL_MIRRORED_REPEAT

# Blend functions
ZERO = 0x0000
ONE = 0x0001
SRC_COLOR = 0x0300
ONE_MINUS_SRC_COLOR = 0x0301
SRC_ALPHA = 0x0302
ONE_MINUS_SRC_ALPHA = 0x0303
DST_ALPHA = 0x0304
ONE_MINUS_DST_ALPHA = 0x0305
DST_COLOR = 0x0306
ONE_MINUS_DST_COLOR = 0x0307

# Blend equations

FUNC_ADD = 0x8006
"""source + destination"""

FUNC_SUBTRACT = 0x800A
"""source - destination"""

FUNC_REVERSE_SUBTRACT = 0x800B
"""destination - source"""

MIN = 0x8007
"""Minimum of source and destination"""

MAX = 0x8008
"""Maximum of source and destination"""

BLEND_DEFAULT = SRC_ALPHA, ONE_MINUS_SRC_ALPHA
BLEND_ADDITIVE = ONE, ONE
BLEND_PREMULTIPLIED_ALPHA = SRC_ALPHA, ONE

# VertexArray: Primitives
POINTS = 0
LINES = 1
LINE_LOOP = 2
LINE_STRIP = 3
TRIANGLES = 4
TRIANGLE_STRIP = 5
TRIANGLE_FAN = 6
LINES_ADJACENCY = 10
LINE_STRIP_ADJACENCY = 11
TRIANGLES_ADJACENCY = 12
TRIANGLE_STRIP_ADJACENCY = 13
PATCHES = 14

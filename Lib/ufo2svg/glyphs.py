from __future__ import absolute_import
from fontTools.misc.py23 import *

from xml.etree.ElementTree import Element
from xml.etree import ElementTree
from .svgPathPen import SVGPathPen
from .tools import valueToString
from .tools import _writeUnicode

from svgpathtools import parse_path

from .simple_path import *

def writeGlyphPath(glyph):
	#
	svgGlyphAttrib = {}
	#_writeGlyphName(glyph, svgGlyphAttrib)
	#_writeHorizAdvX(glyph, svgGlyphAttrib)
	#_writeUnicode(glyph, svgGlyphAttrib)
	#_writeID(glyph, svgGlyphAttrib)
	#
	
	#
	if glyph.box:
		t_x = glyph.box[3]
		t_y = glyph.box[2]
	else:
		t_x = 0
		t_y = 0
	#
	_writeD(glyph, svgGlyphAttrib, t_x, t_y)
	#
	svgGlyph = Element("path", attrib=svgGlyphAttrib )
	#
	return svgGlyph

# def _writeGlyphName(glyph, attrib):

# 	assert glyph.name is not None
# 	attrib["glyph-name"] = glyph.name

def _writeID(glyph, attrib):

	assert glyph.name is not None
	attrib["id"] = '__'.join([str(glyph.name),str(_writeUnicode(glyph)).upper(),str(glyph.width)])

# def _writeHorizAdvX(glyph, attrib):

# 	assert glyph.width >= 0
# 	attrib["horiz-adv-x"] = valueToString(glyph.width)

# maybe a function for the fontex area keeping the point names of elements in the id

def _writeD(glyph, attrib, _x, _y):

	pen = SVGPathPen(glyph.getParent())
	glyph.draw(pen)
	pathCommands = pen.getCommands()
	#
	if pathCommands:
		#
		path = parse_path(pathCommands)
		#
		rev_path = path.d()
		#
		# Coordinates come fliped horizontally, we need to reverse
		flip_path = formatPath(flipPath(parsePath(rev_path), horizontal=True, vertical=False))
		#
		attrib["d"] = flip_path
		#
	else:
		#
		attrib["d"] = "Z"
		#
if __name__ == "__main__":
	import doctest
	doctest.testmod()
#!/usr/bin/env python
""" Convert SVG paths to UFO glyphs.
"""
# Author: Cosimo Lupo, Vivarado
# Email: cosimo@anthrotype.com, support@vivarado.com
# License: Apache Software License 2.0

from __future__ import print_function, absolute_import

__requires__ = ["svg.path", "ufoLib", "FontTools"]

import io
import xml.etree.ElementTree as ET

from svg.path import parse_path, Line, CubicBezier, QuadraticBezier

from fontTools.pens.transformPen import TransformPen

from ufoLib.pointPen import SegmentToPointPen
from ufoLib.glifLib import writeGlyphToString

from .simple_path import *

#from .tools import *

__version__ = "0.1.0"
__all__ = ["svg2glif", "SVGOutline"]

def get_additional_info_from_svg_glyph(svg):
	#
	root = ET.fromstring(svg)
	paths = []
	'''
	for el in root.findall(".//{http://www.w3.org/2000/svg}path[@d]"):
		_id = el.get("id")
		paths.append(_id)
	#

	'''
	dat = root.get("id")

	print("GOT DAT")
	print(dat)
	#if len(paths):
	return dat.split('__')
	#else:
	#	return "NONE"




def svg2glif(svg, name, width=0, height=0, unicodes=None, transform=None,
			 version=1):
	""" Convert an SVG outline to a UFO glyph, and assign the given 'name',
	advance 'width' and 'height' (int), 'unicodes' (list of int) to the
	generated glyph.
	Return the resulting string in GLIF format (default: version 2).
	If 'transform' is provided, apply a transformation matrix before the
	conversion (must be tuple of 6 floats, or a FontTools Transform object).
	"""
		
	add_info = get_additional_info_from_svg_glyph(svg)

	root = ET.fromstring(svg)#.parse(svg_file)
	#
	if 'd' in root[0].attrib:
		#
		path_d = root[0].attrib['d']
		#
		if len(path_d) > 1:
			pass
		#
		path_d = root[0].attrib['d']
		if add_info[1] != "NONE":
			#
			flip_path = formatPath(flipPath(parsePath(path_d), horizontal=True, vertical=False))
			root[0].attrib['d'] = flip_path
			
		svg_string = ET.tostring(root, encoding='utf8', method='xml').decode()
		# print(flip_path)

	glyph = SVGOutline.fromstring(svg_string, transform=transform)
	glyph.name = add_info[0]
	glyph.width = width
	glyph.height = height
	glyph.unicodes = unicodes or []
	#
	#
	glif_string = writeGlyphToString(glyph.name,
							  glyphObject=glyph,
							  drawPointsFunc=glyph.drawPoints,
							  formatVersion=version)
	#
	if add_info[1] == "NONE":
		
		tree = ET.fromstring(glif_string)
		for outline in tree.findall('outline'):
			tree.remove(outline)

		glif_string = ET.tostring(tree, encoding='utf8', method='xml').decode("utf-8")

	xmlstr = glif_string
	#
	return xmlstr

class SVGOutline(object):

	def __init__(self, filename=None, transform=None):
		if filename:
			tree = ET.parse(filename)
			root = tree.getroot()
			self.paths = self.parse_paths(root)
		else:
			self.paths = []
		self.transform = transform

	@classmethod
	def fromstring(cls, data, transform=None):
		self = cls(transform=transform)
		root = ET.fromstring(data)
		self.paths = cls.parse_paths(root)
		return self

	@staticmethod
	def parse_paths(root):
		paths = []
		for el in root.findall(".//{http://www.w3.org/2000/svg}path[@d]"):
			if el.get("d") != "Z":
				path = parse_path(el.get("d"))
				paths.append(path)

		return paths

	def draw(self, pen):
		if self.transform:
			pen = TransformPen(pen, self.transform)
		for path in self.paths:
			current_pos = None
			for s in path:
				if current_pos != s.start:
					if current_pos is not None:
						pen.closePath()
					pen.moveTo((s.start.real, s.start.imag))
				if isinstance(s, Line):
					pen.lineTo((s.end.real, s.end.imag))
				elif isinstance(s, CubicBezier):
					pen.curveTo(
						(s.control1.real, s.control1.imag),
						(s.control2.real, s.control2.imag),
						(s.end.real, s.end.imag))
				elif isinstance(s, QuadraticBezier):
					pen.qCurveTo(
						(s.control.real, s.control.imag),
						(s.end.real, s.end.imag))
				#else:
					# TODO convert Arc segments to bezier?
					#raise NotImplementedError(s)
				current_pos = s.end
			pen.closePath()

	def drawPoints(self, pointPen):
		pen = SegmentToPointPen(pointPen)
		self.draw(pen)

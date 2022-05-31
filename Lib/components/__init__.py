# from __future__ import absolute_import
# from fontTools.misc.py23 import *
# import gzip
# import tempfile
# from xml.etree.ElementTree import ElementTree, Element
#
import os
import sys
from os.path import dirname, join, abspath
#
#
#sys.path.insert(0, abspath(join(dirname("generic"), '..')))
#
from Lib.generic import generic_tools
from Lib.efo import efo_fontinfo
#
from .comp_ufo import run_ufo_glyphs
#
#REMOVE
from pprint import pprint
#
import ufoLib
# from .glyphs import writeMissingGlyph, writeGlyphPath
# from .kerning import writeHKernElements
# from .tools import valueToString
#
#
class COMPS(object):
	#
	read_efo_json_fontinfo = ""
	#
	def __init__(self, _in, _ufo_src, EFO):
		#
		#
		self._in = _in
		self._ufo_src = _ufo_src
		#
		#self._fonts = _fonts
		#
		self.EFO_fontinfo = "fontinfo.json"
		self.EFO_features_dir = "features"
		self.EFO_groups_dir = "groups"
		self.EFO_kerning_dir = "kerning"
		self.EFO_glyphs_dir = "glyphs"
		self.EFO_temp = "temp"
		#
		self.current_font_name = EFO.current_font_file_name
		self.anchor_offsets = EFO.anchor_offsets
		#
		efo_fontinfo.read_efo_json_fontinfo(self)
		#
	#
	def ufos_comp(self):
		#
		comp_class_file = os.path.join(*(self._in,self.EFO_groups_dir,"components.plist"))#input("components class group plist file: ")
		#
		run_ufo_glyphs(self, comp_class_file, self._ufo_src)
		#
		
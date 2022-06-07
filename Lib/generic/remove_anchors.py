#
#!/usr/bin/env python
import os
import json
from json import JSONEncoder
import copy
import re
import xml.etree.cElementTree as ET
#
from collections import OrderedDict
import math
import plistlib
#
from argparse import ArgumentParser
#
from pprint import pprint
#
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../..')))
#
print(abspath(join(dirname(__file__), '../..')))
#
from Lib.efo.efo_fontinfo import read_efo_json_fontinfo
from Lib.efo.efo_fontinfo import get_font_file_array
from Lib.components import comp_tools

from Lib.efo import EFO

from Lib.generic import generic_tools
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
					help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
					help="UFO Fonts to get kerning")
#
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
# 
def get_glif_name(xmlTree, _str):
	#
	for elem in xmlTree.iter():
		#
		if elem.tag == "glyph":
			#
			if elem.attrib.get("name") == _str:
				#
				return elem.attrib.get("glif")+'.glif'
				#
			#
		#
	#
#
def get_glif_width(_in, tree, name, font):
	#
	in_glif_filename = os.path.join(_in,"glyphs",font,get_glif_name(tree, name))
	in_glif_file = ET.parse(in_glif_filename)
	return int(in_glif_file.findall('advance')[0].get('width'))
	#
#
def split_input (inp):
	#
	if "," in inp:
		#
		inp = inp.split(',')
		#
	else:
		#
		inp = [inp]
		#
	#
	return inp
	#
#
def remove_anchor(_in, font, glif_name):
	#
	in_glif_filename = os.path.join(_in,"glyphs",font,glif_name+'.glif')
	in_glif_file = ET.parse(in_glif_filename)
	#
	anchors = in_glif_file.findall('anchor')
	#
	print(anchors)
	#
	if len(anchors) > 0:
		#
		print('\t Anchors Found in: ', glif_name, " Removing, Overwriting")
		#
		for elem in in_glif_file.iter():
			#
			for child in list(elem):
				if child.tag == 'anchor':
					elem.remove(child)
					#
		#
		in_glif_file.write(in_glif_filename, encoding='utf-8', xml_declaration=True)
		#
	else:
		#
		print('\t No Anchors Found in: ', glif_name)
		#
	#
def do_remove_anchors(EFO, orig_fonts):
	#
	read_efo_json_fontinfo(EFO, "Downstream")
	fonts = get_font_file_array(EFO)
	#
	#
	orig_fonts = split_input(orig_fonts)
	#
	source_glyphflib = os.path.join(EFO._in,"glyphlib.xml")
	glyphlib = ET.parse(source_glyphflib)
	#
	for o_f in fonts:
		#
		if o_f in orig_fonts:
			#
			for item in glyphlib.findall("glyph"):
				#
				remove_anchor(EFO._in, o_f, item.get('glif'))
				#
			#
		#
	#
#
faults = False
#
if  args.source is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Source EFO File: -s "/font.efo"\n=')	
	#
if  args.fonts is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Fonts to Remove Anchors: -f "thn,reg,bld"\n=')	
	#
#
if faults == False:
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	do_remove_anchors(EFO, args.fonts)
	#
#

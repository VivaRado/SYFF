'''
Get a few basic letters and distribute the shapes to create all other shared letters in Latin, Greek and Cyrillic

Current state testing on Capital letters

Capital Set

C01 Π ['Π' '03A0' 'Pi']
C02 Ε ['Ε' '0395' 'Epsilon']
C03 Λ ['Λ' '039B' 'Lambda']
C04 Μ ['Μ' '039C' 'Mu']
C05 Ο ['Ο' '039F' 'Omicron']
C06 Β ['Β' '0392' 'Beta']
C07 Л ['Л' '041B' 'Elcyrillic']
C08 J ['J' '004a' 'Jay']
C09 S ['S' '0053' 'Es']
C10 З ['З' '0417' 'Zecyrillic']
C11 Ч ['Ч' '0427' 'Checyrillic']

Assuming there will be a list of commands that take an initial vector shape transform and place it into a UFO structure

likely using simple_path.py

flip_path = formatPath(flipPath(parsePath(rev_path), horizontal=True, vertical=False))

REQ/INIT_UFO: Get an initial UFO
REQ/COMMANDS: Using a list of commands per preset glyph iterate
	prepare glif
	get SVG data from UFO glif
	apply transforms to SVG via formatPath
	convert new SVG into UFO glif
	add into new UFO font

To create recombination we store the result and then point to that result in the subsequent instructions.

'''



#!/usr/bin/env python
import os
import re
import time
import copy
import json
import ast
import pprint
from fontParts.world import *
import numpy as np
import itertools as it
import plistlib
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from svg.path import parse_path
from ufoLib.filenames import userNameToFileName
from ufoLib2.objects import Font, Glyph, Guideline
from types import SimpleNamespace
from fontTools.svgLib import SVGPath
from fontTools.pens.pointPen import SegmentToPointPen
from fontTools.ufoLib.glifLib import writeGlyphToString
from fontTools.ufoLib.glifLib import GlifLibError, readGlyphFromString

import sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath( dirname("ufo2svg")))
sys.path.insert(0, abspath( dirname("generic")))

from Lib.ufo2svg import UFO2SVG
from Lib.ufo2svg.glif2svg import convertUFOToSVGFiles
from Lib.ufo2svg.simple_path import *
from Lib.ufo2svg.svg2glif import *
from Lib.helpers.svgpath2mpl import parse_path as mpl_parse_path
from Lib.ufo2svg.glyphs import writeGlyphPath
from Lib.generic.generic_tools import dotdict

import warnings
from Lib.helpers import warning_format

class Recomb(object):
	def __init__(self):
		
		self.current_font_ufo = "Test/DF_A/"
		self.current_fontex_ufo = "DF_A_001-FONTEX.ufo"
		self.current_font_instance_name = "DF_A_001-Light.ufo"

	def conv(self, _dir):

		self._d = _dir
		self._s = os.path.join(_dir, "Test", "DF_A")
		self._t = os.path.join(_dir, "Test", "temp_d")

		convertUFOToSVGFiles(self, 
			OpenFont(os.path.join(self._s,self.current_font_instance_name)), 
			self.current_font_instance_name, 
			[])

	def t_copy(self, file, nam, uni, _dir, ax=False):
		#
		#print("> COPY",file, nam, ax, userNameToFileName(nam))
		tree, svg_data = parse_svg_path(file)
		svg_data.attrib['id'] = make_id(svg_data.attrib['id'], nam, uni)
		#
		glifnam = userNameToFileName(nam)
		save_svg_file(file,glifnam,tree)
		return self._t+'/'+glifnam

	def t_move(self, file, nam, uni, _dir, ax=False):
		#
		#print(file, nam, ax, userNameToFileName(file))
		tree, svg_data = parse_svg_path(file)
		svg_data.attrib['id'] = make_id(svg_data.attrib['id'], nam, uni)
		path = tree.find('./{*}path')
		# transforming / CHANGING
		#
		pathlist = parsePath(path.attrib['d'])

		if "partial" in ax:
			
			complist = parseCompoundPath(path.attrib['d'])
			inx_part = part_list(tree).index(ax["partial"])
			g_partial = [complist[inx_part]][0]

			t_path = translatePath(
							g_partial,
							x=ax["x"], 
							y=ax["y"]
						)

			pathlist = sum(complist,[])

		else:
			
			t_path = translatePath(
						pathlist,
						x=ax["x"], 
						y=ax["y"]
					)

		path.attrib['d'] = formatPath(
								pathlist
							)
		
		glifnam = userNameToFileName(nam)
		save_svg_file(file,glifnam,tree)
		return self._t+'/'+glifnam

	def t_mirror(self, file, nam, uni, _dir, ax=False):
		#
		#print("> MIRROR",file, nam, ax, userNameToFileName(file))
		tree, svg_data = parse_svg_path(file)
		svg_data.attrib['id'] = make_id(svg_data.attrib['id'], nam, uni)
		path = tree.find('./{*}path')
		_h = ax == "horizontal"
		_v = ax == "vertical"
		svg_string = ET.tostring(svg_data, encoding='utf8', method='xml')
		anchors = get_shape_points(svg_string,nam)
		
		bbox = bounding_box(anchors[0])
		bbox_height = bbox[0][1]
		path.attrib['d'] = formatPath(
								translatePath(
									flipPath(
										parsePath(path.attrib['d']), 
										horizontal=_h, 
										vertical=_v
									),
									x=0,
									y=bbox_height
								)
							)
		# saving / SAME
		glifnam = userNameToFileName(nam)
		save_svg_file(file,glifnam,tree)
		return self._t+'/'+glifnam

	def t_partial(self, file, nam, uni, _dir, ax=False):

		#print("> PARTIAL",file, nam, ax)
		# parsing / SAME
		tree_dest, svg_data_dest = parse_svg_path(file)
		svg_data_dest.attrib['id'] = make_id(svg_data_dest.attrib['id'], nam, uni)
		svg_str_dest = ET.tostring(svg_data_dest, encoding='utf8', method='xml')
		
		part_name_list = part_list(tree_dest)
		nam_part = []
		# Get Regional Fontex for function.
		ufo_curr_inst_dir = os.path.join(self._d, self.current_font_ufo, self.current_font_instance_name)

		#dest_part_path, g_name = self.get_partial(file, ax, nam_part, ufo_curr_inst_dir)

		if "type" not in ax.keys():
			ax["type"] = "partial"

		if "operation" in ax.keys():

			if ax["operation"] == "keep":

				nam_part = [x for x in part_name_list if x not in ax["area"]]

			elif ax["operation"] == "remove":			
				
				nam_part = ax["area"]

			elif ax["operation"] == "copy":

				nam_part = ax["area"]

			elif ax["operation"] == "get":

				nam_part = [ax["area"]]
				
				if ax["rename"] == None:
					part_name_list.append(ax["area"])
				else:

					if ax["rename"] in part_name_list:
						path = tree_dest.find('./{*}path')
						copy_name = self.assign_copy_number( ax["rename"], ax["rename"], path.attrib["id"])

						warnings.warn("Partial Name Taken, Renaming: "+ax["rename"]+" to "+copy_name)

						part_name_list.append(copy_name)
					else:
						part_name_list.append(ax["rename"])

				file = os.path.join(self._t,userNameToFileName(ax["source"]))

			part_path, g_name = self.get_partial(file, ax, nam_part, ufo_curr_inst_dir)

		else:

			nam_part = [ax["area"]]
			part_path, g_name = self.get_partial(file, ax, nam_part, ufo_curr_inst_dir)

		path = tree_dest.find('./{*}path')
		new_list = []

		for x in part_name_list:
			if x not in nam_part and any(m in ax["operation"] for m in ["keep", "remove"]):
				fs = '{type:part,position:%s}' % (x)
				new_list.append(fs)
			elif ax["operation"] == "copy":
				if x in nam_part:

					if len(nam_part) > 1:
						copy_name = nam_part[1]
					else:
						copy_name = self.assign_copy_number(x, nam_part[0],path.attrib["id"])

					fs = '{type:part,position:%s}' % (x)
					fs_c = '{type:part,position:%s}' % (copy_name)
					new_list.append(fs)
					new_list.append(fs_c)
				else:
					fs = '{type:part,position:%s}' % (x)
					new_list.append(fs)
			elif ax["operation"] == "get":

				fs = '{type:part,position:%s}' % (x)

				new_list.append(fs)

		path.attrib["id"] = repr(new_list)

		if ax["operation"] == "get":

			path_dest = tree_dest.find('./{*}path')
			path.attrib['d'] = formatPath( parsePath(path_dest.attrib['d']+part_path.attrib['d']) )
			
		else:

			path.attrib['d'] = formatPath( parsePath(part_path.attrib['d']) )

		# saving / SAME
		glifnam = userNameToFileName(nam)
		save_svg_file(file,glifnam,tree_dest)
		return self._t+'/'+glifnam

	def t_fontex(self, file, nam, uni, _dir, ax=False):
		#
		#print("> FONTEX:",file, nam, ax, userNameToFileName(file))
		# parsing / SAME
		tree, svg_data = parse_svg_path(file)
		svg_data.attrib['id'] = make_id(svg_data.attrib['id'], nam, uni)
		path = tree.find('./{*}path')
		#
		# transforming / CHANGING
		svg_string = ET.tostring(svg_data, encoding='utf8', method='xml')
		anchors = get_shape_points(svg_string,nam)
		#print("CONTOUR POINT COORDINATES")
		ufo_fontex_dir = os.path.join(self.current_font_ufo,self.current_fontex_ufo)
		fontex_anchors = self.get_fontex(file, ax, None, ufo_fontex_dir)
		path.attrib['d'] = formatPath(
								translatePathInArea(
									parsePath(path.attrib['d']), 
									area=fontex_anchors[0], 
									x=ax["x"], 
									y=ax["y"]
								)
							)
			#
		#
		# saving / SAME
		glifnam = userNameToFileName(nam)
		save_svg_file(file,glifnam,tree)
		return self._t+'/'+glifnam

	#
	def assign_copy_number(self, nam, p_name, id_list):
		pos_nn = [parse_fontex(x)["position"].rsplit(".")[0] for x in ast.literal_eval(id_list)]
		#pos_nn = [x.rsplit(".")[0] for x in pos]
		counts = dict((i, pos_nn.count(i)) for i in pos_nn)
		k_name = p_name
		if "." in p_name:
			k_name = p_name.rsplit(".")[0]
		return nam.rsplit(".")[0]+"."+str(counts[k_name]).rsplit(".")[0]
	#
	def get_partial(self, fname, ax, _indexes, ufo_dir):
	
		_a = os.path.join(self._d, ufo_dir)
		glif_names = get_glif_names_plist(_a)
		svg_names = get_svg_names(self._t)
		g_name = fname.split("/")[-1]

		if g_name in glif_names and g_name not in svg_names:

			#print("PARTIAL FOUND AS UFO")
			the_path = manage_compound_from_ufo(_a, g_name, ax, _indexes)

		elif g_name in glif_names and g_name in svg_names:

			#print("PARTIAL FOUND AS SVG", fname, _indexes)
			the_path = manage_compound_from_svg(fname, ax, _indexes)

		else:

			#if g_name in svg_names:
			# Did not find the partial in the glyphs of the UFO will look in the SVGs
			#print("PARTIAL FOUND AS SVG", fname)

			the_path = manage_compound_from_svg(fname, ax, _indexes)


		return the_path, g_name


	def get_fontex(self, fname, ax, _indexes, fins):

		part_path, g_name = self.get_partial(fname, ax, _indexes, fins)
		svg_string = ET.tostring(part_path, encoding='utf8', method='xml')
		anchors = get_shape_points(svg_string,g_name)
		return anchors

	def rcb(self, ins, _dir):
		
		function_declaration = {"H":(),
						"V":(),
						"S":(),
						"R":(),
						"C":(),
						"Copy":(self.t_copy),
						"Translate": (self.t_move),
						"Mirror": (self.t_mirror),
						"Fontex": (self.t_fontex),
						"Partial": (self.t_partial),
						"":(),
						}

		ans = copy.deepcopy(ins)

		for letter,funct in ins.items():
			if len(funct) > 0:
				prevlet = letter
				for fnam,fdet in funct.items():
					fdet_d = dotdict(fdet)
					if "rec" in fdet.keys():
						p = list(ins[fdet["rec"]])[-1]
						prevlet = self._t+'/'+ans[fdet["rec"]][p]["out"][0].split("/")[-1]

					if fdet["fnc"] != "":
						out = function_declaration[fdet["fnc"]](prevlet,fdet_d.nam,fdet_d.uni,_dir,*fdet_d.arg)
						prevlet = out
						ans[letter][fnam]["out"].append(out)


def get_glif_coord(f_g, _type):
	p_arr = []
	for contour in f_g:
		nest = []
		for point in contour.points:
			if _type == 'corner':
				if point.type != 'offcurve':
					nest.append([point.x, point.y])
			else:
				nest.append([point.x, point.y])

		p_arr.append(nest)

	return p_arr

def get_shape_points(svg_string,nam):
	glif = svg2glif(svg_string, nam)
	m_glif = make_glyph(glif,nam)
	anchors = get_glif_coord(m_glif, 'corner')

	return anchors


def make_glyph(_g_dat,_name):
	_let = _name
	f = NewFont()
	g = f.newGlyph(_let)
	pen = g.getPointPen()
	glyph_result = readGlyphFromString(_g_dat, glyphObject=g, pointPen=pen)
	f_g = f[_let]

	return f_g

#################################################

def parse_partials(t):
	path = t.find('./{*}path')
	p_id = path.attrib["id"] if "id" in path.attrib.keys() else None
	p_ids = []
	if p_id != None:
		for pi in ast.literal_eval(p_id):
			p_ids.append( parse_fontex(pi) )
	return p_ids

def part_list(t):

	return [ x["position"] for x in parse_partials(t) ]

def parse_fontex(fx):
	json_data = {}
	pattern = re.compile(r'(\w*):([\w.]*)')
	matches = re.finditer(pattern, fx)

	for match in matches:
		key = match.group(1)
		value = match.group(2)

		if key == "index":
			value = int(value)
		json_data[key] = value
	
	return json_data


def get_glif_names_plist(_a):

	cont_f = open(os.path.join(_a,'glyphs','contents.plist'), 'rb')
	pl = plistlib.load(cont_f)
	cont_f.close()
	glif_names = [x.split(".glif")[0] for x in pl.values()]

	return glif_names

def get_svg_names(_a):

	svg_names = [f.split(".svg")[0] for f in os.listdir(_a) if os.path.isfile(join(_a, f))]

	return svg_names

#################################################

def manage_compound_from_ufo(_a, g_name, ax, _indexes):

	font1 = Font.open(_a)
	fp_font = OpenFont(_a)

	for glyph in font1:

		if userNameToFileName(glyph._name) == g_name:

			_p = []
			_g = fp_font[glyph._name] # RGlyph

			if _indexes == None:
				
				_p = _g[fx_type_area_index(_g, ax["type"], ax["area"])]
			else:

				for x in _indexes:
					try:
						_g.removeContour(_g[partial_name_index(_g, x)])
					except Exception as e:

						warnings.warn("Partial Non Existent")
					
				_p = _g

			the_path = writeGlyphPath(_p)

			return the_path


def manage_compound_from_svg(fname, ax, _indexes):

	tree, svg_data = parse_svg_path(fname)
	p = tree.find('./{*}path')
	prs_p = parsePath(p.attrib['d'])
	action_inx = []
	f_comp = []
	comp = svg_path_to_compound(prs_p)

	if _indexes != None:

		for x in _indexes:
			p_inx = d_name_index(parse_partials(tree), x)
			action_inx.append(p_inx)

		if "operation" in ax:
		
			if any(m in ax["operation"] for m in ["keep", "remove"]):

				for i, c in enumerate(comp):
					if i not in action_inx:
						f_comp.append( formatPath(c) )

			elif ax["operation"] == "copy":

				for i, c in enumerate(comp):
					f_comp.append( formatPath(c) )
					if i in action_inx:
						f_comp.append( formatPath(c) )

			elif ax["operation"] == "get":

				for i, c in enumerate(comp):
					if i in action_inx:
						f_comp.append( formatPath(c) )

		else:
			print(_indexes)
			print(action_inx)
			for i, c in enumerate(comp):
				if i in action_inx:
					f_comp.append( formatPath(c) )


		p.attrib['d'] = formatPath( parsePath(''.join(f_comp)) )

	return p








#################################################

def fx_type_area_index(glyph, _type, _area):
	i = 0
	for x in glyph:
		fx_data = parse_fontex(x.points[0].name)
		if fx_data["type"] == _type and fx_data["position"] == _area:
			break
		i += 1
	return i

def partial_name_index(glyph, _area):
	i = 0
	for x in glyph:
		fx_data = parse_fontex(x.points[0].name)
		if fx_data["position"] == _area:
			break
		i += 1
	return i

def d_name_index(_d, _area):
	i = 0
	for x in _d:
		if x["position"] == _area:
			break
		i += 1
	return i

def make_id(_id, nam, uni):
	#
	return '__'.join([nam,uni,_id.split("__")[2]])
	#

#################################################

ET.register_namespace("","http://www.w3.org/2000/svg")

def svg2glif(svg, name, width=0, height=0, unicodes=None, transform=None,
			 version=2):

	glyph = SimpleNamespace(width=width, height=height, unicodes=unicodes)
	outline = SVGPath.fromstring(svg, transform=transform)

	def drawPoints(pointPen):
		pen = SegmentToPointPen(pointPen)
		outline.draw(pen)

	return writeGlyphToString(name,
							  glyphObject=glyph,
							  drawPointsFunc=drawPoints,
							  formatVersion=version)

'''
def path_to_coord(d):

	_path = mpl_parse_path(d)
	crd_mpl_vrt = _path.__dict__['_vertices'].tolist()
	crd_mpl_cds = _path.__dict__['_codes'].tolist()
	r = [x for _,x in sorted(zip(crd_mpl_cds,crd_mpl_vrt))]

	return [list(x) for x in set(tuple(x) for x in r)]
'''

def parse_svg_path(svg_dir):

	svg_file = os.path.join(svg_dir+'.svg')
	tree = ET.parse(svg_file)
	svg_data = tree.getroot()

	if 'd' in svg_data[0].attrib:
		path_d = svg_data[0].attrib['d']
		if len(path_d) > 1:
			return tree, svg_data
			

def save_svg_file(svg_dir, newname, tree):
	ET.indent(tree)
	new_file = os.path.join("/".join(svg_dir.split("/")[:-1]+[newname]))
	tree.write(new_file+'.svg', xml_declaration=True, encoding='utf-8')


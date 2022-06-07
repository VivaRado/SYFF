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

'''
Prerequisites:
	Have an Upright kerned font with the width of the glyph is exactly as the width of the countours.
	Have a Slanted font with the width of glyph is exactly as the width of the countours.
	Know the slant value in deg
'''
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
					help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
					help="UFO Fonts to get kerning")
parser.add_argument("-t", "--target_fonts", dest="target_fonts", 
					help="UFO Fonts to apply altered kerning")
parser.add_argument("-d", "--deg", dest="deg", 
					help="Slant Degrees")
#
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
# #
# def shear_kerning(height, slant_deg, Ko, L, Ln, R, Rn):
# 	#
# 	xs = math.sin(slant_deg*math.pi/180) * height
# 	xl = xs * 2
# 	d = (L - xs) + Ko
# 	b = xs + d + abs(Ko)
# 	g = xl + d
# 	calc = ((g-b)-(Rn-R)) - ((g-b)-(Ln-L))
# 	# if orig_kern < 0:
# 	# 	#
# 	# 	x= math.sin(slant_deg*math.pi/180) * height
# 	# 	u = ( x + abs(orig_kern) ) / 2
# 	# 	#
# 	# 	calc = int(u - abs(R - Rn) + abs(L - Ln))
# 	# 	#
# 	# 	print("+")
# 	# 	#
# 	# else:
# 	# 	#
# 	# 	print("-") 
# 	# 	#
# 	# 	calc = -int(abs(abs(R - Rn) - abs(L - Ln)))
# 	# 	#
# 	return int(calc)
# 	#
# # (int(args.deg), args.fonts, args.target_fonts)
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
def get_glif_top_point(_in, cap_height, glyph_filename, glif_name, font, instance, transfer_dict, equiv_font):
	#
	in_glif_filename = os.path.join(_in,"glyphs",glyph_filename)
	#
	in_glif_file = ET.parse(in_glif_filename)
	#
	nums = []
	#
	glyph_filename_clean = glyph_filename.split(".glif")[0]
	#
	if font not in transfer_dict[instance]:
		#
		transfer_dict[instance] = {font:{}}
		#
	#
	if instance == "targ":
		#
		orig_idx = transfer_dict["orig"][equiv_font][glyph_filename_clean]["idx"]
		_idx = orig_idx
		#
	#
	for _o in in_glif_file.iter():
		#
		if _o.tag == "glyph":
			#
			in_g_name = _o.get('name')
			#
		#
		if _o.tag == "outline":
			#
			if len(_o.findall('contour')):				
				#
				if instance == "orig":
					# add new
					for _c in _o.findall('contour')[0]:
						#
						nums.append([int(_c.get('x')), int(_c.get('y'))])
						#
					#
				else:
					# get that specific index from orig
					#
					if in_g_name == glif_name:
						#
						idx_point = _o.findall('contour')[0].getchildren()[orig_idx]
						#
						nums.append([int(idx_point.get('x')), int(idx_point.get('y'))])
						#
					#
				#
			else:
				#
				print("\t No Contour Found for: ", in_glif_filename)
				#
			#
		#
	#
	if glyph_filename_clean not in transfer_dict[instance][font]:
		#
		if instance == "orig":
			#
			_min = sorted(nums, key=lambda e: ((cap_height - e[1]), -e[0]))[0] # y closest to capital height and x right most
			_idx = nums.index(_min)
			#
		else:
			#
			_min = nums[0]
			#
		#
		transfer_dict[instance][font][glyph_filename_clean] = {"data": _min, "idx": _idx}
		#
	#
	return transfer_dict
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
def get_transfer_dict(EFO, orig_fonts, targ_fonts, glyphlib):
	#
	transfer_dict = {"orig":{},"targ":{}}
	#
	cap_height = EFO.fontinfo[0]["shared_info"]["capHeight"]
	#
	for weight_name in orig_fonts+targ_fonts:
		#
		for f_k in glyphlib.iter():
			#
			if f_k.tag == "glyph":
				#
				g = f_k.attrib.get("glif")
				#
				if g not in ["_notdef", "space"]:
					#
					glif_filename = f_k.attrib.get("glif")+'.glif'
					glif_name = f_k.attrib.get("name")
					#
					i_n = generic_tools.sanitize_string(EFO.current_font_family_name+' '+weight_name)
					i_n_dir = os.path.join(EFO.current_font_family_directory, i_n+'.ufo')
					#
					equiv_font = None
					#
					if weight_name in orig_fonts:
						#
						instance = "orig"
						#
					elif weight_name in targ_fonts:
						#
						instance = "targ"
						#
						equiv_font = orig_fonts[targ_fonts.index(weight_name)]
						#
					#
					transfer_dict = get_glif_top_point(i_n_dir, cap_height, glif_filename, glif_name, weight_name, instance, transfer_dict, equiv_font) # source_font_L_width
					#
				#
			#
		#
	#
	return transfer_dict
	#
#
def get_new_kerning(Kn, OLw, TLw, ORw, TRw, LOFPt, LTFPt, ROFPt, RTFPt):
	#
	_max_diff = 10
	_offset = 1000
	_sidebearings = 0
	#
	add_Kn = Kn + _offset # add offset ensure positive simplifies the calculation
	#
	LFPt = LTFPt - LOFPt
	RFPt = RTFPt - ROFPt
	#
	TOLw = ( TLw - OLw )
	TORw = ( TRw - ORw )
	#
	FPK = LFPt + add_Kn
	#
	TROLw = TOLw + TORw
	#
	if TOLw < _max_diff and TORw < _max_diff:
		#
		DKn = add_Kn
		#
	else:
		#
		remRFPt = 0
		#
		if TORw < _max_diff and (RTFPt - ROFPt) > _max_diff: # if the right side width is the same in Orig and Targ, but there is movement of FP
			#
			remRFPt = RFPt
			#
		#
		DKn = FPK - TROLw - remRFPt
		#
	#
	return DKn - _offset# remove offset
	#
#
def do_kerning_alterations(EFO, deg, orig_fonts, targ_fonts):
	#
	'''
	open flat kerning for orig_fonts
		get fontinfo capHeight
		flatten all fonts that participate
		
		for each font, for each glyphname in glyphlib not _notdef
			find highest point location for orig and targ fonts
			store to transfer_dict as glif_name : { closest y point to cap height of contour[0] point list as [x,y], index in original contour[0] point list }
		
		for each font in target and dest
	'''
	#
	read_efo_json_fontinfo(EFO, "Downstream")
	fonts = get_font_file_array(EFO)
	#
	#
	orig_fonts = split_input(orig_fonts)
	targ_fonts = split_input(targ_fonts)
	#
	EFO._efo_to_ufos(','.join(orig_fonts+targ_fonts), False, "class")
	#
	for z in orig_fonts+targ_fonts:
		#
		instance_name = generic_tools.sanitize_string(EFO.current_font_family_name+' '+z)
		instance_directory = os.path.join(EFO.current_font_family_directory, instance_name+'.ufo')
		#
		comp_tools.flatten_components(instance_directory)
		#
	#
	source_glyphflib = os.path.join(EFO._in,"glyphlib.xml")
	glyphlib = ET.parse(source_glyphflib)
	#
	t_d = get_transfer_dict(EFO, orig_fonts, targ_fonts, glyphlib)
	#
	for o_f in fonts:
		#
		if o_f in orig_fonts:
			#
			for t_f in fonts:
				#
				if t_f in targ_fonts:
					#
					for t_f in targ_fonts:
						#
						orig_flat_kerning = os.path.join(EFO._in,"kerning","flat",o_f+'.plist')
						s_p_f = plistlib.readPlist(orig_flat_kerning)
						#
						targ_flat_kerning = os.path.join(EFO._in,"kerning","flat",t_f+'.plist')
						t_p_f = plistlib.readPlist(targ_flat_kerning)
						#
						for x in s_p_f:
							#print("glyph",x)
							#print("LOFPt", LOFPt)
							#print("LTFPt", LTFPt)
							#
							for y in s_p_f[x]:
								#
								LOFPt = t_d["orig"][o_f][get_glif_name(glyphlib, x).split(".glif")[0]]["data"][0]# y orig 
								LTFPt = t_d["targ"][t_f][get_glif_name(glyphlib, x).split(".glif")[0]]["data"][0]# y target
								#
								#
								ROFPt = t_d["orig"][o_f][get_glif_name(glyphlib, y).split(".glif")[0]]["data"][0]# y orig 
								RTFPt = t_d["targ"][t_f][get_glif_name(glyphlib, y).split(".glif")[0]]["data"][0]# y target
								#
								#
								Kn = s_p_f[x][y] # orig kerning
								#
								i_n = generic_tools.sanitize_string(EFO.current_font_family_name+' '+o_f)
								i_n_dir = os.path.join(EFO.current_font_family_directory, i_n+'.ufo')
								#
								OLw = get_glif_width(EFO._in, glyphlib, x, o_f) # orig_font_L_width
								TLw = get_glif_width(EFO._in, glyphlib, x, t_f) # targ_font_L_width
								#
								ORw = get_glif_width(EFO._in, glyphlib, y, o_f) # orig_font_R_width
								TRw = get_glif_width(EFO._in, glyphlib, y, t_f) # targ_font_R_width
								#
								DKn = get_new_kerning(Kn, OLw, TLw, ORw, TRw, LOFPt, LTFPt, ROFPt, RTFPt)
								#
								t_p_f[x][y] = DKn
								#
								print("\t","Kn:", Kn, "\tDKn", DKn, "\tPAIR:", x, y)
								#
							#
						#
						plistlib.writePlist(t_p_f, targ_flat_kerning)
						#
						#
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
	print('=\n=> Please Provide the Fonts to Shift Anchor Offsets: -f "thn,reg,bld"\n=')	
	#
#
if  args.target_fonts is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Fonts to apply altered kerning: -t "thn,reg,bld"\n=')	
	#
#
if  args.deg is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Slant Degrees: -d "12"\n=')	
	#
#
if faults == False:
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	do_kerning_alterations(EFO, int(args.deg), args.fonts, args.target_fonts)
	#
#

#
import os
import time
from shutil import copyfile
from distutils.dir_util import copy_tree
#
import ufoLib
#
from Lib.generic import generic_tools
import xml.etree.cElementTree as ET
import lxml.etree as LET
from xml.dom import minidom
#
from bs4 import BeautifulSoup
#
'''
Flattens but punctuation is missaligned.
Intended only for the rendering procedure where the punctuation is ignored and only the number 1 contour is considered.
'''
def flatten_components(ufo_dir, export = True, save_glif = True):
	#
	print('COMP: Flatten UFO Components')
	#
	print(ufo_dir)
	#
	reader = ufoLib.UFOReader(ufo_dir, validate=True)
	#
	if export == True:
		#
		source_dir = os.path.join(ufo_dir,'glyphs')
		target_dir = os.path.join(ufo_dir,'glyphs_flat')
		generic_tools.make_dir(target_dir)
		#
		copy_tree(source_dir, target_dir)
		#
		t_dir = target_dir#/media/root/Malysh1/winshm/advent_repo/Advent/_/exp/advent_pro_fmm/test.ufo/glyphs'
		print('INPUT', ufo_dir)
		print('OUTPUT', t_dir)
	#
		ufoWriter = ufoLib.GlyphSet(t_dir)
	#
	inGlyphSet = reader.getGlyphSet()
	#
	for glyphName in inGlyphSet.keys():
		#
		#print(glyphName, get_name)
		#
		g = inGlyphSet[glyphName]
		#
		text = inGlyphSet.getGLIF(glyphName)
		comp = ufoLib.glifLib._fetchComponentBases(text)
		#
		source_glyph = os.path.join(t_dir,generic_tools.glyphNameToFileName(glyphName)+'.glif')
		#
		g.drawPoints(None) 
		#
		if export:
			#
			ufoWriter.writeGlyph(glyphName, g, g.drawPoints)
		#
		#ufoWriter.writeContents()
		#
		with open(source_glyph, 'r') as rf:
			#
			glif_data = rf.read()
			#
			with open(source_glyph, 'w') as wf:
				#
				target_elem = ET.fromstring(glif_data)
				target_dest = target_elem.find('outline')
				#
				for co in comp:
					#
					comp_source = inGlyphSet.getGLIF(co)
					tree = ET.fromstring(comp_source)
					outl = tree.find('outline')
					#
					for x in outl:
						#
						contour = ET.Element("contour")
						#
						for point in x:
							#
							contour.append(point)
							#
						#
						if len(contour):
							#
							target_dest.append(contour)
							#
						#
					#
				#
				for elem in target_elem.iter():
					#
					#print(elem.tag)
					#
					for child in list(elem):
						if child.tag == 'component':
							elem.remove(child)
						elif child.tag == 'contour':
							#
							for point in list(child):
								#	
								if "move" in str(point.attrib):
									elem.remove(child)
									break
				#
				anchors = target_elem.findall('anchor')
				#
				for anchor in anchors:
					target_elem.remove(anchor)
				#
				xml_str = ET.tostring(target_elem, method='xml').decode().replace("'", '"').replace('</contour><contour>','</contour>\n    <contour>').replace('<contour><point','    <contour>\n      <point')
				new_xml = LET.fromstring(xml_str)
				new_xml_str = LET.tostring(new_xml, encoding='utf8', method="xml", xml_declaration=False, pretty_print=True).decode()
				clean_xml_str = BeautifulSoup(xml_str, "xml").prettify()#minidom.parseString(xml_str).toprettyxml(indent="   ")
				#
				if save_glif == True:
					#
					f = open(source_glyph, "w")
					f.write(clean_xml_str) 
					f.close()
					#
				else:
					#
					f.close()
					#
					#
				#if get_name == glyphName:
					#
					#return clean_xml_str
					#
				#
			#
		#
	#
	if export == True:
		#
		time.sleep(2)
		#
		generic_tools.empty_dir(source_dir)
		#
		generic_tools.rm_dir(source_dir)
		os.rename(target_dir, source_dir)
		#
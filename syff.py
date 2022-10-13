import os
from pathlib import Path
from argparse import ArgumentParser
#import lib.cssutils as cssutils
from Lib.synthetic import parser
from Lib.synthetic import converter

from Lib.synthetic.recombinator import Recomb

from Lib.ufo2svg import svg2glif
#REMOVE
#import pprint
#
args = ArgumentParser()
args.add_argument("-s", "--source", dest="source",
					help="Source SYFF", metavar="FILE")
args.add_argument("-f", "--fonts", dest="fonts", 
					help="Source UFO")
#
args = args.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
faults = False
#
if  args.source is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Source SYFF File: -s "/file.syff"\n=')
	#

# if  args.fonts is None:
# 	#
# 	faults = True
# 	#
# 	print('=\n=> Please Provide Source UFO Files: -s "/UFO Family"\n=')	
# 	#

def svg_to_glif(svg_dir, glif_dir):

	print(svg_dir)

	for file in os.listdir(svg_dir):
		filename = os.fsdecode(file)
		if filename.endswith(".svg"): 
			stem_filename = Path(filename).stem
			print( svg_dir, stem_filename )
			svg_string = open(os.path.join(svg_dir, filename), 'r').read()
			glif_string = svg2glif( svg_string, stem_filename)
			glif_file = open(os.path.join(glif_dir, stem_filename + '.glif'), 'w+')
			glif_file.write(glif_string)

		else:
			pass

#
if faults == False:

	rc = Recomb()

	rc.current_fontex_ufo = "DF_A_001-FONTEX.ufo"
	rc.current_font_instance_name = "DF_A_001-Light.ufo"

	rc._d = dir_path
	rc._s = os.path.join(dir_path, "Test", "DF_A")
	rc._t = os.path.join(dir_path, "Test", "temp_svg_a")
	glif_dir = os.path.join(dir_path, "Test", "temp_glif_a")

	rc.conv()
	syff_file = parser.parseString(Path(args.source).read_text())
	syff_rcb = converter.SYFF_RCB(syff_file)
	print("CONVERTED SYFF TO RCB")
	print(syff_rcb)
	rc.rcb(syff_rcb, dir_path)
	print("SVGs Produced!")

	svg_to_glif(rc._t, glif_dir)


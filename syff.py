#import lib.cssutils as cssutils
from Lib.synthetic import parser
from Lib.synthetic import converter

from argparse import ArgumentParser
from pathlib import Path
import os
#REMOVE
#import pprint

from Lib.recombination.recombinator import Recomb


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

dir_path = os.path.dirname(os.path.realpath(__file__))
#
if faults == False:

	rc = Recomb()

	rc.conv(dir_path)

	syff_file = parser.parseString(Path(args.source).read_text())
	
	syff_rcb = converter.SYFF_RCB(syff_file)
	#
	print("CONVERTED SYFF TO RCB")
	#
	print(syff_rcb)
	#
	rc.rcb(syff_rcb, dir_path)
	#
	print("DONE!")
#


#
#!/usr/bin/env python
import os
import json
from json import JSONEncoder
import copy
import re
#
from collections import OrderedDict
#
from argparse import ArgumentParser
#
from pprint import pprint
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
					help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
					help="UFO Fonts to shift comma separated")
parser.add_argument("-v", "--value", dest="value", 
					help="Shift X value")
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
def do_shift_anchor(anchor_file, x_offset, _fonts):
	#
	with open(anchor_file, 'r') as in_f:
		#
		data = json.load(in_f,object_pairs_hook=OrderedDict)
		#
		data_copy = copy.deepcopy(data)
		#
		for k,v in data.items():
			#
			for x in _fonts:
				#
				if k == x :
					#
					for _k,_v in data[k].items():
						#
						if _k == "component":
							#
							for __k,__v in data[k][_k].items():
								#
								data_copy[k][_k][__k][0] = data_copy[k][_k][__k][0] + x_offset
								#
							#
						#
					#
				#
		#
		in_f.close()
		#
		with open(anchor_file, 'w') as out_f:
			#
			b = json.dumps(data_copy, indent=4)
			#
			output2 = re.sub(r'": \[\s+', '": [', b)
			output3 = re.sub(r',\s+', ', ', output2)
			output4 = re.sub(r'\s+\],', '],\n           ', output3)
			#
			out_f.write(output4)
			#
			out_f.close()
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
if  args.value is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Fonts to Shift Anchor Offsets: -f "thn,reg,bld"\n=')	
	#
#
if faults == False:
	#
	anchor_offsets_json = os.path.join(args.source, "anchors/anchor_offsets.json")
	#
	args.fonts = args.fonts.split(',')
	#
	print('>', anchor_offsets_json)
	#
	do_shift_anchor(anchor_offsets_json, int(args.value), args.fonts)
	#
#

#
import os
#import xml.etree.cElementTree as ET
#import xml.dom.minidom as minidom
import json
#
from Lib.generic import generic_tools
#
def get_anchor_offsets(self):
	#
	print('EFO: Getting Anchor Offsets')
	#
	EFO_anchor_offsets = os.path.join(*(self._in,self.EFO_anchors,'anchor_offsets.json'))
	#
	if os.path.exists(EFO_anchor_offsets):
		#
		with open(EFO_anchor_offsets, 'r') as f:
			#
			self.anchor_offsets = json.load(f)
			#
		#
	else:
		#
		self.anchor_offsets = {}
		#
		print("ERROR: You need an Anchor Offsets file if you want to Componentize")
		#
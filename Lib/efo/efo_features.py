#
import os
import glob
from pathlib import Path
import time
import re
#
from Lib.generic import generic_tools
#
#
'''
order?!
	Languagesystems
	Classes
	feature Kerning
	# until here for now
	feature AlternativeFractions;
	feature ScientificInferiors;
	feature Subscript;
	feature Superscript;
	feature Ordinals;
	feature Denominators;
	feature Numerators;
	feature Fractions;
	feature AlternateAnnotationForms;
	feature OldStyleFigures;
	feature DiscretionaryLigatures;
	feature Ligatures;
	feature Ornaments;
	feature StylisticAlternates;
	feature TerminalForms;
	feature HistoricalLigatures;
	feature HistoricalForms;
'''
#
#features_requested_order = ["language_systems.fea", "classes.fea", "kern_fea", "ligatures.fea"] # and other features
#features_start_end_name = ["Languagesystems", "Classes", "Kerning", "Ligatures"] # and other features / for getting UFO features start line end line split to EFO features
features_requested_order = ["language_systems.fea", "classes.fea", "kern_fea", "ligatures.fea"] # and other features
features_start_end_name = ["Languagesystems", "Classes", "Kerning", "Ligatures"] # and other features / for getting UFO features start line end line split to EFO features
#
flush_space = '                                                                   '
#
def combine_fea(self, _for_var):
	#
	print('EFO: Combining FEA')
	#
	EFO_features_dir = os.path.join(self._in,self.EFO_features_dir)
	#
	all_fea = ''
	#
	features_list_dir = os.listdir(EFO_features_dir)
	#
	#print(features_list_dir)
	sorted_features_list_dir = sorted(features_list_dir, key=lambda x: features_requested_order.index(x), reverse=False)
	#
	x = 0
	#
	for file in sorted_features_list_dir:
		#
		current_FEA_file_dir = os.path.join(self.current_font_instance_directory,"features.fea")
		#
		if file.endswith(".fea"):
			#
			EFO_features_file = os.path.join(EFO_features_dir,file)
			#
			_fea = features_start_end_name[x]
			#
			print('\tFOUND FEATURE: ', _fea)
			#
			with open(EFO_features_file, 'r') as fea_file:
				#
				data = generic_tools.get_between('# '+_fea+' Start;', '# '+_fea+' End;', fea_file.read())
				#
				if data != False:
					#
					if _fea == "Classes":
						#
						if _for_var == True:
							#
							data = re.sub('@','@_',data)
							#
						#
					#
					all_fea = all_fea + '# '+_fea+' Start;\n' + data + '\n# '+_fea+' End;'+'\n\n'
					#
			#
		elif "kern_fea" in file:
			#
			current_EFO_kern_fea = os.path.join( *(EFO_features_dir, 'kern_fea', self.current_font_file_name+'.fea') )
			#
			print('\tFOUND KERN FEA: ', current_EFO_kern_fea)
			#
			with open(current_EFO_kern_fea, 'r') as kern_fea_file:
				#
				data = generic_tools.get_between('# Kerning Start;', '# Kerning End;', kern_fea_file.read())
				#
				if data != False:
					#
					#print(data)
					#
					all_fea = all_fea + '# Kerning Start;\n' + data + '\n# Kerning End;'+'\n\n'
					#
			#
		#
		UFO_fea_file = open(current_FEA_file_dir, "w")
		UFO_fea_file.write(all_fea)
		UFO_fea_file.close()
		#
		x = x + 1
		#
	#
#
def split_fea(self, _from_compress = False):
	#
	print('EFO: Splitting FEA')
	#
	print(">>>>>>", self.current_source_ufo)
	#
	UFO_fea_file = os.path.join(self.current_source_ufo, "features.fea")
	#
	#result_fea = []
	#
	with open(UFO_fea_file, 'r') as f:
		#
		print(UFO_fea_file)
		#
		fea_data = f.read()
		#
		x = 0
		#
		for _fea in features_start_end_name:
			#
			print(">>>", _fea)
			#
			got_between = generic_tools.get_between('# '+_fea+' Start;', '# '+_fea+' End;', fea_data)
			#
			if got_between != False:
				#
				data = '# '+_fea+' Start;\n\n'+got_between+'# '+_fea+' End;\n\n'
				#
				if features_requested_order[x] == "kern_fea":
					#
					if _from_compress:
						self.current_font_file_name = self.current_font_file_name.split('_class')[0]
						if "_krn" in self.current_font_file_name:
							#
							self.current_font_file_name = self.current_font_file_name.replace('_krn', '')
							#
						#
					#
					current_features_file = os.path.join( *(self.current_source_efo_features_dir, features_requested_order[x], self.current_font_file_name+'.fea') )
					#
					print("Current Feature File: ", current_features_file)
					#
				else:
					#
					current_features_file = os.path.join(self.current_source_efo_features_dir, features_requested_order[x])
					#
				#
				print('\r\t'+"Splitting UFO FEA: "+_fea )
				#
				#time.sleep(0.1)
				#
				generic_tools.write_to_file(current_features_file, data)
				#
			x = x + 1
			#
		#
		print('\n')
	#
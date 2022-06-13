#import lib.cssutils as cssutils
from .stylesheets import *
from .prodparser import *
from .css import *
from .tokenize2 import Tokenizer

from .css import *

import re
import ast
import warnings
from Lib.helpers import warning_format

import pprint

def remove_q(_s):

	if any(m in _s for m in ["'", '"']):

		_s = ast.literal_eval(_s)

	return _s

def get_func_attr(_s):

	return _s.split('(')[0].strip(), get_par_attr(_s)

def checkInt(str):
	is_d = False
	is_n = False
	n = 0
	if str[0] in ('-', '+'):
		if str[0] == '-':
			is_n = True
		if str[1:].isdigit():
			is_d = True
			n = float(str)
	else:
		if str.isdigit():
			is_d = True
			n = float(str)
	if is_n:
		n = -abs(n)

	return is_d, n
	
def get_par_attr(_s):
	res_data = re.search("\((.*)\)", _s).group(1)

	if ", " in res_data:
		
		res_list = res_data.split(", ")
		res_data = []

		for x in res_list:
			
			resx = remove_q(x)
			c_dig = checkInt(resx)

			if c_dig[0]:
				resx = c_dig[1]
			res_data.append(resx)
			
	else:

		res_data = remove_q(res_data)

	return res_data

def get_sqr_attr(_s):
	res_data = re.search("\=(.*)\]", _s).group(1)
	res_data = remove_q(res_data).split(",")
	res_data = [x.strip() for x in res_data]
	return res_data

def get_letter_result(_s):

	return _s.split('[')[0].strip()

def get_letter_source(_s):

	res_data = re.search("\[(.*)\=", _s).group(1)

	return res_data

def parse_prop(_p):
	_n = _p[0]
	_v = _p[1]
	_v_p = []

	if "(" in _v:
		_v_p = get_func_attr(_v)

	return _n, _v, _v_p

def manage_form_list(dat):

	_l = []
	if isinstance(dat, list) == False:
		_l = [dat]
	else:
		_l = dat
	return _l

def SYFF_RCB(
		syffData, encoding=None, href=None, media=None, title=None, validate=None
	):

	accepted_props = ["partial", "transform", "out"]

	rules_global = {}

	for rule in syffData.cssRules:
		
		if isinstance(rule, CSSMediaRule):

			m_t = get_par_attr(rule.media.mediaText)

			warnings.warn("Instance Queries are not supported.")

		elif isinstance(rule, CSSStyleRule):

			'''
			<transform()> = translate( <partial-name-string>?, <number>, <number>  )
			<transform()> = mirrorX( <partial-name-string>? )
			<transform()> = mirrorY( <partial-name-string>? )
			<transform()> = fontex( <type-string>, <position-string>, <number>, <number> )
			<partial()> = keep( [<partial-name-string> , <partial-name-string>, ...] )
			<partial()> = remove( [<partial-name-string> , <partial-name-string>, ...] )
			<partial()> = get( <letter-name-string> , <partial-name-string>, <partial-new-name-string> )
			<partial()> = copy( <partial-name-string>, <partial-new-name-string>? )

			'''

			is_init = True


			if "[" in rule.selectorText:
				l_nu = get_sqr_attr(rule.selectorText)
				l_s = get_letter_source(rule.selectorText)

				is_init = False
			
			l_r = get_letter_result(rule.selectorText)
			
			#rules_global[l_r] = {}

			resulting_rules = []
			
			declarations = [
				parse_prop((declaration.name, declaration.value ))
				for declaration in rule.style.getProperties(all=True)
			]
			
			pnlst = [p[0] for p in declarations]
			parsd = []
			
			for p in declarations:
				
				if p[0] not in accepted_props:
					raise ValueError("Not Recognized Property: "+_n)
				else:
					parsd.append([p])
			
			
			if len(declarations) == 0 or (len(declarations) == 1 and "out" in pnlst):
				
				_r_s = {
					"fnc":"",
					"arg":[],
					"out":[],
					"rec":"",
					"nam":"",
					"uni":""
				}

				if is_init == False:
					_r_s["fnc"] = "Copy"
					_r_s["arg"] = []

					_r_s["rec"] = l_s
					_r_s["nam"] = l_nu[0]
					_r_s["uni"] = l_nu[1]
					
				else:
					del _r_s["rec"]
					del _r_s["nam"]
					del _r_s["uni"]
				
				if "out" in pnlst:

					_r_s["out"] = [ast.literal_eval(parsd[ pnlst.index("out") ][0][1])]
					

				resulting_rules.append(_r_s)
				
				
			else:

				for p in declarations:
					
					_r_m = {
						"fnc":"",
						"arg":[],
						"out":[],
						"rec":"",
						"nam":"",
						"uni":""
					}
					
					_r_m["nam"] = l_nu[0]
					_r_m["uni"] = l_nu[1]
					_r_m["rec"] = l_s

					_n = p[0]
					_v = p[1]
					_a = p[2]

					if _n not in accepted_props:
						
						raise ValueError("Not Recognized Property: "+_n)

					else:
						
						if _n == "transform":

							if _a[0] == "translate":
								
								_r_m["fnc"] = "Translate"
								
								if len(_a[1]) == 3 and type(_a[1][0]) == str:
									_r_m["arg"] = [{"x":_a[1][1],"y":_a[1][2],"partial":_a[1][0]}]
								elif len(_a[1]) == 2:
									_r_m["arg"] = [{"x":_a[1][0],"y":_a[1][1]}]
								
							elif any(m == _a[0] for m in ["mirrorx", "mirrory"]):
								
								_r_m["fnc"] = "Mirror"

								if len(_a[1]) > 0:
									warnings.warn("mirrorX and mirrorY are letter only, partial mirroring is not supported.")

								if _a[0] == "mirrorx":
									_r_m["arg"] = ["horizontal"]
								elif _a[0] == "mirrory":
									_r_m["arg"] = ["vertical"]

							elif _a[0] == "fontex":

								_r_m["fnc"] = "Fontex"

								_r_m["arg"] = [{"type":_a[1][0],"area": _a[1][1], "x":_a[1][2], "y":_a[1][3]}]


						elif _n == "partial":

							if any(m == _a[0] for m in ["keep", "remove", "copy"]):

								areas = manage_form_list(_a[1])
								
								_r_m["fnc"] = "Partial"
								_r_m["arg"] = [{"operation":_a[0],"area": areas}]

							elif _a[0] == "get":

								args = manage_form_list(_a[1])
								
								#warnings.warn("partial get is not supported")
								_r_m["fnc"] = "Partial"
								_r_m["arg"] = [{"operation":_a[0],"source":args[0],"area": args[1],"rename":None}]

								if len(args) == 3:

									_r_m["arg"][0]["rename"] = args[2]


						elif _n == "out":
							if len(_v) > 0:
								
								_v = [remove_q (_v)]
								

					resulting_rules.append(_r_m)
			
			rules_global[l_r] = {}

			for i, point in enumerate(resulting_rules):
				
				if i > 0:
					del point["rec"]

				rules_global[l_r][i] = point				

	return rules_global


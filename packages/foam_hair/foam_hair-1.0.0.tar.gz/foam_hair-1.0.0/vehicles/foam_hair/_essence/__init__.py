

'''
	from foam_hair._essence import retrieve_essence
	build_essence ()
'''

'''
	from foam_hair._essence import retrieve_essence
	essence = retrieve_essence ()
'''




'''
	objective:
		[ ] harbor pid for starting and stopping:
				"PID_path": crate ("harbor/the.process_identity_number")
'''


#/
#
from .seek import seek_essence
from .scan import scan_essence
from .merge import merge_essence
#
#
import rich
import pydash
#
#
import pathlib
from os.path import dirname, join, normpath
import sys
import os
#
#\


essence = {}
essence_built = "no"

def build_essence ():
	global essence_built;

	if (essence_built == "yes"):
		return;

	essence_path = seek_essence ({
		"name": "foam_hair_essence.py"
	})
	external_essence = scan_essence (essence_path)
	internal_essence = merge_essence (external_essence, essence_path)

	for key in internal_essence:
		essence [ key ] = internal_essence [key]

	essence_built = "yes"

	return;


#
#	Use this; that way can easily
# 	start using redis or something.
#
def retrieve_essence ():
	build_essence ()
	return essence



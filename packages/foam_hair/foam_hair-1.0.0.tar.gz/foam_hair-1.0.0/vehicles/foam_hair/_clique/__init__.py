

#/
#
import importlib
import os
from os.path import dirname, join, normpath
import sys
import pathlib
from pathlib import Path
#
#
import click
#
#
from foam_hair.adventures.ventures import retrieve_ventures
#
#
#from ventures.clique import ventures_clique
#from foam_hair.mixes._clique import mixes_clique
#
#
from .group import clique as clique_group
#
#\


#mixes_clique = importlib.import_module ("foam_hair.mixes._clique").mixes_clique

def build (essence_path):
	essence = """

essence = {}
	
	"""
	
	with Path (essence_path).open ('w') as FP:
		FP.write (essence)

def clique ():
	@click.group ()
	def group ():
		pass

	
	#
	#
	#	/foam_hair
	#		/[records]
	#		foam_hair_essence.py
	#
	@click.command ("build")
	def command__build ():	
		CWD = os.getcwd ()
		
		essence_path = str (normpath (join (CWD, "foam_hair_essence.py")))
		build (essence_path);
		
		print ("built", essence_path)

	group.add_command (command__build)

	
	try:
		group.add_command (importlib.import_module ("ventures.clique").ventures_clique ({
			"ventures": retrieve_ventures ()
		}))
	except Exception as E:
		print ("venture import exception:", E)
	
	group ()




#

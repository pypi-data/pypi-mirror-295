

'''
	from vaccines.adventures.sanique._controls.on as turn_on_sanique
	turn_on_sanique ()
'''


'''
	sanic /vaccines/venues/stages/vaccines/adventures/sanique/harbor/on.proc.py
'''

#/
#
from ventures.utilities.hike_passive_forks import hike_passive_forks
from foam_hair._essence import retrieve_essence
#
#
from biotech.topics.show.variable import show_variable
#
#
import atexit
import json
import multiprocessing
import subprocess
import time
import os
import shutil
import sys
import time
import pathlib
from os.path import dirname, join, normpath
import sys
#
#\

	

def floating_process (procedure, CWD, env):
	show_variable ("procedure:", procedure)
	process = subprocess.Popen (
		procedure, 
		
		cwd = CWD,
		env = env,
		shell = True
	)
	
	pid = process.pid
	
	show_variable ("sanic pid:", pid)

def turn_on_sanique (packet = {}):
	essence = retrieve_essence ()

	harbor_port = int (packet ["ports"] ["harbor"])
	inspector_port = str (packet ["ports"] ["inspector"])

	def actually_turn_on ():
		harbor_path = str (normpath (join (
			pathlib.Path (__file__).parent.resolve (), 
			".."
		))) 
		
		env_vars = os.environ.copy ()
		env_vars ['PYTHONPATH'] = ":".join (sys.path)
		env_vars ['inspector_port'] = inspector_port
		env_vars ['essence_path'] = essence ["essence_path"]

		
		script = [
			"sanic",
			f'harbor:create',
			f'--port={ harbor_port }',
			f'--host=0.0.0.0',
			'--factory',
			'--fast'
		]
		
		#
		#
		#	Without this, the server might stop when 
		#	SSH connection is disconnected.
		#
		#
		if (essence ["mode"] == "business"):
			script.append ("--no-access-logs")
			script.append (">")
			script.append ('/dev/null')
			script.append ('&')
			

		
		
		hike_passive_forks ({
			"script": " ".join (script),
			"Popen": {
				"cwd": harbor_path,
				"env": env_vars,
				"shell": True
			}
		})



	return actually_turn_on;
	

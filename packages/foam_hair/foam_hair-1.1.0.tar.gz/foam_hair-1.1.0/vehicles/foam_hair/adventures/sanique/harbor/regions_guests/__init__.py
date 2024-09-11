



#/
#
from foam_hair._essence import retrieve_essence
from foam_hair.features.pecuniary.APT_to_Octas import convert_APT_to_Octas
from foam_hair.features.pecuniary.Octas_to_APT import convert_Octas_to_APT
from foam_hair.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
from sanic_limiter import Limiter, get_remote_address
#
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
import threading
import time
from fractions import Fraction
#
#\


turn_on_caching = "no"


def regions_guests (vue_regions_packet):
	essence = retrieve_essence ()
	
	
	##/
	build_path = essence ["sveltnetics"] ["build_path"];
	the_index = build_path + "/index.html"
	the_assets = build_path + "/assets"
	
	front_inventory_paths = generate_inventory_paths (build_path)
	for front_path in front_inventory_paths:
		print ("front_path:", front_path)
		pass;
	##\
	
	
	app = vue_regions_packet ["app"]
	guest_addresses = sanic.Blueprint ("guest", url_prefix = "/")
	app.blueprint (guest_addresses)
	
	@guest_addresses.route ("/")
	async def home (request):
		cookies = request.cookies;
		return await sanic_response.file (the_index)
		
		
		
		
		
		
	@guest_addresses.route ("/<path:path>")
	async def assets_route (request, path):
		the_path = False
		
		try:
			the_path = f"{ path }"
			if (the_path in front_inventory_paths):
				content_type = front_inventory_paths [ the_path ] ["mime"]
				content = front_inventory_paths [ the_path ] ["content"]
				
				headers = {}
				if (turn_on_caching == "yes"):
					headers ["Custom-Header-1"] = "custom"
					headers ["Cache-Control"] ="private, max-age=31536000"
					
					#"Expires": "0"
					
				return sanic_response.raw (
					content, 
					content_type = content_type,
					headers = headers
				)
				
		except Exception as E:
			print ("E:", E)
		
			return sanic_response.json ({
				"note": "An anomaly occurred while processing.",
				"the_path": the_path
			}, status = 600)
			
		return await sanic_response.file (the_index)


	
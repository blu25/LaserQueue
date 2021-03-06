#!/usr/bin/env python

import asyncio
import websockets
import json
import os
import time

import argparse
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-l", "--local", help="Run from localhost", dest="local",
	action="store_const",const=True,default=False)
parser.add_argument("-p", "--port", help="Port to host from", dest="port",
	default=80, type=int)
parser.add_argument("-n", "--regen-host", help="Regenerate host in config", dest="host",
	action="store_const",const=True,default=False)
parser.add_argument("-b", "--queue-backup", help="Backup queue and load from backup on start", dest="backup",
	action="store_const",const=True,default=False)
parser.add_argument("-h", "--help", help="Show help", dest="help",
	action="store_const",const=True,default=False)
parser.add_argument("-r", "--regen-config", help="Regenerate config.json", dest="regen",
	action="store_const",const=True,default=False)
parser.add_argument("-s", "--skip-install", help="Skip package installation", dest="skip",
	action="store_const",const=True,default=False)
parser.add_argument("--install-all", help="Don't ask for confirmation on install", dest="all",
	action="store_const",const=True,default=False)
args = parser.parse_args()
if args.help:
	quit()

config = json.load(open(os.path.join("..", "www", "config.json")))

@asyncio.coroutine
def hello(websocket, path):
	stamp = time.time()
	while stamp-time.time()<config["serverRefreshRate"]/1000:
		if not websocket.open:
			break
		message = yield from websocket.recv()
		temppath = os.path.join(os.path.sep, "tmp")
		try:
			messagedata = json.loads(message)
			if message != None and ("action" in messagedata and messagedata["action"] not in ["null", "auth", "uuddlrlrba"]): print(message)
			if os.path.exists(os.path.join(temppath, "topage.json")): 
				if messagedata:
					if message != None and "action" in messagedata:
						if messagedata["action"] not in ["null", "auth", "uuddlrlrba"]:
							print("saving message")
						messagef = open(os.path.join(temppath, "toscript.json"), "w")
						json.dump(messagedata, messagef)
						messagef.close()

						time.sleep(0.05)

						dataf = open(os.path.join(temppath, "topage.json"))
						data = json.load(dataf)
						dataf.close()
						yield from websocket.send(json.dumps(data))
		except:
			pass
			
		
def main():
	print("Serving WebSockets on "+config['host']+" port "+config["port"]+" ...")
	temppath = os.path.join(os.path.sep, "tmp")
	start_server = websockets.serve(hello, config['host'], config['port'])

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
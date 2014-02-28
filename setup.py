import requests
import sys
import os
import ast
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../lib")
from config import config

lights = {}

idFile = open(os.path.dirname(os.path.realpath(__file__)) + "/id.txt", "r").read()

payload = {'format': 'json', 'module': idFile}
r = json.loads(requests.get("http://" + config.get("general", "confighost") + "/api/v1/device/", params=payload).text)

for object in r['objects']:
	attrib = []
	attrib =  ast.literal_eval(object['attributes'])	
	lights[object['name']] = attrib

target = open (os.path.dirname(os.path.realpath(__file__)) + "/lights.json", 'w')
target.write(json.dumps(lights))
target.close

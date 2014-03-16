#!/usr/bin/python
# SingularityHA
# Copyright (C) 2014 Internet by Design Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import mosquitto
import os
import json
import time
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../../lib")
from config import config

broker = str(config.get("mqtt", "host"))
port = int(config.get("mqtt", "port"))
 
def on_connect(rc):
        print "Connected"

def on_connect(rc):
	if rc == 0:
		#rc 0 successful connect
		print "Actuator test connected to MQTT"
	else:
		raise Exception
 
 
def on_publish(val):
	print "Published ", val
 
def cleanup():
	print "Ending and cleaning up"
	ser.close()
	mqttc.disconnect()
 
mypid = os.getpid()
client_uniq = "arduino_pub_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.connect(broker, port, 60, True)

while mqttc.loop() == 0:
	mqttc.publish("limitlessLED", json.dumps(["DeskLight", "off"]))
	time.sleep(1)
	mqttc.publish("limitlessLED", json.dumps(["DeskLight", "on"]))
	time.sleep(1)
	mqttc.publish("limitlessLED", json.dumps(["DeskLight", "brightness", "5"]))
	time.sleep(1)
	mqttc.publish("limitlessLED", json.dumps(["DeskLight", "brightness", "1"]))
	time.sleep(1)
	mqttc.publish("limitlessLED", json.dumps(["DeskLight", "brightness", "9"]))
	time.sleep(1)
	mqttc.publish("limitlessLED", json.dumps(["DeskLight", "brightness", "3"]))
	time.sleep(1)
	mqttc.publish("limitlessLED", json.dumps(["DeskLight", "off"]))
	break
	pass 

"""
    SingularityHA LimitlessLED Module
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../lib")
import socket
import mosquitto
import json
import time
from config import config
import state
import logging

logger = logging.getLogger(__name__)

""" Import list of lights """
lightJSON = open(os.path.dirname(os.path.realpath(__file__)) + "/lights.json", 'r')
lights = json.loads(lightJSON.read())

broker = str(config.get("mqtt", "host"))
port = int(config.get("mqtt", "port"))

""" Hex commands for the lights """
commands = dict(white_all_on=bytearray([0x35, 0x00, 0x55]),
                white_all_off=bytearray([0x39, 0x00, 0x55]),
                white_1_on=bytearray([0x38, 0x00, 0x55]),
                white_1_off=bytearray([0x3B, 0x00, 0x55]),
                white_2_on=bytearray([0x3D, 0x00, 0x55]),
                white_2_off=bytearray([0x33, 0x00, 0x55]),
                white_3_on=bytearray([0x37, 0x00, 0x55]),
                white_3_oyff=bytearray([0x3A, 0x00, 0x55]),
                white_4_on=bytearray([0x32, 0x00, 0x55]),
                white_4_off=bytearray([0x36, 0x00, 0x55]),
                white_brightnessup=bytearray([0x3C, 0x00, 0x55]),
                white_brightnessdown=bytearray([0x34, 0x00, 0x55]),
                white_all_full=bytearray([0xB5, 0x00, 0x55]),
                white_1_full=bytearray([0xB8, 0x00, 0x55]),
                white_2_full=bytearray([0xBD, 0x00, 0x55]),
                white_3_full=bytearray([0xB7, 0x00, 0x55]),
                white_4_full=bytearray([0xB2, 0x00, 0x55]),
                rgbw_all_on=bytearray([0x41, 0x00, 0x55]),
                rgbw_all_off=bytearray([0x42, 0x00, 0x55]),
                rgbw_disco=bytearray([0x4D, 0x00, 0x00]),
                rgbw_discoslower=bytearray([0x43, 0x00, 0x55]),
                rgbw_discofaster=bytearray([0x44, 0x00, 0x55]),
                rgbw_1_on=bytearray([0x45, 0x00, 0x55]),
                rgbw_1_off=bytearray([0x46, 0x00, 0x55]),
                rgbw_2_on=bytearray([0x47, 0x00, 0x55]),
                rgbw_2_off=bytearray([0x48, 0x00, 0x55]),
                rgbw_3_on=bytearray([0x49, 0x00, 0x55]),
                rgbw_3_off=bytearray([0x4A, 0x00, 0x55]),
                rgbw_4_on=bytearray([0x4B, 0x00, 0x55]),
                rgbw_4_off=bytearray([0x4C, 0x00, 0x55]),
                rgbw_all_white=bytearray([0xC2, 0x00, 0x55]),
                rgbw_1_white=bytearray([0xC5, 0x00, 0x55]),
                rgbw_2_white=bytearray([0xC7, 0x00, 0x55]),
                rgbw_3_white=bytearray([0xC9, 0x00, 0x55]),
                rgbw_4_white=bytearray([0xCB, 0x00, 0x55]),
                rgbw_brightness=bytearray([0x4E, 0x00, 0x55]))

colour_map = dict(violet=0x00,
                  royal_blue=0x10,
                  baby_blue=0x20,
                  aqua=0x30,
                  mint=0x40,
                  seafoam_green=0x50,
                  green=0x60,
                  lime_green=0x70,
                  yellow=0x80,
                  yellow_orange=0x90,
                  orange=0xA0,
                  red=0xB0,
                  pink=0xC0,
                  fusia=0xD0,
                  lilac=0xE0,
                  lavender=0xF0)

brightness_map = {
    '0': 0x02,
    '1': 0x05,
    '2': 0x08,
    '3': 0x0B,
    '4': 0x0E,
    '5': 0x11,
    '6': 0x14,
    '7': 0x17,
    '8': 0x19,
    '9': 0x1A,
    '10': 0x1B
}

""" Send required command to light hub """


def send_command(hub, light, command):
    logger.debug("Sending command " + str(hex(command[1])))
    hubconfig = config.get("limitlessLED", hub).split(":")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command, (hubconfig[0], int(hubconfig[1])))


""" Set brightness for both kinds of lights """
def set_brightness(hub, light, light_type, current_brightness, requested_brightness):
    logger.debug("Changing brightness from " + str(current_brightness) + " to " + str(requested_brightness))
    if current_brightness == requested_brightness:
        logger.info("Already at requested brightness!")
        return False

    if int(requested_brightness) > 10:
        print "going up"
        requested_brightness = 10;

    if int(requested_brightness) < 0:
        requested_brightness = 0;

    logger.debug("Changing brightness from " + str(current_brightness) + " to " + str(requested_brightness))

    group = str(lights[light]['group'])
    type = str(lights[light]['type'])
    logger.debug("Sending on command")
    send_command(hub, light, commands[type + "_" + group + "_on"])
    time.sleep(0.1)

    if light_type == "white":
        logger.debug("white light brightness")
        """ do complicated stuff to set the brightness """
        logger.debug(
            "Changing (converted) brightness from " + str(current_brightness) + " to " + str(requested_brightness))

        steps = int(requested_brightness) - int(current_brightness)

        logger.debug("we have steps: " + str(steps))
        if steps < 0:
            logger.debug("Going down")
            steps *= -1
            """ turn brightness down """
            for x in range(0, int(steps)):
                logger.debug("Step down")
                send_command(hub, light, commands["white_brightnessdown"])
                time.sleep(0.1)
            steps = 0

        if steps > 0:
            logger.debug("Going up")
            """ turn brightness up """
            for x in range(0, int(steps)):
                logger.debug("Step up")
                send_command(hub, light, commands["white_brightnessup"])
                time.sleep(0.1)

    if light_type == "rgbw":
        logger.debug("Sending brightness")
        brightness = brightness_map[requested_brightness]
        command = commands["rgbw_brightness"]
        command[1] = brightness
        send_command(hub, light, command)


def on_connect(rc):
    print "LimitlessD Connected to MQTT"


def on_message(msg):
    inbound = json.loads(msg.payload)
    light = inbound[0]
    func = inbound[1]
    try:
        data = inbound[2]
    except IndexError:
        data = ""

    hub = lights[light]['hub']
    group = str(lights[light]['group'])
    light_type = str(lights[light]['type'])
    try:
        attributes = state.get(light).attributes
        current_status = state.get(light).state
    except:
        attributes = {}
        current_status = ""
        attributes['brightness'] = 0
        if light_type == "white":
            for x in range(0, 10):
                logger.debug("Step down")
                send_command(hub, light, commands["white_brightnessdown"])
        if light_type == "rgbw":
            brightness = brightness_map[0]
            command = commands["rgbw_brightness"]
            command[1] = brightness
            send_command(hub, light, command)

    print light + ' ' + func + ' ' + data

    if func == current_status:
        logger.info("Sorry we are already at status " + str(func) + " for this light")
        return False

    command = ""

    # On or full
    if func == "on" or func == "full":
        print light_type + "_" + group + "_" + func
        command = commands[light_type + "_" + group + "_" + func]
        if func == "on":
            state_data = "on"
        if func == "full":
            state_data = "on"
            attributes['brightness'] = 10

    # Off
    if func == "off":
        send_command(hub, light, commands[light_type + "_" + group + "_on"])
        time.sleep(0.2)
        set_brightness(hub, light, light_type, attributes['brightness'], "0")
        time.sleep(0.2)
        command = commands[light_type + "_" + group + "_off"]
        state_data = "off"
        attributes['brightness'] = 0

    # Brightness
    if func == "brightness":
        set_brightness(hub, light, light_type, attributes['brightness'], data)
        attributes['brightness'] = data
        state_data = "on"

    if command is not "":
        send_command(hub, light, command)

    if attributes:
        state.set("limitlessLED", light, state_data, json.dumps(attributes))
    else:
        state.set("limitlessLED", light, state_data)


def main():
    mqttc = mosquitto.Mosquitto("limitlessD")

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    mqttc.connect(broker, port, 60, False)

    mqttc.subscribe("limitless", 0)

    while mqttc.loop() == 0:
        pass


if __name__ == "__main__":
    main()
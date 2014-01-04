#!/bin/bash
# Singularity
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

if [ -z "$1" ] ; then
    echo "You must enter a parameter: "
    echo "  e.g. $0 172.18.1.3 8899 rgbw_colour [option]"
    exit 1
fi

incmd="$3"
ipaddress="$1"
portnum="$2"
option="$4"

white_allon="\x35\00\x55"
white_alloff="\x39\00\x55"
white_zone1on="\x38\00\x55"
white_zone1off="\x3B\00\x55"
white_zone2on="\x3D\00\x55"
white_zone2off="\x33\00\x55"
white_zone3on="\x37\00\x55"
white_zone3off="\x3A\00\x55"
white_zone4on="\x32\00\x55"
white_zone4off="\x36\00\x55"
white_brightnessup="\x3C\00\x55"
white_brightnessdown="\x34\00\x55"
rgbw_allon="\x41\00\x55"
rgbw_alloff="\x42\00\x55"
rgbw_disco="\x4D\00\00"
rgbw_discoslower="\x43\00\x55"
rgbw_discofaster="\x44\00\x55"
rgbw_zone1on="\x45\00\x55"
rgbw_zone1off="\x46\00\x55"
rgbw_zone2on="\x47\00\x55"
rgbw_zone2off="\x48\00\x55"
rgbw_zone3on="\x49\00\x55"
rgbw_zone3off="\x4A\00\x55"
rgbw_zone4on="\x4B\00\x55"
rgbw_zone4off="\x4C\00\x55"
rgbw_allwhite="\xC2\00\x55"
rgbw_zone1white="\xC5\00\x55"
rgbw_zone2white="\xC7\00\x55"
rgbw_zone3white="\xC9\00\x55"
rgbw_zone4white="\xCB\00\x55"
rgbw_brightness+="\x4E\\x"
rgbw_brightness+="$option"
rgbw_brightness+="\x55"

eval incmd=\$$incmd

#echo $incmd

echo -n -e "$incmd" >/dev/udp/"$ipaddress"/"$portnum"

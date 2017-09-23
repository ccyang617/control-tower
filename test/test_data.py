#!/usr/bin/env python

# This script continously prints test packets to a prompted serial interface. These
# packets have been collected by previous team members from real devices.

import serial
import time

heartbeat = "\x7e\x00\x16\x90\x00\x7d\x33\xa2\x00\x40\xe6\x4b\x5e\x03\xfd\x01\x00\x00\xff\xff\xf0\xfa\x23\x00\x2b\x02\xb2"
apple = "\x7e\x00\x22\x90\x00\x7d\x33\xa2\x00\x40\x9f\x27\xa7\x29\x6c\x01\x01\x00\x65\x00\x80\x6f\x69\x3d\x06\x0f\x71\x7d\x33\x5a\x8a\x01\x00\x76\x01\x22\x00\x6e\x09\xee"
cranberry = "\x7e\x00\x22\x90\x00\x7d\x33\xa2\x00\x41\x25\xe5\x88\x0c\x83\x01\x02\x00\xff\xff\x7c\xf3\x05\x00\xba\x0f\x5c\x08\x05\x00\x20\x73\x3b\x00\xdd\x8b\x01\x00\x7a"
dragonfruit = "\x7e\x00\x24\x90\x00\x13\xa2\x00\x40\xe6\x72\x7e\x30\x18\x01\x03\x00\x00\x00\x30\xc8\x07\x00\x6b\x0d\xf4\x00\x06\x00\x00\x00\xb6\x72\x37\x00\xfe\x8b\x01\x00\xfe"
badPacket = "\x7e\x00\x16\x90\x00\x7d\x33\xa2\x00\x40\xe6\x4b\x5e\x03\xfd\x01\x00\x59\x90\x95\x95\x94\x88\x48\x48\x49\xe2"


# port = raw_input("Please enter your serial port path/name: ")
port = "./ttyV1"

try:
    ser = serial.Serial(port, 9600)
except serial.serialutil.SerialException as e:
    print "Serial Error: ", e
    sys.exit(1)

schemaSend = 0
while(True):
	if schemaSend == 0:
		ser.write(heartbeat)
		schemaSend = 1
	elif schemaSend == 1:
		ser.write(apple)
		schemaSend = 2
	elif schemaSend == 2:
		ser.write(cranberry)
		schemaSend = 3
	elif schemaSend == 3:
		ser.write(dragonfruit)
		schemaSend = 4
	elif schemaSend == 4:
		ser.write(badPacket)
		schemaSend = 0

	print 'Wrote data to serial hopefully'
	time.sleep(2)

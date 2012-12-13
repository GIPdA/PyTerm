#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from serial import Serial


s = Serial('/dev/cu.usbserial-A6008cB6')

#print("Open: ", s.open())

print("Bytes: ", s.write(bytes('test', 'UTF-8')))

print("Read: ", s.read(4))

print("Close: ", s.close())


from portsListener import PortsListener

for port in PortsListener.getPorts():
	print("port: ", port)

#execfile("list_ports.py")
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from serial import Serial
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from portsListener import PortsListener



def main(args):
	
	def portChanged(portName):
		print('Port changed: ', portName)
	
	a = QtGui.QApplication(args)
	
	
	s = Serial('/dev/cu.usbserial-A6008cB6')
	
	#print("Open: ", s.open())
	
	print("Bytes: ", s.write(bytes('test', 'UTF-8')))
	
	print("Read: ", s.read(4))
	
	s.close()
	
	matchedPorts = PortsListener.getPorts()
	
	ports_cb = QtGui.QComboBox()
	ports_cb.currentIndexChanged[str].connect(portChanged)
	
	for port in matchedPorts:
		ports_cb.addItem(port)	# TODO: add QVariant with port data
	
	
	window =  QWidget()
	layout =  QVBoxLayout()
	
	layout.addWidget(ports_cb)
	
	window.setLayout(layout)
	window.show()
	
	
	r = a.exec_()
	return r


if __name__ == "__main__":
	main(sys.argv)
	
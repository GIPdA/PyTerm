#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
#from serial import Serial
import serial
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from portsListener import PortsListener
import threading
import time

verbose = 1

class SerialEvents(threading.Thread):

	def __init__(self, serialObject):
		threading.Thread.__init__(self)

		self._serialObject = serialObject
		
		self._stopevent = threading.Event()

	def stop(self):
		self._stopevent.set()

	def run(self):
		while not self._stopevent.isSet():
			if self._serialObject.inWaiting() > 0:
				print("Receive: ", self._serialObject.read(self._serialObject.inWaiting()))
		
		if verbose:
			print("SerialEvents thread exited")


def main(args):
	
	def portChanged(portName):
		print('Port changed: ', portName)
	
	a = QtGui.QApplication(args)
	
	
	try:
		s = serial.Serial('/dev/cu.usbserial-A6008cB6')
		
		se = SerialEvents(s)
		se.start()
		
		#print("Open: ", s.open())
		
		print("Bytes: ", s.write(bytes('test', 'UTF-8')))
		print("Bytes: ", s.write(bytes('erfhurfgjrfgjhrgf', 'UTF-8')))
		
		time.sleep(5)
		
		#print("Read: ", s.read(4))
	
		se.stop()
		
		#se.join()
		s.close()
		
	except (FileNotFoundError, serial.SerialException):
		print("Error")
	
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
	
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

class SerialEvents(QObject, threading.Thread):
	"""
	SerialEvents provide way to have asyncronous serial events 
	interfaced with Qt slots/signals system.
	"""
	
	## ## ## SIGNALS ## ## ##
	readyRead = QtCore.Signal(int)
	

	def __init__(self, serialObject):
		QObject.__init__(self)
		threading.Thread.__init__(self)
		
		self._serialObject = serialObject
		self._stopEvent = threading.Event()
		
		self._availableBytes = 0
	
	
	""" Read all waiting bytes.
	Function provided for convenience
	"""
	def readAll(self):
		return self._serialObject.read(self._serialObject.inWaiting())
	
	
	""" Stop all serial events """
	@QtCore.Slot()
	def stop(self):
		self._stopEvent.set()
		

	""" Thread loop """
	def run(self):
		
		if verbose:
			print('Entering Serial events loop...')
			
		while not self._stopEvent.isSet():
			# Check if data in buffer
			if self._serialObject.isOpen():
				
				wb = self._serialObject.inWaiting()
				if wb > 0 and wb != self._availableBytes:	# Emit readyRead signal only one time
					#string = self._serialObject.read(self._serialObject.inWaiting())
					
					# Emit signal with number of bytes to read
					self.readyRead.emit(self._serialObject.inWaiting())
					
					if verbose:
						print('Data available (', self._serialObject.inWaiting(), ')')
				
				# Store current number of waiting bytes
				self._availableBytes = self._serialObject.inWaiting()
				
				time.sleep(0.1) # Wait 100ms
				
			else:	# Not open, wait more
				time.sleep(1)	# Wait 1s
		
		if verbose:
			print('SerialEvents thread exited')
		


def main(args):
	
	def quit():
		se.stop()
		s.close()
	
	def portChanged(portName):
		print('Port changed: ', portName)
		
	def tryConnect():
		if not s.isOpen():
			s.port = ports_cb.currentText()
			s.open()
			connect.setText('Connected')
	
	def sendStr():
		s.write(bytes('ABCDEF', 'UTF-8'))
		
	def write():
		textedit.setText(textedit.toPlainText() + se.readAll().decode("utf-8"))
	
	
	a = QtGui.QApplication(args)
	
	matchedPorts = PortsListener.getPorts()
	
	ports_cb = QtGui.QComboBox()
	ports_cb.currentIndexChanged[str].connect(portChanged)
	
	for port in matchedPorts:
		ports_cb.addItem(port)	# TODO: add QVariant with port data
	
	connect = QPushButton("Connect")
	connect.clicked.connect(tryConnect)
	
	send = QPushButton("Send")
	send.clicked.connect(sendStr)
	
	textedit = QTextEdit()
	
	s = serial.Serial()
	
	se = SerialEvents(s)
	se.readyRead.connect(write)
	se.start()
	
	# try:
	# 	s = serial.Serial('/dev/cu.usbserial-A6008cB6')
		
		
		
	# 	#print("Open: ", s.open())
		
	# 	print("Bytes: ", s.write(bytes('test', 'UTF-8')))
	# 	print("Bytes: ", s.write(bytes('erfhurfgjrfgjhrgf', 'UTF-8')))
		
	# 	time.sleep(1)
		
	# 	#print("Read: ", s.read(4))
	
	# 	se.stop()
		
	# 	#se.join()
	# 	s.close()
		
	# except (FileNotFoundError, serial.SerialException):
	# 	print("Error")
	
	
	window =  QWidget()
	layout =  QVBoxLayout()
	
	layout.addWidget(ports_cb)
	layout.addWidget(connect)
	layout.addWidget(send)
	layout.addWidget(textedit)
	
	window.setLayout(layout)
	window.show()
	
	
	r = a.exec_()
	quit()
	return r


if __name__ == "__main__":
	main(sys.argv)
	
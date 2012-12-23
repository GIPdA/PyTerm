#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
#from serial import Serial
import serial
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from portsListener import PortsListener
from serialevents import SerialEvents
from pyterm_exceptions import *
from pluginmanager import PluginManager
import time

verbose = 1



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
		processedText = pm.process(textedit.toPlainText(), se.readAll().decode("utf-8"))
		
		textedit.setText(processedText)
	
	
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
	
	
	pm = PluginManager()
	
	plugins_cb = QComboBox()
	plugins_cb.addItems(list(pm.plugins.keys()))
	
	
	s = serial.Serial()
	
	se = SerialEvents(s)
	se.readyRead.connect(write)
	se.start()
	
	# try:
	# 	s = serial.Serial('/dev/cu.usbserial-A6008cB6')
	# except (FileNotFoundError, serial.SerialException):
	# 	print("Error")
	
	
	window =  QWidget()
	layout =  QVBoxLayout()
	
	layout.addWidget(ports_cb)
	layout.addWidget(connect)
	layout.addWidget(send)
	layout.addWidget(textedit)
	layout.addWidget(plugins_cb)
	
	window.setLayout(layout)
	window.show()
	
	
	r = a.exec_()
	quit()
	return r


if __name__ == "__main__":
	main(sys.argv)
	
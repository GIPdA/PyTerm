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
import re

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
		

class LoadException(Exception):
    def __init__(self,reason):
        self.reason = reason
    
    def __str__(self):
        return self.reason

import modules
class PluginManager():
	
	_pluginNameRe = '^[a-z].+\.py$'	# Plugin must begin with letter
	
	def __init__(self):
		self.plugins = dict()
		self._pluginsNames = []
		self.currentPlugin = None
		
		self.loadPlugins()
	
	def loadPlugins(self):
		files = os.listdir('modules')
		
		test = re.compile(self._pluginNameRe, re.IGNORECASE)
		
		self._pluginsNames = [item for item in files if (test.search(item) and item not in modules.__ignore__)]
		
		if len(self._pluginsNames) == 0:
			raise LoadException('No plugins loaded!')
		
		for _pluginName in self._pluginsNames:
			pluginName = _pluginName[0:-3]
			plugin = __import__ ("modules." + pluginName, fromlist=self._pluginsNames) # Load plugin
			
			plugin_instance = getattr(plugin, pluginName)() # Call constructor
			
			# Check if plugin have right methods (= usable plugin)
			if hasattr(plugin_instance, 'processText'):
				self.plugins[pluginName] = plugin_instance
			else:
				raise RuntimeWarning('Unusable plugin: ', pluginName)
			
		
		if 'default' not in self.plugins:
			raise LoadException('Default plugin not found!')
		else:
			self.currentPlugin = 'default'
	
	def usePlugin(self, pluginName):
		if pluginName in self.plugins.keys():
			self.currentPlugin = pluginName
			return True
		else:
			raise RuntimeWarning('Unable to load plugin ', pluginName, ', back to default plugin.')
		return False
		
	def process(self, alltext, text):
		if self.currentPlugin:
			return self.plugins[self.currentPlugin].processText(alltext, text)
		
		raise RuntimeWarning('No plugin set ! Return default')
		return alltext + text
		


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
	
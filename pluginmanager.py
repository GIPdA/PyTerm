#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from PySide import QtGui, QtCore
from PySide.QtCore import *
#from PySide.QtGui import *
import re



import modules
class PluginManager:
	
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
		

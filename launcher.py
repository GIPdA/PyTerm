#!/usr/bin/env python

import os
import modules
import re



files = os.listdir('modules') 
print(files)                    

test = re.compile('^[a-z].+', re.IGNORECASE)

#ffiles = filter(test.search, files)
	
ffiles = [item for item in files if (test.search(item) and item not in modules.__ignore__)]

for f in ffiles:
	print(f)


for mod_namef in ffiles:
	mod_name = mod_namef[0:-3]
	mod = __import__ ("modules." + mod_name, fromlist=ffiles) # on charge le module
	mod_instance = getattr(mod, mod_name)() # on appelle le constructeur
	mod_instance.processText('aaaa')
	
	if hasattr(mod_instance, 'type'):
		print(mod_instance.type)
	
	# if hasattr(mod_instance, "special"):
	#   mod_instance.special()
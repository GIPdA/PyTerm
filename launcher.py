#!/usr/bin/env python

import modules
for mod_name in modules.__all__:
  mod = __import__ ("modules." + mod_name, fromlist=modules.__all__) # on charge le module
  mod_instance = getattr(mod, mod_name)() # on appelle le constructeur
  mod_instance.run()
  if hasattr(mod_instance, "special"):
    mod_instance.special()
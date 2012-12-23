

class default:
	
	description = 'Default plugin'
	
	def __init__(self):
		pass

	def processText(self, alltext, text):
		#print(alltext, text)
		return alltext + text
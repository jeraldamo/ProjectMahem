def onquit(original_function):
	import threading
	orig_shutdown = threading._shutdown
	def new_shutdown():
		original_function()
		orig_shutdown()
		
	threading._shutdown = new_shutdown

import platform

OS_PLATFORM = platform.system()

def read_file(filepath):

	contents = ""
	fp = None
	try:
		fp = open(filepath, 'r')
		contents = fp.read()
	except FileNotFoundError as e:
		message = "[!] Internal Error: No such file as " + filepath + '.'
		print(message)
	finally:
		fp.close()

	return contents

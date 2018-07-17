import sys
import filehandle
import phlex
import phparser
import phtoken
import phprint

def ph_main(source_path):
	code = filehandle.read_file(source_path)
	if code.isspace() or code == "":
		return
	phlex.init(source_path, code)
	while phlex.token != phtoken.TOKEN_EOF:
		phprint.print_decl(phparser.parse_decl())
		print()

if __name__ == '__main__':
	args = sys.argv
	file_name = args[0]
	if (len(args) <= 1):
		print('For now, there is no working REPL. Please specify an external file.')
		exit(0)
	source_file = args[1]
	ph_main(source_file)

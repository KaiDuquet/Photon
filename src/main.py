import sys
import filehandle
import phlex
import phparser
import token


def ph_main(source_path):
	code = filehandle.read_file(source_path)
	if code.isspace() or code == "":
		return
	phlex.init(source_path, code)
	while phlex.token != token.TOKEN_EOF:
		print(phparser.parse_expr())

if __name__ == '__main__':
	args = sys.argv
	file_name = args[0]
	if (len(args) <= 1):
		print('For now, there is no working REPL. Please specify an external file.')
		exit(0)
	source_file = args[1]
	ph_main(source_file)
from filehandle import OS_PLATFORM
from phtoken import *

filename = None
line = 1
column = 1
source = ""
source_length = 0
lex_pos = 0
cur_char = None
lookahead = None
token = None

escapable_chars = ['n', 'r', 't', 'v', 'f', 'b', 'a', '\\', '\'', '"', '?']


def init(arg_filename, arg_source):
	global filename, source, source_length, cur_char, lookahead, token
	filename = arg_filename
	source = arg_source
	source_length = len(source)
	cur_char = source[0]
	if len(source) != 1:
		lookahead = source[1]
	next_token()


def phlexer_error(msg):
	print("[!] Scanner Error: " + msg)
	print("at line %d ->" % line)
	print('\t' + source.splitlines()[line - 1])
	exit(1)


def next_char():
	global lex_pos, source, cur_char, lookahead, source_length
	lex_pos += 1
	if lex_pos >= source_length:
		cur_char = None
		lookahead = None
	elif lex_pos + 1 >= source_length:
		cur_char = source[lex_pos]
		lookahead = None
	else:
		cur_char = source[lex_pos]
		lookahead = source[lex_pos + 1]



def next_token():
	global filename, line, column, source, source_length, lex_pos, cur_char, lookahead, token
	global escapable_chars
	try:
		if cur_char.isspace():
			while cur_char is not None and cur_char.isspace():
				if cur_char == '\n':
					line += 1
					column = 1
				elif cur_char == '\r':
					line += 1
					column = 1
					next_char()
				next_char()

		if cur_char.isdigit():
			val = 0
			while cur_char is not None and cur_char.isdigit():
				val = val * 10 + int(cur_char)
				next_char()
			if cur_char == '.':
				if not lookahead.isdigit():
					phlexer_error('Invalid float literal %d. , no digit found after period' % val)
				next_char()
				decimal = 0
				place = 0.1
				while cur_char is not None and cur_char.isdigit():
					decimal += int(cur_char) * place
					place /= 10
					next_char()
				val += decimal
			token = Token(TOKEN_INT, val)

		elif cur_char.isalpha() or cur_char == '_':
			val = ""
			while cur_char is not None and cur_char.isalnum() or cur_char == '_':
				val += cur_char
				next_char()
			if val in ph_keywords:
				token = Token(TOKEN_KEYWORD, val)
			else:
				token = Token(TOKEN_NAME, val)

		elif cur_char == '\'':
			char = ''
			next_char()
			if char == '\\':
				if not lookahead in escapable_chars:
					phlexer_error('Invalid escape sequence \\' + lookahead)
				next_char()
				char = '\\' + cur_char
			else:
				char = cur_char
			next_char()
			if cur_char != '\'':
				phlexer_error('Missing closing single-quote after ' + char)
			next_char()
			token = Token(TOKEN_INT, ord(char))

		elif cur_char == '"':
			string = ""
			next_char()
			while cur_char is not None and cur_char != '"':
				if cur_char == '\n' or cur_char == '\r':
					phlexer_error('Missing closing double-quote before newline')
				if cur_char == '\\':
					if not lookahead in escapable_chars:
						phlexer_error('Invalid escape sequence \\' + lookahead)
					next_char()
					string += '\\' + cur_char
				else:
					string += cur_char
				next_char()
			next_char()
			token = Token(TOKEN_STR, string)

###########################################################################################
# UNSURE CODE: CHECK LATER ON HOW TO TOKENIZE SYMBOLS, FOR NOW LEXER WILL SCAN ONE BY ONE #
###########################################################################################
		else:
			symbol = TOKEN_EOF
			if cur_char == '+':
				if lookahead == '+':
					symbol = TOKEN_INC
					next_char()
				elif lookahead == '=':
					symbol = TOKEN_ADD_ASSIGN
					next_char()
				else:
					symbol = TOKEN_ADD
				next_char()
			elif cur_char == '-':
				if lookahead == '-':
					symbol = TOKEN_DEC
					next_char()
				elif lookahead == '=':
					symbol = TOKEN_SUB_ASSIGN
					next_char()
				elif lookahead == '>':
					symbol = TOKEN_ARROW
					next_char()
				else:
					symbol = TOKEN_SUB
				next_char()
			elif cur_char == '*':
				if lookahead == '=':
					symbol = TOKEN_MUL_ASSIGN
					next_char()
				else:
					symbol = TOKEN_MUL
				next_char()
			elif cur_char == '/':
				if lookahead == '=':
					symbol = TOKEN_DIV_ASSIGN
					next_char()
				else:
					symbol = TOKEN_DIV
				next_char()
			elif cur_char == '%':
				if lookahead == '=':
					symbol = TOKEN_MOD_ASSIGN
					next_char()
				else:
					symbol = TOKEN_MOD
				next_char()
			elif cur_char == '=':
				if lookahead == '=':
					symbol = TOKEN_EQ
					next_char()
				else:
					symbol = TOKEN_ASSIGN
				next_char()
			elif cur_char == '<':
				if lookahead == '=':
					symbol = TOKEN_LE
					next_char()
				elif lookahead == '<':
					next_char()
					if lookahead == '=':
						symbol = TOKEN_LSHIFT_ASSIGN
						next_char()
					else:
						symbol = TOKEN_LSHIFT
				else:
					symbol == TOKEN_LT
				next_char()
			elif cur_char == '>':
				if lookahead == '=':
					symbol = TOKEN_GE
					next_char()
				elif lookahead == '>':
					next_char()
					if lookahead == '=':
						symbol = TOKEN_RSHIFT_ASSIGN
						next_char()
					else:
						symbol = TOKEN_RSHIFT
				else:
					symbol == TOKEN_GT
				next_char()
			elif cur_char == '!':
				if lookahead == '=':
					symbol = TOKEN_NE
					next_char()
				else:
					symbol = TOKEN_NOT
				next_char()
			elif cur_char == '&':
				if lookahead == '&':
					symbol = TOKEN_AND_AND
					next_char()
				elif lookahead == '=':
					symbol = TOKEN_AND_ASSIGN
					next_char()
				else:
					symbol = TOKEN_AND
				next_char()
			elif cur_char == '|':
				if lookahead == '|':
					symbol = TOKEN_OR_OR
					next_char()
				elif lookahead == '=':
					symbol = TOKEN_OR_ASSIGN
					next_char()
				else:
					symbol = TOKEN_OR
				next_char()
			elif cur_char == '^':
				if lookahead == '=':
					symbol = TOKEN_XOR_ASSIGN
					next_char()
				else:
					symbol = TOKEN_XOR
				next_char()
			elif cur_char == '~':
				symbol = TOKEN_INV
				next_char()
			elif cur_char == '(':
				symbol = TOKEN_LPAREN
				next_char()
			elif cur_char == ')':
				symbol = TOKEN_RPAREN
				next_char()
			elif cur_char == '[':
				symbol = TOKEN_LBRACK
				next_char()
			elif cur_char == ']':
				symbol = TOKEN_RBRACK
				next_char()
			elif cur_char == '{':
				symbol = TOKEN_LBRACE
				next_char()
			elif cur_char == '}':
				symbol = TOKEN_RBRACE
				next_char()
			elif cur_char == '.':
				if lookahead == '.':
					symbol = TOKEN_RANGE
					next_char()
				else:
					symbol = TOKEN_DOT
				next_char()
			elif cur_char == ',':
				symbol = TOKEN_COMMA
				next_char()
			elif cur_char == ';':
				symbol = TOKEN_SEMICOLON
				next_char()
			elif cur_char == ':':
				if lookahead == '=':
					symbol = TOKEN_COLON_ASSIGN
					next_char()
				else:
					symbol = TOKEN_COLON
				next_char()

			token = Token(symbol, STR_TOKEN_TYPE[symbol])


	except AttributeError as e:
		if e.args[0].split(' ')[0] == "'NoneType'":
			token = Token(TOKEN_EOF, "")
		else:
			raise e

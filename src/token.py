TOKEN_SYM = 0
TOKEN_INT = 1
TOKEN_FLOAT = 2
TOKEN_CHAR = 3
TOKEN_STRING = 4
TOKEN_NAME = 5
TOKEN_KEY_BREAK = 6
TOKEN_KEY_CASE = 7
TOKEN_KEY_CHAR = 8
TOKEN_KEY_CONTINUE = 9
TOKEN_KEY_DEFAULT = 10
TOKEN_KEY_ELSE = 11
TOKEN_KEY_FALSE = 12
TOKEN_KEY_FLOAT = 13
TOKEN_KEY_FOR = 14
TOKEN_KEY_IF = 15
TOKEN_KEY_IMPORT = 16
TOKEN_KEY_INT = 17
TOKEN_KEY_NULL = 18
TOKEN_KEY_STRING = 19
TOKEN_KEY_STRUCT = 20
TOKEN_KEY_SWITCH = 21
TOKEN_KEY_TRUE = 22
TOKEN_KEY_UNION = 23
TOKEN_KEY_VOID = 24
TOKEN_KEY_WHILE = 25
TOKEN_EOF = -1

STR_TOKEN_TYPE = {
	TOKEN_SYM: 'Symbol',
	TOKEN_INT: 'Integer',
	TOKEN_FLOAT: 'Float',
	TOKEN_CHAR: 'Char',
	TOKEN_STRING: 'String',
	TOKEN_NAME: 'Name',
	TOKEN_KEY_BREAK: 'Keyword Break',
	TOKEN_KEY_CASE: 'Keyword Case',
	TOKEN_KEY_CHAR: 'Keyword Char',
	TOKEN_KEY_CONTINUE: 'Keyword Continue',
	TOKEN_KEY_DEFAULT: 'Keyword Default',
	TOKEN_KEY_ELSE: 'Keyword Else',
	TOKEN_KEY_FALSE: 'Keyword False',
	TOKEN_KEY_FLOAT: 'Keyword Float',
	TOKEN_KEY_FOR: 'Keyword For',
	TOKEN_KEY_IF: 'Keyword If',
	TOKEN_KEY_IMPORT: 'Keyword Import',
	TOKEN_KEY_INT: 'Keyword Int',
	TOKEN_KEY_NULL: 'Keyword Null',
	TOKEN_KEY_STRING: 'Keyword String',
	TOKEN_KEY_STRUCT: 'Keyword Struct',
	TOKEN_KEY_SWITCH: 'Keyword Switch',
	TOKEN_KEY_TRUE: 'Keyword True',
	TOKEN_KEY_UNION: 'Keyword Union',
	TOKEN_KEY_VOID: 'Keyword Void',
	TOKEN_KEY_WHILE: 'Keyword While',
	TOKEN_EOF: 'End Of File'
}

ph_reserved = {
	'break': TOKEN_KEY_BREAK,	
	'case': TOKEN_KEY_CASE,
	'char': TOKEN_KEY_CHAR,
	'continue': TOKEN_KEY_CONTINUE,
	'default': TOKEN_KEY_DEFAULT,
	'else': TOKEN_KEY_ELSE,
	'false': TOKEN_KEY_FALSE,
	'float': TOKEN_KEY_FLOAT,
	'for': TOKEN_KEY_FOR,
	'if': TOKEN_KEY_IF,
	'import': TOKEN_KEY_IMPORT,
	'int': TOKEN_KEY_INT,
	'null': TOKEN_KEY_NULL,
	'string': TOKEN_KEY_STRING,
	'struct': TOKEN_KEY_STRUCT,
	'switch': TOKEN_KEY_SWITCH,
	'true': TOKEN_KEY_TRUE,
	'union': TOKEN_KEY_UNION,
	'void': TOKEN_KEY_VOID,
	'while': TOKEN_KEY_WHILE
}


class Token(object):
	"""Represents a single token"""
	def __init__(self, t_type, t_val):
		self.t_type = t_type
		self.val_type = type(t_val)
		self.t_val = t_val

	def __eq__(self, other):
		if isinstance(other, Token):
			return self.t_type == other.t_type and self.val_type == other.val_type and self.t_val == other.t_val
		return self.t_type == other

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		tok_str = STR_TOKEN_TYPE[self.t_type]
		string = "TOK [ " + tok_str + ", " + str(self.t_val) + " ]"
		return string

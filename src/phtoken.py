TOKEN_EOF = -1
TOKEN_COLON = 0
TOKEN_SEMICOLON = 1
TOKEN_DOT = 2
TOKEN_RANGE = 3
TOKEN_COMMA = 4
TOKEN_NOT = 5
TOKEN_DIV = 6
TOKEN_MOD = 7
TOKEN_QUESTION = 8
TOKEN_AND = 9
TOKEN_MUL = 10
TOKEN_LPAREN = 11
TOKEN_RPAREN = 12
TOKEN_LBRACK = 13
TOKEN_RBRACK = 14
TOKEN_LBRACE = 15
TOKEN_RBRACE = 16
TOKEN_ARROW = 17
TOKEN_SUB = 18
TOKEN_ADD = 19
TOKEN_ASSIGN = 20
TOKEN_COLON_ASSIGN = 21
TOKEN_OR = 22
TOKEN_XOR = 23
TOKEN_INV = 24
TOKEN_LT = 25
TOKEN_GT = 26
TOKEN_LE = 27
TOKEN_GE = 28
TOKEN_EQ = 29
TOKEN_NE = 30
TOKEN_AND_AND = 31
TOKEN_OR_OR = 32
TOKEN_LSHIFT = 33
TOKEN_RSHIFT = 34
TOKEN_INC = 35
TOKEN_DEC = 36
TOKEN_ADD_ASSIGN = 37
TOKEN_SUB_ASSIGN = 38
TOKEN_MUL_ASSIGN = 39
TOKEN_DIV_ASSIGN = 40
TOKEN_MOD_ASSIGN = 41
TOKEN_AND_ASSIGN = 42
TOKEN_OR_ASSIGN = 43
TOKEN_XOR_ASSIGN = 44
TOKEN_LSHIFT_ASSIGN = 45
TOKEN_RSHIFT_ASSIGN = 46
TOKEN_INT = 47
TOKEN_FLOAT = 48
TOKEN_STRING = 49
TOKEN_NAME = 50
TOKEN_KEYWORD = 51

STR_TOKEN_TYPE = {
	TOKEN_EOF 			: 'EOF',
	TOKEN_COLON 		: ':',
	TOKEN_SEMICOLON		: ';',
	TOKEN_DOT			: '.',
	TOKEN_RANGE			: '...',
	TOKEN_COMMA			: ',',
	TOKEN_NOT 			: '!',
	TOKEN_DIV 			: '/',
	TOKEN_MOD 			: '%',
	TOKEN_QUESTION 		: '^',
	TOKEN_AND 			: '&',
	TOKEN_MUL 			: '*',
	TOKEN_LPAREN 		: '(',
	TOKEN_RPAREN 		: ')',
	TOKEN_LBRACK 		: '[',
	TOKEN_RBRACK 		: ']',
	TOKEN_LBRACE 		: '{',
	TOKEN_RBRACE		: '}',
	TOKEN_ARROW 		: '->',
	TOKEN_SUB 			: '-',
	TOKEN_ADD 			: '+',
	TOKEN_ASSIGN 		: '=',
	TOKEN_COLON_ASSIGN	: ':=',
	TOKEN_OR 			: '|',
	TOKEN_XOR 			: '^',
	TOKEN_INV 			: '~',
	TOKEN_LT 			: '<',
	TOKEN_GT 			: '>',
	TOKEN_LE 			: '<=',
	TOKEN_GE 			: '>=',
	TOKEN_EQ 			: '==',
	TOKEN_NE 			: '!=',
	TOKEN_AND_AND		: '&&',
	TOKEN_OR_OR			: '||',
	TOKEN_LSHIFT 		: '<<',
	TOKEN_RSHIFT 		: '>>',
	TOKEN_INC			: '++',
	TOKEN_DEC			: '--',
	TOKEN_ADD_ASSIGN	: '+=',
	TOKEN_SUB_ASSIGN	: '-=',
	TOKEN_MUL_ASSIGN	: '*=',
	TOKEN_DIV_ASSIGN	: '/=',
	TOKEN_MOD_ASSIGN	: '%=',
	TOKEN_AND_ASSIGN	: '&=',
	TOKEN_OR_ASSIGN 	: '|=',
	TOKEN_XOR_ASSIGN	: '^=',
	TOKEN_LSHIFT_ASSIGN : '<<=',
	TOKEN_RSHIFT_ASSIGN : '>>=',
	TOKEN_INT 			: 'Integer',
	TOKEN_FLOAT 		: 'Float',
	TOKEN_STRING 		: 'String',
	TOKEN_NAME 			: 'Name',
	TOKEN_KEYWORD 		: 'Keyword',
}

ph_keywords = [
	'if',
	'else',
	'while',
	'for',
	'do',
	'struct',
	'union',
	'typedef',
	'sizeof',
	'break',
	'continue',
	'function',
	'return',
	'switch',
	'case',
	'default',
]


class Token(object):
	"""Represents a single token"""
	def __init__(self, t_type, t_val):
		self.t_type = t_type
		self.t_val = t_val

	def __eq__(self, other):
		if isinstance(other, Token):
			return self.t_type == other.t_type and self.t_val == other.t_val
		return self.t_type == other

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		tok_str = STR_TOKEN_TYPE[self.t_type]
		string = "TOK [ " + tok_str + ", " + str(self.t_val) + " ]"
		return string

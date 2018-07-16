import phlex
from phtoken import *
from phast import *


def syntax_error(msg):
	print('[!] Syntax Error: ' + msg)
	print('at line %d ->' % phlex.line)
	print('\t' + phlex.source.splitlines()[phlex.line - 1])
	exit(1)

def is_token(t_type):
	return phlex.token == t_type


def match_token(t_type):
	if is_token(t_type):
		phlex.next_token()
		return True
	return False

def is_keyword(keyword):
	assert(type(keyword) is str)
	return phlex.token == TOKEN_KEYWORD and phlex.token.t_val == keyword

def match_keyword(keyword):
	assert(type(keyword) is str)
	if phlex.token == TOKEN_KEYWORD and phlex.token.t_val == keyword:
		phlex.next_token()
		return True
	return False

def expect_token(t_type):
	if not match_token(t_type):
		syntax_error('Expected token \'%s\', got %s' % (STR_TOKEN_TYPE[t_type], str(phlex.token)))

##############################################################################
# LEFT OFF AT: Finished Declaration parsing, start statements, exprs and types
##############################################################################

def parse_name():
	name = phlex.token.t_val
	expect_token(TOKEN_NAME)
	return name

def parse_var_decl():
	name = parse_name()
	type_ = None
	expr = None
	if match_token(TOKEN_COLON):
		type_ = parse_type()
		if match_token(TOKEN_ASSIGN):
			expr = parse_expr()
	elif match_token(TOKEN_ASSIGN):
		expr = parse_expr()
	else:
		syntax_error("Expected ':' or '=' after var declaration, got %s" % str(phlex.token))
	expect_token(TOKEN_SEMICOLON)
	return DeclVar(name, type_, expr)

def parse_const_decl():
	name = parse_name()
	expect_token(TOKEN_ASSIGN)
	expr = parse_expr()
	expect_token(TOKEN_SEMICOLON)
	return DeclConst(name, expr)

def parse_typedef_decl():
	name = parse_name()
	expect_token(TOKEN_ASSIGN)
	type_ = parse_type()
	expect_token(TOKEN_SEMICOLON)
	return DeclTypedef(name, type_)

def parse_enum_item():
	name = parse_name()
	expr = None
	if match_token(TOKEN_ASSIGN):
		expr = parse_expr()
	return EnumItem(name, expr)

def parse_enum_decl():
	name = parse_name()
	expect_token(TOKEN_LBRACE)
	items = []
	if not is_token(TOKEN_RBRACE):
		items.append(parse_enum_item())
		while match_token(TOKEN_COMMA):
			if is_token(TOKEN_RBRACE):
				break
			items.append(parse_enum_item())
	expect_token(TOKEN_RBRACE)
	return DeclEnum(name, items)

def parse_aggregate_field():
	if is_token(TOKEN_NAME):
		name = parse_name()
		expect_token(TOKEN_COLON)
		type_ = parse_type()
		return AggregateField(name, type_, None)
	else:
		if match_keyword('struct'):
			return parse_struct_decl()
		elif match_keyword('union'):
			return parse_union_decl()
		elif match_keyword('enum'):
			return parse_enum_decl()
		else:
			syntax_error("Invalid aggregate field '%s'" % str(phlex.token))

def parse_aggregate_fields():
	expect_token(TOKEN_LBRACE)
	fields = []
	while not is_token(TOKEN_RBRACE):
		fields.append(parse_aggregate_field())
	expect_token(TOKEN_RBRACE)
	return fields

def parse_struct_decl():
	name = parse_name()
	fields = parse_aggregate_fields()
	return DeclAggregate(DECL_STRUCT, name, fields)

def parse_union_decl():
	name = parse_name()
	fields = parse_aggregate_fields()
	return DeclAggregate(DECL_UNION, name, fields)

def parse_func_arg():
	name = parse_name()
	expect_token(TOKEN_COLON)
	type_ = parse_type()
	return FuncArg(name, type_)

def parse_func_decl():
	name = parse_name()
	expect_token(TOKEN_LPAREN)
	func_args = []
	if not is_token(TOKEN_RPAREN):
		func_args.append(parse_func_arg())
		while match_token(TOKEN_COMMA):
			func_args.append(parse_func_arg())
	expect_token(TOKEN_RPAREN)
	ret_type = None
	if match_token(TOKEN_ARROW):
		ret_type = parse_type()
	block = parse_stmt_block()
	return DeclFunc(name, func_args, ret_type, block)

def parse_context_decl():
	if match_keyword('var'):
		return parse_var_decl()
	elif match_keyword('const'):
		return parse_const_decl()
	elif match_keyword('typedef'):
		return parse_typedef_decl()
	elif match_keyword('struct'):
		return parse_struct_decl()
	elif match_keyword('union'):
		return parse_union_decl()
	elif match_keyword('enum'):
		return parse_enum_decl()
	else:
		syntax_error('Unknown declaration \'%s\'' % phlex.token.t_val)

def parse_decl():
	if match_keyword('function'):
		return parse_func_decl()
	return parse_context_decl()

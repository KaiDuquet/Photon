import phlex
from phlex import next_token
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

def expect_keyword(keyword):
	if not match_keyword(keyword):
		syntax_error('Expected keyword \'%s\', got %s') % (keyword, str(phlex.token))

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

def parse_base_type():
	if is_token(TOKEN_NAME):
		return TypespecName(parse_name())
	elif match_keyword('functiom'):
		expect_token(TOKEN_LPAREN)
		arg_types = []
		if not is_token(TOKEN_RPAREN):
			arg_types.append(parse_type())
			while match_token(TOKEN_COMMA):
				arg_types.append(parse_type())
		expect_token(TOKEN_RPAREN)
		ret_type = None
		if match_token(TOKEN_ARROW):
			ret_type = parse_type()
		return TypespecFunc(arg_types, ret_type)
	elif match_token(TOKEN_LPAREN):
		type_ = parse_type()
		expect_token(TOKEN_RPAREN)
		return type_
	else:
		syntax_error("Unexpected token %s in specified type" % str(phlex.token))

def parse_type():
	type_ = parse_base_type()
	while is_token(TOKEN_LBRACK) or is_token(TOKEN_MUL):
		if match_token(TOKEN_LBRACK):
			expr = None
			if not is_token(TOKEN_RBRACK):
				expr = parse_expr()
			expect_token(TOKEN_RBRACK)
			type_ = TypespecArray(type_, expr)
		else:
			next_token()
			type_ = TypespecPtr(type_)
	return type_

##########################################################################

def parse_paren_expr():
	expect_token(TOKEN_LPAREN)
	expr = parse_expr()
	expect_token(TOKEN_RPAREN)
	return expr

def parse_compound_expr(type_):
	expect_token(TOKEN_LBRACE)
	args = []
	if not is_token(TOKEN_RBRACE):
		args.apppend(parse_expr())
		while match_token(TOKEN_COMMA):
			args.append(parse_expr())
	expect_token(TOKEN_RBRACE)
	return ExprCompound(type_, args)

def parse_operand_expr():
	if is_token(TOKEN_INT):
		int_val = phlex.token.t_val
		next_token()
		return ExprInt(int_val)
	elif is_token(TOKEN_FLOAT):
		float_val = phlex.token.t_val
		next_token()
		return ExprFloat(float_val)
	elif is_token(TOKEN_STR):
		str_val = phlex.token.t_val
		next_token()
		return ExprStr(str_val)
	elif is_token(TOKEN_NAME):
		name = phlex.token.t_val
		next_token()
		if is_token(TOKEN_LBRACE):
			return parse_compound_expr(TypespecName(name))
		return ExprName(name)
	elif match_token(TOKEN_LPAREN):
		if match_token(TOKEN_COLON):
			type_ = parse_type()
			expect_token(TOKEN_RBRACE)
			return parse_compound_expr(type_)
		expr = parse_expr()
		expect_token(TOKEN_RPAREN)
		return expr
	elif is_token(TOKEN_LBRACE):
		return parse_compound_expr(None)
	else:
		syntax_error('Unexpected token %s in expression', str(phlex.token))

def parse_base_expr():
	expr = parse_operand_expr()
	while is_token(TOKEN_LPAREN) or is_token(TOKEN_LBRACK) or is_token(TOKEN_DOT):
		if match_token(TOKEN_LPAREN):
			call_args = []
			if not is_token(TOKEN_RPAREN):
				call_args.append(parse_expr())
				while match_token(TOKEN_COMMA):
					call_args.append(parse_expr())
			expect_token(TOKEN_RPAREN)
			expr = ExprCall(expr, call_args)
		elif match_token(TOKEN_LBRACK):
			index = parse_expr()
			expect_token(TOKEN_RPAREN)
			expr = ExprIndex(expr, index)
		else:
			next_token()
			name = parse_name()
			expr = ExprField(expr, name)
	return expr

def is_unary_op():
	return phlex.token.t_type in [
		TOKEN_ADD, TOKEN_SUB, TOKEN_NOT, TOKEN_INV, TOKEN_AND, TOKEN_MUL
	]

def parse_unary_expr():
	if is_unary_op():
		op = phlex.token.t_type
		next_token()
		return ExprUnary(op, parse_unary_expr())
	return parse_base_expr()

def parse_range_expr():
	expr = parse_unary_expr()
	if match_token(TOKEN_RANGE):
		expr = ExprBinary(TOKEN_RANGE, parse_unary_expr())
	return expr

def is_mul_op():
	return phlex.token.t_type in [
		TOKEN_MUL, TOKEN_DIV, TOKEN_MOD, TOKEN_AND, TOKEN_LSHIFT, TOKEN_RSHIFT
	]

def parse_mul_expr():
	expr = parse_range_expr()
	while is_mul_op():
		op = phlex.token.t_type
		next_token()
		expr = ExprBinary(op, expr, parse_range_expr())
	return expr

def is_add_op():
	return phlex.token.t_type in [TOKEN_ADD, TOKEN_SUB, TOKEN_OR, TOKEN_XOR]

def parse_add_expr():
	expr = parse_mul_expr()
	while is_add_op():
		op = phlex.token.t_type
		next_token()
		expr = ExprBinary(op, expr, parse_mul_expr())
	return expr

def is_cmp_op():
	return TOKEN_LT <= phlex.token.t_type and phlex.token.t_type <= TOKEN_NE

def parse_cmp_expr():
	expr = parse_add_expr()
	while is_cmp_op():
		op = phlex.token.t_type
		next_token()
		expr = ExprBinary(op, expr, parse_add_expr())
	return expr

def parse_and_expr():
	expr = parse_cmp_expr()
	while match_token(TOKEN_AND_AND):
		expr = ExprBinary(TOKEN_AND_AND, expr, parse_cmp_expr())
	return expr

def parse_or_expr():
	expr = parse_and_expr()
	while match_token(TOKEN_OR_OR):
		expr = ExprBinary(TOKEN_OR_OR, expr, parse_and_expr())
	return expr

def parse_ternary_expr():
	expr = parse_or_expr()
	if match_token(TOKEN_QUESTION):
		then_expr = parse_ternary_expr()
		expect_token(TOKEN_COLON)
		else_expr = parse_ternary_expr()
		expr = ExprTernary(expr, then_expr, else_expr)
	return expr

def parse_expr():
	parse_ternary_expr()

#########################################################################

def parse_stmt_block():
	expect_token(TOKEN_LBRACE)
	stmts = []
	while not is_token(TOKEN_RBRACE):
		stmts.append(parse_stmt())
	expect_token(TOKEN_RBRACE)
	return StmtBlock(stmts)

def is_assign_op():
	return TOKEN_ASSIGN <= phlex.token.t_type and phlex.token.t_type <= TOKEN_RSHIFT_ASSIGN

def parse_base_stmt():
	expr = parse_expr()
	if is_token(TOKEN_INC) or is_token(TOKEN_DEC):
		op = phlex.token.t_type
		next_token()
		return StmtAssign(op, expr, None)
	elif is_assign_op():
		op = phlex.token.t_type
		next_token()
		return StmtAssign(op, expr, parse_expr())
	return StmtExpr(expr)

def parse_if_stmt():
	cond = parse_paren_expr()
	then_block = parse_stmt_block()
	elseifs = []
	else_block = None
	while match_keyword('else'):
		if not match_keyword('if'):
			else_block = parse_stmt_block()
			break
		elseif_cond = parse_paren_expr()
		elseif_block = parse_stmt_block()
		elseifs.append(ElseIf(elseif_cond, elseif_block))
	return StmtIf(cond, then_block, elseifs, else_block)

def parse_while_stmt():
	cond = parse_paren_expr()
	block = parse_stmt_block()
	return StmtWhile(cond, block)

def parse_for_stmt():
	expect_token(TOKEN_LPAREN)
	init = None
	if not is_token(TOKEN_SEMICOLON):
		init = parse_base_stmt()
	expect_token(TOKEN_SEMICOLON)
	cond = None
	if not is_token(TOKEN_SEMICOLON):
		cond = parse_expr()
	expect_token(TOKEN_SEMICOLON)
	update = None
	if not is_token(TOKEN_RPAREN):
		update = parse_base_stmt()
		if isinstance(update, StmtAssign):
			if update.op == TOKEN_COLON_ASSIGN:
				syntax_error("Infered type initializations are not allowed in 'for' update clauses")
	expect_token(TOKEN_RPAREN)
	return StmtFor(init, cond, update)

def parse_do_while_stmt():
	block = parse_stmt_block()
	expect_keyword('while')
	cond = parse_paren_expr()
	expect_token(TOKEN_SEMICOLON)
	return StmtDoWhile(block, cond)

def parse_switch_case():
	exprs = []
	is_default = False
	while is_keyword('case') or is_keyword('default'):
		if match_keyword('case'):
			exprs.append(parse_expr)
		elif match_keyword('default'):
			if is_default:
				syntax_error("Duplicate default labels in same switch clause")
			is_default = True
		else:
			syntax_error("Expected 'case' or 'default' in switch clause, got %s" % str(phlex.token))
		expect_token(TOKEN_COLON)
	stmts = []
	while not is_token(TOKEN_EOF) and not is_token(TOKEN_RBRACE) and not is_keyword('case') and not is_keyword('default'):
		stmts.append(parse_stmt())
	block = StmtBlock(stmts)
	return SwitchCase(exprs, block, is_default)

def parse_switch_stmt():
	expr = parse_paren_expr()
	cases = []
	expect_token(TOKEN_LBRACE)
	while not is_token(TOKEN_EOF) and not is_token(TOKEN_RBRACE):
		cases.append(parse_switch_case())
	expect_token(TOKEN_RBRACE)
	return StmtSwitch(expr, cases)

def parse_return_stmt():
	expr = None
	if not is_token(TOKEN_SEMICOLON):
		expr = parse_expr()
	expect_token(TOKEN_SEMICOLON)
	return StmtReturn(expr)

def parse_stmt():
	if match_keyword('if'):
		return parse_if_stmt()
	elif match_keyword('while'):
		return parse_while_stmt()
	elif match_keyword('for'):
		return parse_for_stmt()
	elif match_keyword('do'):
		return parse_do_while_stmt()
	elif match_keyword('switch'):
		return parse_switch_stmt()
	elif match_keyword('return'):
		return parse_return_stmt()
	elif match_keyword('break'):
		return StmtBreak()
	elif match_keyword('continue'):
		return StmtContinue()
	elif match_keyword('struct'):
		return StmtDecl(parse_struct_decl())
	elif match_keyword('union'):
		return StmtDecl(parse_union_decl())
	elif match_keyword('enum'):
		return StmtDecl(parse_enum_decl())
	elif match_keyword('var'):
		return StmtDecl(parse_var_decl())
	elif match_keyword('const'):
		return StmtDecl(parse_const_decl())
	elif match_keyword('typedef'):
		return StmtDecl(parse_typedef_decl())
	elif is_token(TOKEN_LBRACE):
		return parse_stmt_block()
	else:
		stmt = parse_base_stmt()
		expect_token(TOKEN_SEMICOLON)
		return stmt

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
		expect_token(TOKEN_SEMICOLON)
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

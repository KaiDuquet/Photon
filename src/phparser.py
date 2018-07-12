import phlex
from token import *


def syntax_error(msg):
	print('[!] Syntax Error: ' + msg)
	print('at line %d ->' % phlex.line)
	print('\t' + phlex.source.splitlines()[phlex.line - 1])
	exit(1)


def is_token(t_type):
	if type(t_type) is str:
		return phlex.token.t_val == t_type
	return phlex.token == t_type


def match_token(t_type):
	if is_token(t_type):
		phlex.next_token()
		return True
	return False


def expect_token(t_type):
	if is_token(t_type):
		phlex.next_token()
	else:
		expected = ''
		if type(t_type) is str:
			expected = t_type
		else:
			expected = STR_TOKEN_TYPE[t_type]
		syntax_error('Expected token %s, got %s' % (expected, str(phlex.token)))


# literal: INT | FLOAT | '(' expr ')'
# factor: [-] factor | literal
# term: factor ([*/%] factor)*
# expr: term ([+-] term)*

def parse_literal():
	if is_token(TOKEN_INT):
		int_val = phlex.token.t_val
		phlex.next_token()
		return int_val
	elif is_token(TOKEN_FLOAT):
		float_val = phlex.token.t_val
		phlex.next_token()
		return float_val
	elif match_token('('):
		ret_val = parse_expr()
		expect_token(')')
		return ret_val
	else:
		syntax_error('Invalid token ' + str(phlex.token))

def parse_factor():
	if match_token('-'):
		return -parse_factor()
	return parse_literal()

def parse_term():
	lvalue = parse_factor()
	while is_token('*') or is_token('/') or is_token('%'):
		op = phlex.token.t_val
		phlex.next_token()
		rvalue = parse_factor()
		if op == '*':
			lvalue *= rvalue
		elif op == '/':
			if rvalue == 0:
				# TODO: Implement an Exception/Error system for handling different exceptions
				raise ZeroDivisionError
			lvalue /= rvalue
		else:
			lvalue %= rvalue
	return lvalue

def parse_expr():
	lvalue = parse_term()
	while is_token('+') or is_token('-'):
		op = phlex.token.t_val
		phlex.next_token()
		rvalue = parse_term()
		if op == '+':
			lvalue += rvalue
		else:
			lvalue -= rvalue

	return lvalue

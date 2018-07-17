from phtoken import *
from phast import *
from phlex import *

indent = 0

def phprint(msg):
    print(msg, end='')

def newln():
    global indent
    phprint('\n{0: <{1}}'.format("", 2 * indent))

def print_type(type_):
    if type_ == TYPESPEC_NAME:
        phprint("%s"% type_.name)
    elif type_ == TYPESPEC_FUNC:
        phprint("(function (")
        for arg in type_.arg_types:
            phprint(' ')
            print_type(arg)
        phprint(') ')
        print_type(type_.ret_type)
        phprint(')')
    elif type_ == TYPESPEC_ARRAY:
        phprint('(array ')
        print_type(type_.elem_type)
        phprint(' ')
        print_expr(type_.size)
        phprint(')')
    elif type_ == TYPESPEC_PTR:
        phprint('(ptr ')
        print_type(type_.elem_type)
        phprint(')')
    else:
        assert(False)

def print_expr(expr):
    if expr in [EXPR_INT, EXPR_FLOAT, EXPR_STR]:
        phprint(expr.val)
    elif expr == EXPR_NAME:
        phprint(expr.name)
    elif expr == EXPR_SIZEOF_EXPR:
        phprint('(sizeof_expr ')
        print_expr(expr.expr)
        phprint(')')
    elif expr == EXPR_SIZEOF_TYPE:
        phprint('(sizeof_type ')
        print_type(expr.type_)
    elif expr == EXPR_CALL:
        phprint('(call ')
        print_expr(expr.operand)
        for arg in expr.args:
            phprint(' ')
            print_expr(arg)
        phprint(')')
    elif expr == EXPR_INDEX:
        phprint('(index ')
        print_expr(expr.operand)
        phprint(' ')
        print_expr(expr.expr)
        phprint(')')
    elif expr == EXPR_FIELD:
        phprint('(field ')
        print_expr(expr.operand)
        phprint('.%s' % expr.field_name)
        phprint(')')
    elif expr == EXPR_COMPOUND:
        phprint('(compound ')
        if expr.type_ is None:
            phprint('<null>')
        else:
            print_type(expr.type_)
        for arg in expr.args:
            phprint(' ')
            print_expr(arg)
        phprint(')')
    elif expr == EXPR_UNARY:
        phprint('(%s ' % STR_TOKEN_TYPE[expr.op])
        print_expr(expr.expr)
        phprint(')')
    elif expr == EXPR_BINARY:
        phprint('(%s ' % STR_TOKEN_TYPE[expr.op])
        print_expr(expr.left)
        phprint(' ')
        print_expr(expr.right)
        phprint(')')
    elif expr == EXPR_TERNARY:
        phprint('(? ')
        print_expr(expr.cond)
        phprint(' ')
        print_expr(expr.then_expr)
        phprint(' ')
        print_expr(expr.else_expr)
        phprint(')')

def print_aggregate(decl):
    for field in decl.fields:
        newln()
        if hasattr(field, 'data_decl'):
            print_decl(field.data_decl)
        else:
            phprint('(')
            print_type(field.type_)
            for name in field.names:
                phprint(' %s' % name)
            phprint(')')

def print_decl(decl):
    global indent
    if decl == DECL_VAR:
        phprint('(var %s ' % decl.name)
        if decl.type_ is None:
            phprint('<null>')
        else:
            print_type(decl.type_)
        phprint(' ')
        print_expr(decl.expr)
        phprint(')')
    elif decl == DECL_CONST:
        phprint('(const %s ' % decl.name)
        print_expr(decl.expr)
        phprint(')')
    elif decl == DECL_TYPEDEF:
        phprint('(typedef %s ' % decl.name)
        print_type(decl.type_)
        phprint(')')
    elif decl == DECL_STRUCT:
        phprint('(struct %s' % decl.name)
        indent += 1
        print_aggregate(decl)
        indent -= 1
        phprint(')')
    elif decl == DECL_UNION:
        phprint('(union %s' % decl.name)
        indent += 1
        print_aggregate(decl)
        indent -= 1
        phprint(')')
    elif decl == DECL_ENUM:
        phprint('(enum %s' % decl.name)
        indent += 1
        for item in decl.items:
            newln()
            phprint('(%s ' % item.name)
            if item.expr is not None:
                print_expr(item.expr)
            else:
                phprint('<null>')
            phprint(')')
        indent -= 1
        phprint(')')
    elif decl == DECL_FUNC:
        phprint('(function %s ' % decl.name)
        phprint('(')
        for arg in decl.args:
            phprint(" %s: " % arg.name)
            print_type(arg.type_)
        phprint(')')
        if decl.ret_type is None:
            phprint('<null>')
        else:
            print_type(decl.ret_type)
        indent += 1
        newln()
        print_stmt_block(decl.block)
        indent -= 1
        phprint(')')

def print_stmt_block(block):
    global indent
    phprint('(block')
    indent += 1
    for stmt in block.stmts:
        newln()
        print_stmt(stmt)
    indent -= 1
    phprint(')')

def print_stmt(stmt):
    global indent
    if stmt == STMT_BREAK:
        phprint('(break)')
    elif stmt == STMT_CONTINUE:
        phprint('(continue)')
    elif stmt == STMT_BLOCK:
        print_stmt_block(stmt.stmt_list)
    elif stmt == STMT_RETURN:
        phprint('(return ')
        if stmt.expr is not None:
            print_expr(stmt.expr)
        phprint(')')
    elif stmt == STMT_DECL:
        print_decl(stmt.decl)
    elif stmt == STMT_IF:
        phprint('(if ')
        print_expr(stmt.cond)
        indent += 1
        newln()
        print_stmt_block(stmt.then_block)
        for elseif in stmt.elseifs:
            newln()
            phprint('elseif ')
            print_expr(elseif.cond)
            newln()
            print_stmt_block(elseif.block)
        if stmt.else_block is not None:
            newln()
            phprint('else')
            newln()
            print_stmt_block(stmt.else_block)
        indent -= 1
        phprint(')')
    elif stmt == STMT_WHILE:
        phprint('(while ')
        print_expr(stmt.expr)
        indent += 1
        newln()
        print_stmt_block(stmt.block)
        indent -= 1
        phprint(')')
    elif stmt == STMT_DO_WHILE:
        phprint('(do')
        indent += 1
        newln()
        print_stmt_block(stmt.block)
        indent -= 1
        phprint('while ')
        print_expr(stmt.expr)
        phprint(')')
    elif stmt == STMT_FOR:
        phprint('(for ')
        print_stmt(stmt.init)
        print_expr(stmt.cond)
        print_stmt(stmt.update)
        indent += 1
        newln()
        print_stmt_block(stmt.block)
        indent -= 1
        phprint(')')
    elif stmt == STMT_SWITCH:
        phprint('(switch ')
        print_expr(stmt.expr)
        indent += 1
        for case in stmt.cases:
            newln()
            phprint('(%s (' % ('default' if case.is_default else 'case'))
            for expr in case.exprs:
                phprint(' ')
                print_expr(expr)
            phprint(')')
            indent += 1
            newln()
            print_stmt_block(case.block)
            indent -= 1
        indent -= 1
        phprint(')')
    elif stmt == STMT_ASSIGN:
        phprint('(%s ' % STR_TOKEN_TYPE[stmt.op])
        print_expr(stmt.left)
        if stmt.right is not None:
            phprint(' ')
            print_expr(stmt.right)
        phprint(')')
    elif stmt == STMT_EXPR:
        print_expr(stmt.expr)

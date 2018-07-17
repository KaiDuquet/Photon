TYPESPEC_NAME = "TYPESPEC_NAME"
TYPESPEC_FUNC = "TYPESPEC_FUNC"
TYPESPEC_ARRAY = "TYPESPEC_ARRAY"
TYPESPEC_PTR = "TYPESPEC_PTR"

class Typespec(object):
    """docstring for Typespec."""
    def __init__(self, kind):
        self.kind = kind

class TypespecName(Typespec):
    """docstring for TypespecName."""
    def __init__(self, name):
        super(TypespecName, self).__init__(TYPESPEC_NAME)
        self.name = name

class TypespecFunc(Typespec):
    """docstring for TypespecFunc."""
    def __init__(self, arg_types, ret_type):
        super(TypespecFunc, self).__init__(TYPESPEC_FUNC)
        self.arg_types = arg_types
        self.ret_type = ret_type

class TypespecArray(Typespec):
    """docstring for TypespecArray."""
    def __init__(self, elem_type, size):
        super(TypespecArray, self).__init__(TYPESPEC_ARRAY)
        self.elem_type = elem_type
        self.size = size

class TypespecPtr(Typespec):
    """docstring for TypespecPtr."""
    def __init__(self, elem_type):
        super(TypespecPtr, self).__init__(TYPESPEC_PTR)
        self.elem_type = elem_type


DECL_FUNC = "DECL_FUNC"
DECL_ENUM = "DECL_ENUM"
DECL_STRUCT = "DECL_STRUCT"
DECL_UNION = "DECL_UNION"
DECL_VAR = "DECL_VAR"
DECL_CONST = "DECL_CONST"
DECL_TYPEDEF = "DECL_TYPEDEF"

class Decl(object):
    """docstring for Decl ."""
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name

class FuncArg(object):
    """docstring for FuncArg."""
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

class DeclFunc(Decl):
    """docstring for DeclFunc."""
    def __init__(self, name, args, ret_type, block):
        super(DeclFunc, self).__init__(DECL_FUNC, name)
        self.args = args
        self.ret_type = ret_type
        self.block = block

class EnumItem(object):
    """docstring for EnumItem."""
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class DeclEnum(Decl):
    """docstring for DeclEnum."""
    def __init__(self, name, items):
        super(DeclEnum, self).__init__(DECL_ENUM)
        self.items = items

class AggregateField(object):
    """docstring for AggregateField."""
    def __init__(self, name, type_, data_decl):
        if name is None and type_ is None:
            self.data_decl = data_decl
        else:
            self.name = name
            self.type_ = type_

class DeclAggregate(Decl):
    """docstring for DeclAggregate."""
    def __init__(self, kind, name, fields):
        assert(kind == DECL_STRUCT or kind == DECL_UNION)
        super(DeclAggregate, self).__init__(kind, name)
        self.fields = fields

class DeclVar(Decl):
    """docstring for DeclVar."""
    def __init__(self, name, type_, expr):
        super(DeclVar, self).__init__(DECL_VAR, name)
        self.type_ = type_
        self.expr = expr

class DeclConst(Decl):
    """docstring for DeclConst."""
    def __init__(self, name, expr):
        super(DeclConst, self).__init__(DECL_CONST, name)
        self.expr = expr

class DeclTypedef(Decl):
    """docstring for DeclTypedef."""
    def __init__(self, name, _type):
        super(DeclTypedef, self).__init__(DECL_TYPEDEF, name)
        self.type_ = type_

#############################################################

STMT_DECL = "STMT_DECL"
STMT_IF = "STMT_IF"
STMT_WHILE = "STMT_WHILE"
STMT_FOR = "STMT_FOR"
STMT_DO_WHILE = "STMT_DO_WHILE"
STMT_SWITCH = "STMT_SWITCH"
STMT_RETURN = "STMT_RETURN"
STMT_BREAK = "STMT_BREAK"
STMT_CONTINUE = "STMT_CONTINUE"
STMT_EXPR = "STMT_EXPR"
STMT_ASSIGN = "STMT_ASSIGN"

class Stmt(object):
    """docstring for Stmt."""
    def __init__(self, kind):
        self.kind = kind

class StmtAssign(Stmt):
    """docstring for StmtAssign."""
    def __init__(self, op, left, right):
        super(StmtAssign, self).__init__(STMT_ASSIGN)
        self.op = op
        self.left = left
        self.right = right


class StmtBlock(object):
    """docstring for StmtBlock."""
    def __init__(self, stmts):
        self.stmts = stmts


class StmtDecl(Stmt):
    """docstring for StmtDecl."""
    def __init__(self, decl):
        super(StmtDecl, self).__init__(STMT_DECL)
        self.decl = decl

class ElseIf(object):
    """docstring for ElseIf."""
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

class StmtIf(Stmt):
    """docstring for StmtIf."""
    def __init__(self, cond, then_block, elseifs, else_block):
        super(StmtIf, self).__init__(STMT_IF)
        self.cond = cond
        self.then_block = then_block
        self.elseifs = elseifs
        self.else_block = else_block

class StmtWhile(Stmt):
    """docstring for StmtWhile."""
    def __init__(self, expr, block):
        super(StmtWhile, self).__init__(STMT_WHILE)
        self.expr = expr
        self.block = block

class StmtFor(Stmt):
    """docstring for StmtFor."""
    def __init__(self, init, cond, update, block):
        super(StmtFor, self).__init__(STMT_FOR)
        self.init = init
        self.cond = cond
        self.update = update
        self.block = block

class StmtDoWhile(Stmt):
    """docstring for StmtDoWhile."""
    def __init__(self, block, expr):
        super(StmtDoWhile, self).__init__(STMT_DO_WHILE)
        self.block = block
        self.expr = expr

class StmtReturn(Stmt):
    """docstring for StmtReturn."""
    def __init__(self, expr):
        super(StmtReturn, self).__init__(STMT_RETURN)
        self.expr = expr

class StmtBreak(Stmt):
    """docstring for StmtBreak."""
    def __init__(self):
        super(StmtBreak, self).__init__(STMT_BREAK)

class StmtContinue(Stmt):
    """docstring for StmtContinue."""
    def __init__(self):
        super(StmtContinue, self).__init__(STMT_CONTINUE)

class SwitchCase(object):
    """docstring for SwitchCase."""
    def __init__(self, exprs, stmts, is_default):
        self.exprs = exprs
        self.stmts = stmts
        self.is_default

class StmtSwitch(Stmt):
    """docstring for StmtSwitch."""
    def __init__(self, expr, cases):
        super(StmtSwitch, self).__init__(STMT_SWITCH)
        self.expr = expr
        self.cases = cases

class StmtExpr(Stmt):
    """docstring for StmtExpr."""
    def __init__(self, expr):
        super(StmtExpr, self).__init__(STMT_EXPR)
        self.expr = expr

############################################################

EXPR_TERNARY = "EXPR_TERNARY"
EXPR_BINARY = "EXPR_BINARY"
EXPR_UNARY = "EXPR_UNARY"
EXPR_INT = "EXPR_INT"
EXPR_FLOAT = "EXPR_FLOAT"
EXPR_STR = "EXPR_STR"
EXPR_NAME = "EXPR_NAME"
EXPR_COMPOUND = "EXPR_COMPOUND"
EXPR_CALL = "EXPR_CALL"
EXPR_INDEX = "EXPR_INDEX"
EXPR_FIELD = "EXPR_FIELD"
EXPR_SIZEOF_EXPR = "EXPR_SIZEOF_EXPR"
EXPR_SIZEOF_TYPE = "EXPR_SIZEOF_TYPE"


class Expr(object):
    """docstring for Expr."""
    def __init__(self, kind):
        self.kind = kind

class ExprTernary(Expr):
    """docstring for ExprTernary."""
    def __init__(self, cond, then_expr, else_expr):
        super(ExprTernary, self).__init__(EXPR_TERNARY)
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

class ExprBinary(Expr):
    """docstring for ExprBinary."""
    def __init__(self, op, left, right):
        super(ExprBinary, self).__init__(EXPR_BINARY)
        self.op = op
        self.left = left
        self.right = right

class ExprUnary(Expr):
    """docstring for ExprUnary."""
    def __init__(self, op, expr):
        super(ExprUnary, self).__init__(EXPR_UNARY)
        self.expr = expr

class ExprInt(Expr):
    """docstring for ExprInt."""
    def __init__(self, val):
        super(ExprInt, self).__init__(EXPR_INT)
        self.val = val

class ExprFloat(Expr):
    """docstring for ExprFloat."""
    def __init__(self, val):
        super(ExprFloat, self).__init__(EXPR_FLOAT)
        self.val = val

class ExprStr(Expr):
    """docstring for ExprStr."""
    def __init__(self, val):
        super(ExprStr, self).__init__(EXPR_STR)
        self.val = val

class ExprName(Expr):
    """docstring for ExprName."""
    def __init__(self, name):
        super(ExprName, self).__init__(EXPR_NAME)
        self.name = name

class ExprCall(Expr):
    """docstring for ExprCall."""
    def __init__(self, operand, args):
        super(ExprCall, self).__init__(EXPR_CALL)
        self.operand = operand
        self.args = args

class ExprIndex(Expr):
    """docstring for ExprIndex."""
    def __init__(self, operand, expr):
        super(ExprIndex, self).__init__(EXPR_INDEX)
        self.operand = operand
        self.expr = expr

class ExprField(Expr):
    """docstring for ExprField."""
    def __init__(self, operand, field_name):
        super(ExprField, self).__init__(EXPR_FIELD)
        self.operand = operand
        self.field_name = field_name

class ExprCompound(Expr):
    """docstring for ExprCompound."""
    def __init__(self, type_, args):
        super(ExprCompound, self).__init__(EXPR_COMPOUND)
        self.type_ = type_
        self.args = args

class ExprSizeofExpr(Expr):
    """docstring for ExprSizeofExpr."""
    def __init__(self, expr):
        super(ExprSizeofExpr, self).__init__(EXPR_SIZEOF_EXPR)
        self.expr = expr

class ExprSizeofType(Expr):
    """docstring for ExprSizeofType."""
    def __init__(self, type_):
        super(ExprSizeofType, self).__init__(EXPR_SIZEOF_TYPE)
        self.type_ = type_

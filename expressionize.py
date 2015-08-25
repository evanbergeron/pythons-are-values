import ast
import sys
import unparse
from cStringIO import StringIO

# Helpful macros
DEF_LET_GLOBAL = "globals().update({'let_global': lambda k,v : globals().update({k:v})})"
IMPORT_SYS = "let_global('sys', __import__('sys'))"
DEF_THROW = "let_global('throw', lambda e : (_ for _ in ()).throw(e))"
DEF_PRINTF = "let_global('printf', lambda *s : sys.stdout.write('%s\\n' % ' '.join(map(str, s))))"
DEF_WHILE = "let_global('WHILE', lambda e, b : (e() and (b(), WHILE(e, b)) or None))"

MACROS = [DEF_LET_GLOBAL, IMPORT_SYS, DEF_THROW, DEF_PRINTF, DEF_WHILE]
HEADER = " or ".join(MACROS) + "\n"

with open("a.py", 'w') as f:
  f.write(HEADER)

# DEBUG = True
DEBUG = False

def parsed(source):
    '''Meant for parsing single lines of code'''
    source = ast.parse(source)
    # By default, type(source) is ast.Module
    return source.body[0]

def unparsed(node):
    '''Wrapper for the unparse module'''
    tmp = StringIO()
    unparse.Unparser(node, tmp)
    result = tmp.getvalue()
    tmp.close()
    return result.strip()

def dfs_fix_children(node):
    # Bears great resemblence to ast.iter_fields
    for name, field in ast.iter_fields(node):
        if isinstance(field, ast.AST):
            node.__dict__[name] = expressionize(field)
        elif isinstance(field, list):
            newField = []
            for item in field:
                if isinstance(item, ast.AST):
                    newField.append(expressionize(item))
            node.__dict__[name] = newField
    return None

def visit_Module(node):
    return node

def visit_Print(node):
    args = ", ".join([unparsed(value) for value in node.values])
    goal = "printf(%s)" % args
    return parsed(goal)

def visit_Assign(node):
    targets = unparsed(node.targets)
    value = unparsed(node.value)
    goal = "[%s for %s in [%s]]" % (targets, targets, value)
    return parsed(goal)

def visit_Num(node):
    return node

def visit_FunctionDef(node):
    name = node.name
    args = unparsed(node.args)
    body = unparsed(node.body)
    func = "lambda %s : %s" % (args, body)
    goal = "[%s for %s in [%s]]" % (name, name, func)
    return parsed(goal)

def visit_Return(node):
    return node.value

def visit_For(node):
    body = unparsed(node.body)
    target = unparsed(node.target)
    iterable = unparsed(node.iter)
    goal = "[%s for %s in %s]" % (body, target, iterable)
    return parsed(goal)

def visit_While(node):
    test = 'lambda : %s' % unparsed(node.test)
    body = 'lambda : %s' % unparsed(node.body)
    goal = "WHILE(%s, %s)" % (test, body)
    return parsed(goal)

def visit_If(node):
    test = unparsed(node.test)
    body = unparsed(node.body)
    if hasattr(node, "orelse"):
        elseClause = "%s" % unparsed(node.orelse)
    else:
        elseClause = "None"
    goal = "%s if %s else %s" % (body, test, elseClause)
    return parsed(goal)

def visit_Assert(node):
    test = unparsed(node.test)
    msg = unparsed(node.msg) if node.msg is not None else ""
    goal = "() if %s else throw(AssertionError, %s)" % (test, msg)
    return parsed(goal)

def unparse_op(op):
    case = {

           ast.Add : "+",
           ast.Sub : "-",
          ast.Mult : "*",
        ast.Div    : "/",
        ast.BitAnd : "&",
        ast.BitXor : "^",

    }
    if type(op) not in case:
        print type(op)
        raise FutureWarning
    return case[type(op)]

def visit_AugAssign(node):
    # target, op, value
    target = unparsed(node.target)
    op = unparse_op(node.op)
    value = unparsed(node.value)
    goal = "[None for %s in [%s %s %s]]" % (target, target, op, value)
    return parsed(goal)

options = {

    ast.Module      : visit_Module,
    ast.Print       : visit_Print,
    ast.Num         : visit_Num,
    ast.Assign      : visit_Assign,
    ast.Num         : visit_Num,
    ast.FunctionDef : visit_FunctionDef,
    ast.Return      : visit_Return,
    ast.For         : visit_For,
    ast.While       : visit_While,
    ast.If          : visit_If,
    ast.Assert      : visit_Assert,
    ast.AugAssign   : visit_AugAssign,

}

def is_listcomp(node):
    try:
        return type(node.value) is ast.ListComp
    except AttributeError:
        return False

def expressionize(node):
    if DEBUG: print type(node)
    dfs_fix_children(node)

    if hasattr(node, 'body') and type(node) is not ast.Module:
        # Replace multiple lines with a single list comphrension

        # Each element in this list comphrension is either a
        # lambda function representing a  line of code or
        # another list comphrension, used for variable assignment
        # and reassignment
        if type(node.body) is list and len(node.body) > 1:
            lines = []
            for item in node.body:
                if is_listcomp(item):
                    # List comphrensions' side effects need to be
                    # preserved in current namespace
                    lines.append(item)
                else:
                    lmbda = ast.Lambda(args = [], body = item)
                    lines.append(lmbda)
            # Black magic
            goal =  str([unparsed(line).replace("\n", "") for line in lines]).replace("'", "")
            node.body = parsed("[_() if hasattr(_, '__call__') else _ for _ in %s]" % goal)

        elif isinstance(node.body, ast.AST):
            pass

    try: return options[type(node)](node)
    except KeyError:
        return node

def main(src):
    src = HEADER + src
    try:
        root = ast.parse(src)
    except SyntaxError:
        print "Invalid syntax in original file"
        exit(-1)
    exp = expressionize(root)
    return unparsed(exp).strip()

if __name__ == "__main__":
    with open(sys.argv[1], "r") as src:
        src = src.read()
        if DEBUG: print src
        print main(src)

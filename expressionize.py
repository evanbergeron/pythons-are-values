import ast
import sys
import unparse
from cStringIO import StringIO

# Helpful macros
DEF_LET_GLOBAL = "globals().update({'let_global': lambda k,v : globals().update({k:v})})"
IMPORT_SYS = "let_global('sys', __import__('sys'))"
DEF_THROW = "let_global('throw', lambda e : (_ for _ in ()).throw(e))"
DEF_PRINTF = "let_global('printf', lambda *s : sys.stdout.write('%s\\n' % ' '.join(map(str, s))))"

MACROS = [DEF_LET_GLOBAL, IMPORT_SYS, DEF_THROW, DEF_PRINTF]
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

options = {

    ast.Module      : visit_Module,
    ast.Print       : visit_Print,
    ast.Num         : visit_Num,
    ast.Assign      : visit_Assign,
    ast.Num         : visit_Num,
    ast.FunctionDef : visit_FunctionDef,
    ast.Return      : visit_Return,
    ast.For         : visit_For

}

def expressionize(node):
    if DEBUG: print type(node)
    dfs_fix_children(node)

    if hasattr(node, 'body') and type(node) is not ast.Module:
        # Replace multiple lines with a single list comphrension
        # TODO - not fully working

        if type(node.body) is list and len(node.body) > 1:
            lines = []
            for item in node.body:
                lmbda = ast.Lambda(args = [], body = item)
                lines.append(lmbda)
            # Black magic
            goal =  str([unparsed(line).replace("\n", "") for line in lines]).replace("'", "")
            node.body = parsed("[_() for _ in %s]" % goal)

        elif isinstance(node.body, ast.AST):
            pass

    try: return options[type(node)](node)
    except KeyError:
        return node

if __name__ == "__main__":
    with open(sys.argv[1], "r") as src:
        src = src.read()
        if DEBUG: print src
        src = HEADER + src
        try:
            root = ast.parse(src)
        except SyntaxError:
            print "Invalid syntax in original file"
            exit(-1)
        exp = expressionize(root)
        print unparsed(exp).strip()

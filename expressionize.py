import sys
import ast
import unparse
from pprint import pprint
from collections import deque
from cStringIO import StringIO

# Helpful macros
IMPORT_SYS = "__import__('sys')._getframe(-1).f_locals.update({'sys':__import__('sys')})"
DEF_VARS = "sys._getframe(-1).f_locals.update({'vvvs' : sys._getframe(-1).f_locals})"
DEF_LET = "sys._getframe(-1).f_locals.update({'let': lambda x, v : vvvs.update({x:v})})"
DEF_THROW = "let('throw', lambda e : (_ for _ in ()).throw(e))"
DEF_PRINTF = "let('printf', lambda *s : sys.stdout.write('%s\\n' % ' '.join(map(str, s))))"

MACROS = [IMPORT_SYS, DEF_VARS, DEF_LET, DEF_THROW, DEF_PRINTF]
HEADER = " or ".join(MACROS) + "\n"

def parsed(source):
    source = ast.parse(source)
    return source.__dict__['body'][0]

def unparsed(node):
    tmp = StringIO()
    unparse.Unparser(node, tmp)
    result = tmp.getvalue()
    tmp.close()
    return result

class Expressionizer(ast.NodeTransformer):

    @staticmethod
    def parsed(source):
        source = ast.parse(source)
        return source.__dict__['body'][0]

    @staticmethod
    def unparsed(node):
        tmp = StringIO()
        unparse.Unparser(node, tmp)
        result = tmp.getvalue()
        tmp.close()
        return result

class BFS(Expressionizer):

    def generic_visit(self, node):
        pass

class OrBody(Expressionizer):

    def generic_visit(self, node):
        if 'body' in node.__dict__:
            return self.orTogether(node)
        return node

    def orTogether(self, node):
        goal = ['()']
        tmp = StringIO()
        for subnode in node.__dict__['body']:
            goal.append(self.unparsed(subnode).strip())
        goal = " or ".join(goal)
        return self.parsed(goal)

class ReturnToValue(Expressionizer):

    def visit_Return(self, node):
        src = self.unparsed(node)
        goal = " ".join([item.strip() for item in src.split("return")[1:]])
        return self.parsed(goal)

class ExpressionizeForLoops(Expressionizer):

    def visit_For(self, node):

        # Grab loop line
        src = self.unparsed(node)
        loopLine = src.split("\n")[1][:-1] # remove colon

        # Or together body
        orTogether = OrBody()
        node = orTogether.visit(node)
        body = self.unparsed(node)
        goal = "[(lambda : %s)() %s]" % (body, loopLine)
        return self.parsed(goal)

class DefToLambda(Expressionizer):

    @staticmethod
    def function_name(node):
        return node.__dict__['name']

    @staticmethod
    def function_args(node):
        return node.__dict__['args']

    @staticmethod
    def function_body(node):
        orTogether = OrBody()
        return orTogether.visit(node)

    def visit_FunctionDef(self, node):
        args = self.unparsed(self.function_args(node))
        # name = self.unparsed(self.function_name(node))
        name = self.function_name(node)
        body = self.unparsed(self.function_body(node))
        func = "lambda %s : %s" % (args, body)
        goal = "let(%r, %s)" % (name, func)
        return self.parsed(goal)

class LineByLineExpressionizer(Expressionizer):

    def visit_Print(self, node):
        printedObjects = node.__dict__['values']
        tmp = StringIO()
        for obj in printedObjects:
            unparse.Unparser(obj, tmp)
        goal = "printf(%s)" % str(tmp.getvalue())
        tmp.close()
        return self.parsed(goal)
        return node

    def visit_Assign(self, node):
        # Unparse node into currentLineOfCode
        tmp = StringIO()
        unparse.Unparser(node, tmp)
        currentLineOfCode = tmp.getvalue()
        tmp.write("")
        tmp.close()
        # Grab target and value
        target = currentLineOfCode.split("=")[0]
        value = currentLineOfCode.split("=")[1]
        # List comphrensions have side effects
        goal = "([%s for %s in [%s]] and ())" % (target, target, value)
        return self.parsed(goal)

    def visit_Import(self, node):
        src = self.unparsed(node)
        module = src.split(" ")[1]
        goal = "(not [%s for %s in [__import__('%s')]])" % (module, module, module)
        return self.parsed(goal)

    def visit_Assert(self, node):
        src = self.unparsed(node)
        condition = " ".join(src.split("assert")[1:])
        goal = "((%s or throw(AssertionError, '')) and ())" % condition
        return self.parsed(goal)

    def visit_Raise(self, node):
        src = self.unparsed(node)
        toThrow = "".join(src.split("raise")[1:])
        goal = "throw(%s)" % toThrow
        return self.parsed(goal)

def body_nodes_reverse_bfs(root):
    result = []
    visitedNodes = set()
    queue = deque([root])

    while len(queue) > 0:
        node = queue.pop()
        if node in visitedNodes:
            continue

        visitedNodes.add(node)
        if 'body' in node.__dict__:
            result.append(node)

        for child in ast.iter_child_nodes(node):
            if child not in visitedNodes:
                queue.appendleft(child)
    return reversed(result)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        source = sys.argv[1]
    else:
        print "No command line argument found"
        exit(-1)
    with open(source, "r+") as src:
        src = src.read()
        src = HEADER + src
        unmodified = ast.parse(src)
        # pprint([n for n in body_nodes_reverse_bfs(unmodified)])

        # Fix variables assignments and print statements
        transformer = LineByLineExpressionizer()
        modified = transformer.visit(unmodified)

        # Get rid of returns
        noReturns = ReturnToValue()
        modified = noReturns.visit(unmodified)

        # Func to lambda
        noDefs = DefToLambda()
        modified = noDefs.visit(modified)

        # fix Loops
        fixForLoops = ExpressionizeForLoops()
        modified = fixForLoops.visit(modified)

        # Or together bodies
        orMaster = OrBody()
        modified = orMaster.visit(modified)

        # Unparse AST and write to result
        result = StringIO()
        unparse.Unparser(modified, result)
        print "%s\n" % result.getvalue().strip()
        result.close()

import sys
import ast
import unparse
from cStringIO import StringIO

# Imports sys and defines a new print function
IMPORT_SYS = "__import__('sys')._getframe(-1).f_locals.update({'sys':__import__('sys')}) or sys._getframe(-1).f_locals.update({'printf': lambda *s : sys.stdout.write('%s\\n' % ' '.join(map(str, s)))})\n"

class OrBody(ast.NodeTransformer):
    def generic_visit(self, node):
        if 'body' in node.__dict__:
            # node.__dict__['body'] = self.orTogether(node)
            return self.orTogether(node)
        return node

    # @staticmethod
    def orTogether(self, node):
        goal = ['False']
        tmp = StringIO()
        for subnode in node.__dict__['body']:
            goal.append(self.unparsed(subnode).strip())
        goal = " or ".join(goal)
        # assert(False)
        return self.parsed(goal)

    @staticmethod
    def unparsed(node):
        tmp = StringIO()
        unparse.Unparser(node, tmp)
        result = tmp.getvalue()
        tmp.close()
        return result

    @staticmethod
    def parsed(source):
        source = ast.parse(source)
        return source.__dict__['body'][0]

class ExpressionizeAssignmentsAndPrint(ast.NodeTransformer):

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
        goal = "([%s for %s in [%s]] and False)" % (target, target, value)
        return self.parsed(goal)

    @staticmethod
    def parsed(source):
        source = ast.parse(source)
        return source.__dict__['body'][0]

def orTogether(src):
    src = src.split("\n")
    return "False" + " or ".join(src)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        source = sys.argv[1]
    else:
        print "No command line argument found"
        exit(-1)
    with open(source, "r+") as src:
        src = src.read()

        src = IMPORT_SYS + src
        unmodified = ast.parse(src)

        transformer = ExpressionizeAssignmentsAndPrint()
        modified = transformer.visit(unmodified)

        result = StringIO()

        orMaster = OrBody()
        modified = orMaster.visit(modified)

        unparse.Unparser(modified, result)


        print "%s\n" % result.getvalue().strip()
        result.close()
        # print orTogether(result.getvalue())

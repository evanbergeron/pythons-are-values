import ast
import sys
import unparse
from cStringIO import StringIO

class Expressionizer(ast.NodeTransformer):

    def visit_Print(self, node):
        '''
        print someObject -->
            __import__('sys').stdout.write(str(someObject))
        '''
        printedObjects = node.__dict__['values']
        print printedObjects
        tmp = StringIO()
        for obj in printedObjects:
            unparse.Unparser(obj, tmp)
        print tmp.getvalue()

        goal = "__import__('sys').stdout.write(%%s)"
        newNode = self.parsed(goal)
        # return newNode
        # if len(printedObjects) == 0:
        #     # For now, erase empty print statements
        #     return None
        # printedObject = printedObjects[0]
        # # sys.stdout.write expects a character buf arg
        # printExpr = "__import__('sys').stdout.write(str('foo'))"
        # printExprNode = ast.parse(printExpr)
        # # Sneak into printExpr's stdou.write argument and change it
        # printExprNode.__dict__['body'][0].__dict__['value'].__dict__['args'][0].__dict__['args'][0] = printedObject
        # return printExprNode

    @staticmethod
    def assign_print_info(node):
        print "##########################"
        print "# Visiting an assignment #"
        print "##########################"
        print node.__dict__
        print
        print "Targets: (or variables)"
        for target in node.__dict__['targets']:
            print target.__dict__
        print "Value:"
        print node.__dict__['value'].__dict__
        print "##########################"

    def visit_Assign(self, node):
        tmp = StringIO()
        unparse.Unparser(node, tmp)
        currentLineOfCode = tmp.getvalue()
        tmp.write("")
        tmp.close()
        currentLineOfCode = currentLineOfCode.split("=")
        (target, value) = currentLineOfCode[0].strip(), currentLineOfCode[1].strip()
        # Note that this eval hack will not work for certain python values
        # eg - exceptions
        d = {target:eval(value)}
        goal = "__import__('sys')._getframe(-1).f_locals.update(%s)\n" % d
        goal = self.parsed(goal)
        return goal

    def visit_Raise(self, node):
        # All exceptions are FutureWarnings. Proof of concept,
        return self.parsed("raise FutureWarning")

    @classmethod
    def print_all(self, node):
        for subnode in ast.walk(node):
            if 'body' in subnode.__dict__:
                print subnode
                print subnode.__dict__

    @staticmethod
    def printDict(node):
        print node.__dict__

    @staticmethod
    def parsed(source):
        # Returns the ast object corresponding to a single line of code.
        # (Removes the module cruft)
        source = ast.parse(source)
        result = source.__dict__['body'][0]
        # print result
        return result

def parsed(source):
    # Returns the ast object corresponding to a single line of code.
    # (Removes the module cruft)
    source = ast.parse(source)
    result = source.__dict__['body'][0]
    # print result
    return result

with open(sys.argv[1], 'r') as sourceCode:
    sourceCode = sourceCode.read()
    unmodified = ast.parse(sourceCode)
    transformer = Expressionizer()
    # transformer.print_all(unmodified)
    modified = transformer.visit(unmodified)
    result = StringIO()
    unparse.Unparser(modified, result)
    print "%s\n" % result.getvalue()

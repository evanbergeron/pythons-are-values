import ast
import sys
import unparse

class Expressionizer(ast.NodeTransformer):
    def visit_Print(self, node):
        '''
        print someObject -->
            __import__('sys').stdout.write(str(someObject))
        '''
        printedObjects = node.__dict__['values']
        if len(printedObjects) == 0:
            # For now, erase empty print statements
            return None
        printedObject = printedObjects[0]
        # sys.stdout.write expects a character buf arg
        printExpr = "__import__('sys').stdout.write(str('foo'))"
        printExprNode = ast.parse(printExpr)
        # Sneak into printExpr's stdou.write argument and change it
        printExprNode.__dict__['body'][0].__dict__['value'].__dict__['args'][0].__dict__['args'][0] = printedObject
        return printExprNode

with open(sys.argv[1], 'r') as sourceCode:
    sourceCode = sourceCode.read()
    unmodified = ast.parse(sourceCode)
    transformer = Expressionizer()
    modified = transformer.visit(unmodified)
    unparse.Unparser(modified, sys.stdout)

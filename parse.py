import ast
import sys
import astpp

print astpp.dump(ast.parse(sys.argv[1]))

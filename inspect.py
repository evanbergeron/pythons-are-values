import sys
import ast

with open(sys.argv[1], "r") as source:
    source = ast.parse(source.read())
    source = source.__dict__['body'][0]
    print source.__dict__

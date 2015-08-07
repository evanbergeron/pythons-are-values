import unittest
import sys
import ast
import unparse
import pprint

# Iteration 1

class TryExcept(unittest.TestCase):

    def __init__(self, func, methodName='runTest'):
        super(TryExcept, self).__init__(methodName=methodName)
        self.func = func

    def raises(self, ex):
        return self.assertRaises(ex, self.func) is None

t = TryExcept(lambda : 1 / 0, methodName='raises')
print t.raises(ZeroDivisionError) # True

# Iteration 2

class Concise(unittest.TestCase):
    failureException = Exception
    def runTest(self, ex, func):
        return self.assertRaises(ex, func) is None

c = Concise()
print c.runTest(ZeroDivisionError, lambda : 1/0)

# Iteration 3

Conciser = type('Conciser', (unittest.TestCase,),
                dict(runTest = lambda self, ex, func :
                self.assertRaises(ex, func) is None))

cr = Conciser()
print cr.runTest(ZeroDivisionError, lambda : 1/0)

# More readable version

TR = type('tr', (unittest.TestCase,),
                dict(yexcept = lambda self, ex, func :
                self.assertRaises(ex, func) is None))

tr = TR(methodName='yexcept')
print tr.yexcept(ZeroDivisionError, lambda : 1/0)

# Must get shorter!

tr = type('tr', (unittest.TestCase,), dict(y = lambda self, ex, func :
          self.assertRaises(ex, func) is None))(methodName='y')

print tr.y(ZeroDivisionError, lambda : 1/0)

# To be pendantic...

tr = type('tr', (__import__('unittest').TestCase,), dict(y =
lambda self, ex, func : self.assertRaises(ex, func) is None))(methodName='y')

print tr.y(ZeroDivisionError, lambda : 1/0)

# But if the code provided doesn't raise an exception,
# we get an AssertionError instead. No good....
# TestCase has attribute failedException. Maybe I can make a
# dummy exception...?

class Foo(Exception):
    def __new__(self):
        return BaseException()
    def __init__(self):
        pass

## orr...

class Concise(unittest.TestCase):
    class Nop:
        def __init__(self, hi): pass
        def __call__(self): pass

    failureException = Nop
    def runTest(self, ex, func):
        return self.assertRaises(ex, func) is None

c = Concise()
print c.runTest(ZeroDivisionError, lambda : 1/0)

# Alright, unittests here we go

# Keeping this version for now.

import StringIO

oldStdout, tmpStdout = sys.stdout, StringIO.StringIO()
oldStderr, tmpStderr = sys.stderr, StringIO.StringIO()
sys.stdout = tmpStdout
sys.stderr = tmpStderr

test = unittest.FunctionTestCase(lambda : 1 / 0)
runner = unittest.TextTestRunner(stream=sys.stdout, failfast=True)
pprint.pprint(runner.__dict__)
results = runner.run(test)

sys.stdout = oldStdout
sys.stderr = oldStderr

# print results.errors
# pprint.pprint(runner.run(test).errors)

test2 = unittest.FunctionTestCase(lambda : 1 / 1)
runner2 = unittest.TextTestRunner(stream=sys.stdout)
# pprint.pprint(runner2.run(test2).errors)
print 4

# Wrapping it in a function!

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

def trr(func):
    oldStdout, tmpStdout = sys.stdout, StringIO.StringIO()
    oldStderr, tmpStderr = sys.stderr, StringIO.StringIO()
    print 'asdf'
    sys.stdout = tmpStdout
    sys.stderr = tmpStderr
    test = unittest.FunctionTestCase(func)
    runner = unittest.TextTestRunner(stream=sys.stdout, failfast=True)
    print 'asdf'
    results = runner.run(test)
    sys.stdout = oldStdout
    sys.stderr = oldStderr
    return results.errors

# WOOOOO
def doesNotRaise(func):
    test = unittest.FunctionTestCase(func)
    runner = unittest.TextTestRunner(stream=StringIO.StringIO(), failfast=True)
    results = runner.run(test)
    return [] == results.errors

assert not doesNotRaise(lambda : 1 / 0)
assert doesNotRaise(lambda : 1 / 1)
assert doesNotRaise(lambda : sys.stdout.write('stdout\n'))
assert not doesNotRaise(lambda : sys.stderr.write('hahaha\n') or 1 / 0)
assert doesNotRaise(lambda : FutureWarning)
assert not doesNotRaise(lambda : [][0])
assert not doesNotRaise(lambda : dict()['NOT_HERE'])
print 'All doesNotRaise tests passed!'

# sys.stderr.write('hi\n')

# print bool(trr(sys.stderr.write('stderr\n')))


#################

# Commented out because the supression of printing
# was not effective. Better to just redirect stdout,
# stderr elsewhere, run, and then parse what was spewed.
#
# I do not feel motivated to implement the parsing rn.

# class MyTestResult(unittest.TextTestResult):
#     def addSuccess(self, test):
#         unittest.TestResult.addSuccess(self, test)
#     def addError(self, test, err):
#         unittest.TestResult.addError(self, test, err)
#     def addFailure(self, test, err):
#         unittest.TestResult.addFailure(self, test, err)

# class MyTestRunner(unittest.TextTestRunner):
#     def _makeResult(self):
#         return MyTestResult(self.stream, self.descriptions, self.verbosity)

# tmpStdout = StringIO.StringIO()
# tmpStderr = StringIO.StringIO()
# sys.stdout = tmpStdout
# sys.stderr = tmpStderr

# test = unittest.FunctionTestCase(lambda : 1 / 0)
# runner = MyTestRunner(stream=sys.stdout, failfast=True, descriptions=False)
# pprint.pprint(runner.__dict__)
# pprint.pprint(runner.run(test).errors)

# test2 = unittest.FunctionTestCase(lambda : 1 / 1)
# runner2 = MyTestRunner(stream=sys.stdout)
# pprint.pprint(runner2.run(test2).errors)
# print 4

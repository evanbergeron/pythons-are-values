import unittest
from os import listdir
from os.path import isfile, join
from textwrap import dedent

import expressionize as exp

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.tests = []
        self.reserved_names = {'__builtins__', 'code'}

    def namespaceCheck(self, test):
        def run(code):
            # print code
            exec code in locals()
            return locals()
        orig_ns, expr_ns = run(test), run(exp.main(test))
        orig_vars, expr_vars = set(orig_ns.keys()), set(expr_ns.keys())
        for var in (orig_vars & expr_vars) - self.reserved_names:
            # print orig_ns[var]
            if hasattr(orig_ns[var], '__eq__'):
                self.assertEqual(orig_ns[var], expr_ns[var])

    def test_all(self):
        def run(code):
            exec code in locals()
            return locals()
        for test in self.tests:
            orig_ns, expr_ns = run(test), run(exp.main(test))
            orig_vars, expr_vars = set(orig_ns.keys()), set(expr_ns.keys())
            for var in (orig_vars & expr_vars) - self.reserved_names:
                if hasattr(orig_ns[var], '__eq__'):
                    self.assertEqual(orig_ns[var], expr_ns[var])

class LoopsAndConditionals(MyTestCase):
    def setUp(self):
        super(LoopsAndConditionals, self).setUp()
        self.tests = [dedent(text) for text in [
            '''
            x = 32
            for i in xrange(5):
                x += i
            ''',
            '''
            y = 3
            for i in xrange(3):
                for j in xrange(2):
                    y += i ^ j
            ''',
            '''
            z = 123
            for i in xrange(4):
                for j in xrange(2):
                    for k in xrange(6):
                        z = z - i * j + k
            ''',
            '''
            x = 3
            if x % 2:
                x = 5
                if x % 2:
                    x = 8
                else:
                    x = False
            else:
                None
            ''',
            ]]

class Functions(MyTestCase):
    def setUp(self):
        super(Functions, self).setUp()
        self.tests = [dedent(text) for text in [
            '''
            y = 2
            def foo(x):
                x += 4
                return x + 1
            z = foo(y)
            ''',
            ]]

class AllTests(MyTestCase):
    def setUp(self):
        super(AllTests, self).setUp()

    def test_all(self): pass

if __name__ == "__main__":
    testdir = 'tests'
    externalTests = [(f, open(join(testdir, f), 'r').read())
            for f in listdir('tests') if f.endswith('.py')]
    for name, test in externalTests:
        setattr(AllTests, 'test_%s' % name,
                (lambda test : lambda self : self.namespaceCheck(test))(test))
    unittest.main()

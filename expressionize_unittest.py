import unittest
from textwrap import dedent

import expressionize as exp

class LoopsAndConditionals(unittest.TestCase):

    def setUp(self):
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
        ]]
        self.reserved_names = {'__builtins__', 'code'}

    def test_all(self): 
        def run(code):
            exec code in locals()
            return locals()
        for test in self.tests:
            orig_ns, expr_ns = run(test), run(exp.main(test)) 
            orig_vars, expr_vars = set(orig_ns.keys()), set(expr_ns.keys())
            for var in (orig_vars & expr_vars) - self.reserved_names:
                self.assertEqual(orig_ns[var], expr_ns[var])


if __name__ == "__main__":
    unittest.main()

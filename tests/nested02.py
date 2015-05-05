def foo():
    def bar():
        def baz():
            None
        baz()
    bar()
foo()

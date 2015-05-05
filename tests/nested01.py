def foo():
    def bar():
        None
    return bar()
print foo()

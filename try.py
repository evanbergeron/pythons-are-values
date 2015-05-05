(__import__('sys')._getframe((-1)).f_locals.update({'sys': __import__('sys')}) or sys._getframe((-1)).f_locals.update({'MODULE_LEVEL_VARS': sys._getframe((-1)).f_locals}) or sys._getframe((-1)).f_locals.update({'let': (lambda x, v: MODULE_LEVEL_VARS.update({x: v}))}) or let('throw', (lambda e: (_ for _ in ()).throw(e))) or let('printf', (lambda *s: sys.stdout.write(('%s\n' % ' '.join(map(str, s)))))))

[foo for foo in [(lambda : [_() for _ in [(lambda : [bar for bar in [(lambda : None)]]), (lambda : bar())]])]]

printf(foo())

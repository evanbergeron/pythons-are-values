(() or (__import__('sys')._getframe((-1)).f_locals.update({'sys': __import__('sys')}) or sys._getframe((-1)).f_locals.update({'MODULE_LEVEL_VARS': sys._getframe((-1)).f_locals}) or sys._getframe((-1)).f_locals.update({'let': (lambda x, v: MODULE_LEVEL_VARS.update({x: v}))}) or let('throw', (lambda e: (_ for _ in ()).throw(e))) or let('printf', (lambda *s: sys.stdout.write(('%s\n' % ' '.join(map(str, s))))))) or \
\
([i for i in [0]] and ()) or [(lambda : (() or ([i for i in [(j + 1)]] and ())))() for _ in xrange(2)])

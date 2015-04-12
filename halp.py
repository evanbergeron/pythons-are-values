(() or (__import__('sys')._getframe((-1)).f_locals.update({'sys': __import__('sys')}) or sys._getframe((-1)).f_locals.update({'printf': (lambda *s: sys.stdout.write(('%s\n' % ' '.join(map(str, s))))), 'vvvs': sys._getframe((-1)).f_locals, 'let': (lambda x, v: vvvs.update({x: v})), 'throw': (lambda e, msg: (_ for _ in ()).throw(e(msg)))})) or printf(123))


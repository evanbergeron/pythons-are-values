(globals().update({'let_global': (lambda k, v: globals().update({k: v}))}) or let_global('sys', __import__('sys')) or let_global('throw', (lambda e: (_ for _ in ()).throw(e))) or let_global('printf', (lambda *s: sys.stdout.write(('%s\n' % ' '.join(map(str, s)))))) or let_global('WHILE', (lambda e, b: ((e() and (b(), WHILE(e, b))) or None))))
raise Exception('hello world')

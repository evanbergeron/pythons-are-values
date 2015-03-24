from cStringIO import StringIO

tmp = StringIO()
tmp.write("hello\n")
print tmp.getvalue()
tmp.close()

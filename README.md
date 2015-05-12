# Pythons are Values

Pythons are Values is a hypothesis - that every python program has an equivalent one-liner. This goal is accomplished in a number of horrible, horrible ways. More coming soon.

### Features

The most up-to-date version of the project is in expressionize.py. The other python program is supplied as input via the command line. It is then parsed with the ast module into an abstract syntax tree. This tree is traversed and modified with DFS.

- *Variable Assignment*
```python
[foo for foo in [5]] # foo = 5
```
(Python 2.7 specific). One may also have
```python
lambda k,v : globals().update({k:v})
```
- Printing
```python
lambda *s : sys.stdout.write('%s\\n' % ' '.join(map(str, s)))
```
- Raising exceptions:
```python
lambda e : (_ for _ in ()).throw(e)
```
- Conditionals as nested if-else expressions
- For loops as list comphrensions
- While loops as recursive lambda functions

### Todo
- Fix namespace issues
- Tail recursion optimization to fix while loop lambda
- Classes
- Coroutines to generator comphrensions
- Metaclasses / default type constructors
- Try / Except clauses

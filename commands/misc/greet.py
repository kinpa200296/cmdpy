from api import *


cache = []


@cmd_func('greet')
def greet(interpreter, line):
    if line:
        greeting = "hello, " + line
        if not line in cache:
            cache.append(line)
    else:
        greeting = 'hello'
    print greeting


@cmd_helper('greet')
def help_greet(interpreter):
    print '\n'.join([
        'Greets person'
    ])


@cmd_completer('greet')
def complete_greet(interpreter, text, line, begidx, endidx):
    if not text:
        return cache
    else:
        return [l for l in cache if l.startswith(text)]

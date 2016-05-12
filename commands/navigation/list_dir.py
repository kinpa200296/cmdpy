from api import *
import os


@cmd_func('ls', ['dir'])
def list_dir(interpreter, line):
    if not line:
        res = os.listdir('.')
    else:
        dir = os.path.dirname(line)
        if not dir:
            res = os.listdir('.')
            inp = line
        else:
            res = os.listdir(dir)
            inp = line[len(dir) + 1:]
        res = filter(lambda d: d.startswith(inp), res)
    res = [p + os.path.sep if os.path.isdir(p) else p for p in res]
    interpreter.poutput('\n'.join(res))


@cmd_helper('ls', ['dir'])
def help_list_dir(interpreter):
    interpreter.poutput('\n'.join([
        'ls\t\t print current directory contents',
        'ls [path]\t print directories and files matching [path]'
    ]))


@cmd_completer('ls', ['dir'])
def complete_list_dir(interpreter, text, line, begidx, endidx):
    path = line[3:]
    if not path:
        res = next(os.walk('.'))[1]
        res = [p + os.path.sep if os.path.isdir(p) else p for p in res]
    else:
        dir = os.path.dirname(path)
        if not dir:
            res = next(os.walk('.'))[1]
        else:
            res = next(os.walk(dir))[1]
        res = filter(lambda d: d.startswith(text), res)
        res = [p + os.path.sep if os.path.isdir(os.path.join(dir, p)) else p for p in res]
    return res

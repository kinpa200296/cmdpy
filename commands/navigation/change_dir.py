from api import *
import os


@cmd_func('cd', ['chdir'])
def chdir(interpreter, line):
    if not line:
        interpreter.poutput(os.path.abspath(os.path.curdir))
    else:
        try:
            os.chdir(line)
        except:
            interpreter.poutput('Invalid path "{path}"'.format(path=line))


@cmd_helper('cd', ['chdir'])
def help_chdir(interpreter):
    interpreter.poutput('\n'.join([
        'cd\t\t print current directory',
        'cd [path]\t switch current directory to path'
    ]))


@cmd_completer('cd', ['chdir'])
def complete_chdir(interpreter, text, line, begidx, endidx):
    path = line[3:]
    if not path:
        res = next(os.walk('.'))[1]
        res = [p + os.path.sep if os.path.isdir(p) else p for p in res]
    else:
        dir = os.path.dirname(path)
        if not dir:
            res = next(os.walk('.'))[1]
        else:
            res = next(os.walk(os.path.dirname(path)))[1]
        res = filter(lambda d: d.startswith(text), res)
        res = [p + os.path.sep if os.path.isdir(os.path.join(dir, p)) else p for p in res]
    return res

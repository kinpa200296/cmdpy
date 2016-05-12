from api import cmd_func, cmd_helper


@cmd_func('echo', ['say'])
def echo(interpreter, line):
    interpreter.poutput(line)


@cmd_helper('echo', ['say'])
def help_echo(interpreter):
    interpreter.poutput('\n'.join([
        'echo [message]\t prints message to console'
    ]))

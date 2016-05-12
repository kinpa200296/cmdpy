from api import cmd_func, cmd_helper
import os


@cmd_func('pwd')
def print_dir(interpreter, line):
    interpreter.poutput(os.path.abspath(os.path.curdir))


@cmd_helper('pwd')
def help_print_dir(interpreter):
    interpreter.poutput("Print current directory")

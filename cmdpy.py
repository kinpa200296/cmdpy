from cmd2 import Cmd
import logging
import sys
import os
from core import inspect_package


class CmdPy(Cmd):

    ruler = '-'
    default_to_shell = True
    no_prompt = False

    Cmd.init_done = False
    Cmd.shortcuts.update({"$": 'var'})

    def __init__(self, *args, **kwargs):
        self.__logger = logging.getLogger("cmdpy.CmdPy")
        if not Cmd.init_done:
            self.setup_commands()
            Cmd.init_done = True
        Cmd.__init__(self, *args, **kwargs)
        self.vars = {}
        self.prompt = os.path.abspath(os.curdir) + '> '

    def setup_commands(self):
        self.__logger.debug('Starting commands loading')
        commands = inspect_package('commands')
        self.__logger.debug('Finished commands loading')
        for cmd in commands:
            if hasattr(Cmd, cmd.__name__):
                if cmd.is_alias:
                    self.__logger.warn('Can\'t add alias {name}. Name already exists'.format(name=cmd.__name__))
                else:
                    self.__logger.error('Can\'t add command {name}. Name already exists'.format(name=cmd.__name__))
            else:
                setattr(Cmd, cmd.__name__, cmd)
                if cmd.is_alias:
                    self.__logger.debug('Added alias {name}'.format(name=cmd.__name__))
                else:
                    self.__logger.debug('Added command {name}'.format(name=cmd.__name__))

    def precmd(self, line):
        if self.no_prompt:
            self.prompt = ''
        else:
            self.prompt = os.path.abspath(os.curdir) + '> '
        return Cmd.precmd(self, line)

    def help_q(self):
        self.poutput('Finish interpreter')

    def help_quit(self):
        return self.help_q()

    def help_exit(self):
        return self.help_q()

    def help_EOF(self):
        return self.help_q()

    def help_eof(self):
        return self.help_q()

    def do_about(self, line):
        self.poutput('\n'.join([
            'Interactive command interpreter'
        ]))

    def help_about(self):
        self.poutput('Prints this message: ')
        self.do_about('')

    def help_help(self):
        self.poutput('Prints information about available commands')

    def do_var(self, line):
        line = line.strip()
        var = line.split()[0]
        try:
            val = line.split()[1]
            self.vars[var] = val
        except IndexError:
            if var in self.vars:
                self.poutput('{var} = {val}'.format(var=var, val=self.vars[var]))
            else:
                self.poutput('Variable doesn\'t exists')

    def help_var(self):
        self.poutput('\n'.join([
            'var [name] [value] \t create a variable [name] = [value]',
            'var [name]\t\t displays variable value',
            'Also can be used through "$" shortcut'
        ]))

    def do_exec(self, line):
        if os.path.isfile(line):
            cmd_inst = CmdPy()
            cmd_inst.no_prompt = True
            cmd_inst.onecmd('load ' + line)
        else:
            self.poutput('Invalid path to script')

    def help_exec(self):
        self.poutput('\n'.join([
            'exec [filepath]\t run script in new context'
        ]))


if __name__ == '__main__':
    logger = logging.getLogger('cmdpy')
    logger.debug('Creating app instance')
    app = CmdPy()

    if len(sys.argv) == 2:
        logger.debug('Executing script {path}'.format(path=sys.argv[1]))
        app.no_prompt = True
        app.onecmd('load ' + sys.argv[1])
        logger.debug('Done executing')
    else:
        logger.debug('Starting cmd loop')
        app.cmdloop()
        logger.debug('Cmd loop finished')

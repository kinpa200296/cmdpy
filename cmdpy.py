import readline
import pywin
from cmd2 import Cmd
import logging
import sys
from core import inspect_package


class CmdPy(Cmd):
    def __init__(self, *args, **kwargs):
        self.__logger = logging.getLogger("cmdpy.CmdPy")
        self.setup_commands()
        Cmd.__init__(self, *args, **kwargs)

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


if __name__ == '__main__':
    logger = logging.getLogger('cmdpy')
    logger.debug('Creating app instance')
    app = CmdPy()
    logger.debug('Starting cmd loop')
    exit_code = 0
    try:
        app.cmdloop()
    except:
        exit_code = -1
        logger.error('Unhandled exception occurred. ' + sys.exc_info()[0])
    logger.debug('Cmd loop finished')
    sys.exit(exit_code)

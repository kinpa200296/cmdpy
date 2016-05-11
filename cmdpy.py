import readline
import pywin
from cmd2 import Cmd
import logging
from core import inspect_package


class CmdPy(Cmd):
    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.__logger = logging.getLogger("cmdpy.CmdPy")
        self.__logger.debug('Starting commands loading')
        self.commands = inspect_package('commands')
        self.__logger.debug('Finished commands loading')


if __name__ == '__main__':
    logger = logging.getLogger('cmdpy')
    logger.debug('Creating app instance')
    app = CmdPy()
    logger.debug('Starting cmd loop')
    app.cmdloop()
    logger.debug('Cmd loop finished')

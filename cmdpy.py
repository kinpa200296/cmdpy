import readline
import pywin
from cmd2 import Cmd
import logging, os, pkgutil
from datetime import datetime


class CmdPy(Cmd):
    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.__logger = logging.getLogger("cmdpy.CmdPy")
        self.load_commands()

    def load_commands(self):
        self.__logger.debug('Started commands load')
        try:
            self.__inspect_package('commands', True)
            self.__logger.debug('Finished commands load')
        except:
            self.__logger.error('Failed to load commands')

    def __inspect_package(self, name, is_pkg):
        for importer, name, is_pkg in pkgutil.iter_modules([name]):
            # if is_pkg:
            #     self.__inspect_package(name, is_pkg)
            # else:
            __import__(name)


def setup_logger(logger):
    logger.setLevel(logging.DEBUG)
    path = os.path.join('logs', '{date}-log.log'.format(date=datetime.now().ctime()))
    path = path.replace(':', ' ')
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    file_handler = logging.FileHandler(path, 'w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(name)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

if __name__ == '__main__':
    logger = logging.getLogger('cmdpy')
    setup_logger(logger)
    logger.debug('Creating app instance')
    app = CmdPy()
    logger.debug('Starting cmd loop')
    app.cmdloop()
    logger.debug('Cmd loop finished')

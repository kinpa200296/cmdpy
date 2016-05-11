import importlib
import logging
import pkgutil

logger = logging.getLogger('cmdpy.core.loader')


def inspect_package(pkg_name):
    commands = []
    for importer, name, is_pkg in pkgutil.iter_modules([pkg_name]):
        fullname = '.'.join([pkg_name, name])
        tmp = inspect_module(fullname)
        try:
            commands.extend(tmp)
        except TypeError:
            logger.error('Module {name} inspection returned {res}'.format(name=fullname, res=repr(tmp)))
    return commands


def inspect_module(name):
    logger.debug('Inspecting module {name}'.format(name=name))
    commands = []
    module = importlib.import_module(name)
    for val in module.__dict__.itervalues():
        if isinstance(val, type(inspect_module)):
            if hasattr(val, '_cmd_name') and hasattr(val, '_cmd_prefix') and hasattr(val, '_cmd_aliases'):
                tmp = make_commands(val)
                try:
                    commands.extend(tmp)
                except TypeError:
                    logger.error('Module {name} inspection returned {res}'.format(name=name, res=repr(tmp)))
    logger.debug('Done inspecting module {name}'.format(name=name))
    return commands

def make_commands(func):
    if not (hasattr(func, '_cmd_name') and hasattr(func, '_cmd_prefix') and hasattr(func, '_cmd_aliases')):
        logger.error('Invalid command function {func}'.format(func=repr(func)))
        raise ValueError('Invalid command function')
    commands = []
    # add command definition
    return commands

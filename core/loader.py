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
                    logger.error('Command {name} inspection returned {res}'.format(name=name, res=repr(tmp)))
    logger.debug('Done inspecting module {name}'.format(name=name))
    return commands


def cmd_wrapper(func, name, cmd_name, is_alias):
    def f(*args, **kwargs):
        return func(*args, **kwargs)
    f.__name__ = name
    f.cmd_name = cmd_name
    f.is_alias = is_alias
    if is_alias:
        logger.debug('Loaded alias {alias} for command {cmd}'.format(alias=name, cmd=cmd_name))
    else:
        logger.debug('Loaded {func} for command {cmd}'.format(func=name, cmd=cmd_name))
    return f


def make_commands(func):
    if not (hasattr(func, '_cmd_name') and hasattr(func, '_cmd_prefix') and hasattr(func, '_cmd_aliases')):
        logger.error('Invalid command function {func}'.format(func=repr(func)))
        raise ValueError('Invalid command function')
    cmd_name = getattr(func, '_cmd_name')
    cmd_prefix = getattr(func, '_cmd_prefix')
    cmd_aliases = getattr(func, '_cmd_aliases')
    logger.debug('Loading command {cmd} from function {func}'.format(cmd=cmd_name, func=func.__name__))
    commands = []
    commands.append(cmd_wrapper(func, '_'.join([cmd_prefix, cmd_name]), cmd_name, False))
    try:
        for alias in cmd_aliases:
            commands.append(cmd_wrapper(func, '_'.join([cmd_prefix, alias]), cmd_name, True))
    except TypeError:
        logger.debug('No aliases for {cmd} were found'.format(cmd=cmd_name))
        pass
    return commands
